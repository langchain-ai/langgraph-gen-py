# langgraph-gen

langgraph-gen is a CLI tool that allows you to auto-generate a LangGraph stub from a
specification file.

## Usage

```shell
pip install langgraph-gen
```

## Basic Usage

```shell
# Generate Python code from a YAML spec
langgraph-gen spec.yml

# Generate TypeScript code from a YAML spec
langgraph-gen spec.yml --language typescript

# Generate with custom output paths
langgraph-gen spec.yml -o custom_output.py --implementation custom_impl.py
```

## Command Line Options

```
langgraph-gen [options] input

Required arguments:
  input                 Input YAML specification file

Optional arguments:
  -l, --language        Language to generate code for (python, typescript)
                        Default: python
  -o, --output          Output file path for the agent stub
  --implementation      Output file path for an implementation with function stubs for all nodes
  -V, --version         Show program's version number and exit
```

## Example Spec

```YAML
# A simple 2-step Retrieval-Augmented Generation workflow
name: RagWorkflow
nodes:
- name: retrieve
- name: generate
edges:
- from: __start__
  to: retrieve
- from: retrieve
  to: generate
- from: generate
  to: __end__
```

## Quick Start

Create an example specification file and generate the code:

```shell
# Create a simple RAG workflow specification
cat > rag_example.yml << 'EOF'
# A simple 2-step Retrieval-Augmented Generation workflow
name: RagWorkflow
nodes:
  - name: retrieve
  - name: generate
edges:
  - from: __start__
    to: retrieve
  - from: retrieve
    to: generate
  - from: generate
    to: __end__
EOF

# Generate Python code
langgraph-gen rag_example.yml

# This will create rag_example.py and rag_example_impl.py
```

## Examples

You can find examples of the LangGraph specification together with the generated LangGraph stubs in the [examples](./examples) directory.