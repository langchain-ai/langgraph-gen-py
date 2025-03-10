#!/usr/bin/env python3
"""LangGraph Agent Code Generator CLI"""

import json
import re
from pathlib import Path
from typing import Any, Callable, Literal, Set, Optional

import jinja2
import yaml
from jinja2.sandbox import SandboxedEnvironment
from langgraph.graph import StateGraph, START, END

from langgraph_gen._version import __version__

HERE = Path(__file__).parent

ASSETS = HERE / "assets"


def _load_template(name: str) -> str:
    """Load a template from the assets directory"""
    with open(ASSETS / name) as f:
        return f.read()


# Load fully generated functional stub
PY_STUB = _load_template("py-stub.j2")
PY_IMPL = _load_template("py-stub-impl.j2")

# TypeScript templates
TS_STUB = _load_template("ts-stub.j2")
TS_IMPL = _load_template("ts-stub-impl.j2")


class InvalidSpec(Exception):
    """Invalid spec."""


def _validate_spec(spec: Any) -> None:
    """Raise an error if the spec is invalid."""
    if not isinstance(spec, dict):
        raise InvalidSpec("Specification must be a top level dictionary.")
    required_fields = {"nodes", "edges"}
    if not required_fields.issubset(spec.keys()):
        missing = required_fields - spec.keys()
        raise ValueError(f"Missing required fields in spec: {', '.join(missing)}")

    node_names = {n["name"] for n in spec["nodes"]}
    for edge in spec["edges"]:
        if edge["from"] not in node_names and edge["from"] != START:
            raise ValueError(f"Edge source node '{edge['from']}' not defined in nodes")
        if "to" in edge:
            if edge["to"] not in node_names and edge["to"] != END:
                raise ValueError(
                    f"Edge target node '{edge['to']}' not defined in nodes"
                )


PATTERN = re.compile(r"\W")


def _update_spec(spec: dict) -> None:
    """Add an id to each node in the spec which will be used as a machine name."""
    for node in spec["nodes"]:
        # Set the node id to be a "machine name" if not provided
        # convert any non alpha-numeric characters to underscores
        node["id"] = PATTERN.sub("_", node["name"])


def generate_from_spec(
    spec_str: str,
    format_: Literal["yaml", "json"],
    templates: list[Literal["stub", "implementation"]],
    *,
    language: Literal["python", "typescript"] = "python",
    stub_module: Optional[str] = None,
) -> list[str]:
    """Generate agent code from a YAML specification file.

    Args:
        spec_str: Specification encoded as a string
        format_: Format of the specification
        templates: Sequence of templates to generate
        language: Language to generate code for
        stub_module If known, the module name to import the stub from.
            This will be known in the CLI.

    Returns:
        list[str]: List of generated code files, in the same order as the templates.
    """
    if format_ == "yaml":
        try:
            spec = yaml.safe_load(spec_str)
        except Exception:
            raise InvalidSpec("Invalid YAML spec.")
    elif format_ == "json":
        try:
            spec = json.loads(spec_str)
        except Exception:
            raise InvalidSpec("Invalid JSON spec.")
    else:
        raise ValueError(f"Invalid format: {format_}")

    _validate_spec(spec)
    # Add machine names to the nodes
    _update_spec(spec)

    env = SandboxedEnvironment(
        loader=jinja2.BaseLoader, trim_blocks=True, lstrip_blocks=True
    )

    generated = []

    for template_name in templates:
        try:
            if template_name == "stub":
                if language == "python":
                    template = env.from_string(PY_STUB)
                elif language == "typescript":
                    template = env.from_string(TS_STUB)
                else:
                    raise ValueError(f"Invalid language: {language}")
            elif template_name == "implementation":
                if language == "python":
                    template = env.from_string(PY_IMPL)
                elif language == "typescript":
                    template = env.from_string(TS_IMPL)
                else:
                    raise ValueError(f"Invalid language: {language}")
            else:
                raise ValueError(f"Invalid template type: {template_name}")
            # Update the name based on the language

            if "name" not in spec:
                if language == "python":
                    stub_name = "create_agent"
                elif language == "typescript":
                    stub_name = "createAgent"
                else:
                    raise ValueError(f"Invalid language: {language}")
            else:
                stub_name = spec["name"]

            code = template.render(
                stub_name=stub_name,
                nodes=spec["nodes"],
                edges=spec["edges"],
                entrypoint=spec.get("entrypoint", None),
                version=__version__,
                stub_module=stub_module,
            )
            generated.append(code)
        except jinja2.TemplateError as e:
            raise AssertionError(
                f"Error rendering template: {str(e)}",
            )

    return generated


def _add_to_graph(
    state_graph: StateGraph,
    spec: str,
    implementations: list[tuple[str, Callable]],
) -> None:
    """Add edges and implementations to the state graph, updating it in place.

    Args:
        state_graph (StateGraph): The state graph to update.
        spec: Specification as a YAML string
        implementations (list[tuple[str, Callable]]): The list of implementations.
    """
    spec_ = yaml.safe_load(spec)

    # Declare the state graph
    if not isinstance(spec_, dict):
        raise TypeError(
            f"Specification must be a top level dictionary. Found: {type(spec_)}"
        )

    # Identify all node implementations by scanning the edges
    if "edges" not in spec_:
        raise ValueError("Missing key 'edges' in spec.")

    edges = spec_["edges"]
    found_nodes: Set[str] = set()

    for edge in edges:
        if "from" in edge:
            found_nodes.add(edge["from"])
        if "to" in edge:
            found_nodes.add(edge["to"])
        if "condition" in edge:
            found_nodes.add(edge["condition"])
        if "paths" in edge:
            if isinstance(edge["paths"], dict):
                found_nodes.update(edge["paths"].values())
            elif isinstance(edge["paths"], list):
                found_nodes.update(edge["paths"])
            else:
                raise TypeError(f"Invalid paths: {edge['paths']}")

    # Remove the end node from the edges since it's a special case
    found_nodes = found_nodes - {"__end__"}

    nodes_by_name = {name: implementation for name, implementation in implementations}
    found_implementations = set(nodes_by_name)

    missing_implementations = found_nodes - found_implementations

    if missing_implementations:
        raise ValueError(f"Missing implementations for : {missing_implementations}")

    for name, node in nodes_by_name.items():
        state_graph.add_node(name, node)

    for edge in spec_["edges"]:
        # It's a conditional edge
        if "condition" in edge:
            state_graph.add_conditional_edges(
                edge["from"],
                nodes_by_name[edge["condition"]],
                path_map=edge["paths"] if "paths" in edge else None,
            )
        else:
            # it's a directed edge
            state_graph.add_edge(edge["from"], edge["to"])

    # Set the entry point
    if "entrypoint" in spec_:
        state_graph.add_edge(START, spec_["entrypoint"])


def _add_to_graph_from_yaml(
    state_graph: StateGraph,
    spec: str,
    implementations: list[tuple[str, Callable]],
) -> None:
    """Add edges and implementations to the state graph, updating it in place.

    Args:
        state_graph (StateGraph): The state graph to update.
        spec: Specification as a YAML string
        implementations (list[tuple[str, Callable]]): The list of implementations.
    """
    spec_ = yaml.safe_load(spec)
    return _add_to_graph(
        state_graph,
        spec_,
        implementations,
    )
