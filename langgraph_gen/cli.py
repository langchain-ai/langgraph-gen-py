"""Entrypoint script."""

import argparse
import sys
from pathlib import Path
from typing import Optional, Literal

from langgraph_gen._version import __version__
from langgraph_gen.generate import generate_from_spec


def _rewrite_path_as_import(path: Path) -> str:
    """Rewrite a path as an import statement."""
    return ".".join(path.with_suffix("").parts)


def _generate(
    input_file: Path,
    *,
    language: Literal["python", "typescript"],
    output_file: Optional[Path] = None,
    implementation: Optional[Path] = None,
) -> tuple[str, str]:
    """Generate agent code from a YAML specification file.

    Args:
        input_file (Path): Input YAML specification file
        language (Literal["python", "typescript"]): Language to generate code for
        output_file (Optional[Path]): Output Python file path
        implementation (Optional[Path]): Output Python file path for a placeholder implementation

    Returns:
        2-tuple of path: Path to the generated stub file and implementation file
    """
    if language not in ["python", "typescript"]:
        raise NotImplementedError(
            f"Unsupported language: {language} Use one of 'python' or 'typescript'"
        )
    suffix = ".py" if language == "python" else ".ts"
    output_path = output_file or input_file.with_suffix(suffix)

    # Add a _impl.py suffix to the input filename if implementation is not provided
    if implementation is None:
        implementation = input_file.with_name(f"{input_file.stem}_impl{suffix}")

    # Get the implementation relative to the output path
    stub_module = _rewrite_path_as_import(
        output_path.relative_to(implementation.parent)
    )

    spec_as_yaml = input_file.read_text()
    stub, impl = generate_from_spec(
        spec_as_yaml,
        "yaml",
        templates=["stub", "implementation"],
        language=language,
        stub_module=stub_module,
    )
    output_path.write_text(stub)
    implementation.write_text(impl)

    # Return the created files for reporting
    return output_path, implementation


def main() -> None:
    """Langgraph-gen CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate LangGraph agent base classes from YAML specs.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog="""
Examples:
  # Generate Python code from a YAML spec
  langgraph-gen spec.yml

  # Generate TypeScript code from a YAML spec
  langgraph-gen spec.yml --language typescript

  # Generate with custom output paths
  langgraph-gen spec.yml -o custom_output.py --implementation custom_impl.py
        """,
    )
    parser.add_argument("input", type=Path, help="Input YAML specification file")
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        default="python",
        help="Language to generate code for (python, typescript)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output file path for the agent stub",
        default=None,
    )

    parser.add_argument(
        "--implementation",
        type=Path,
        help="Output file path for an implementation with function stubs for all nodes",
        default=None,
    )

    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    # Custom error handling for argparse
    try:
        args = parser.parse_args()
    except SystemExit as e:
        # If there's a parse error (exit code != 0), print help and colorized error message
        if e.code != 0:
            parser.print_help()
            # Check if stderr is a TTY to use colors
            if sys.stderr.isatty():
                sys.stderr.write(
                    "\033[91m\nError: Invalid arguments. See usage above.\033[0m\n"
                )
            else:
                sys.stderr.write("\nError: Invalid arguments. See usage above.\n")
        sys.exit(e.code)

    # Check if input file exists
    if not args.input.exists():
        sys.stderr.write(f"Error: Input file {args.input} does not exist\n")
        sys.exit(1)

    # Generate the code
    try:
        stub_file, impl_file = _generate(
            input_file=args.input,
            output_file=args.output,
            language=args.language,
            implementation=args.implementation,
        )

        # Check if stdout is a TTY to use colors and emoji
        if sys.stdout.isatty():
            print("\033[32m✅ Successfully generated files:\033[0m")
            print(f"\033[32m📄 Stub file:          \033[0m {stub_file}")
            print(f"\033[32m🔧 Implementation file: \033[0m {impl_file}")
        else:
            print("Successfully generated files:")
            print(f"- Stub file:           {stub_file}")
            print(f"- Implementation file: {impl_file}")
    except Exception as e:
        # Use red color for errors if terminal supports it
        if sys.stderr.isatty():
            sys.stderr.write(f"\033[91mError: {str(e)}\033[0m\n")
        else:
            sys.stderr.write(f"Error: {str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
