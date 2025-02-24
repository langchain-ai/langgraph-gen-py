# langgraph-gen

langgraph-gen is a CLI tool that allows you to auto-generate a LangGraph stub from a
specification file.

## Usage

```shell
pip install langgraph-gen
```
## Stubs for Python

```shell
langgraph-gen --input <path-to-spec-file> --output <path-to-output-file> --language python
```

## Stubs for TypeScript

```shell
langgraph-gen --input <path-to-spec-file> --output <path-to-output-file> --language typescript
```

## Example Spec

```YAML
# A simple 2-step Retrieval-Augmented Generation workflow
name: RagWorkflow
entrypoint: retrieve
nodes:
- name: retrieve
- name: generate
  edges:
- from: retrieve
  to: generate
- from: generate
  to: __end__
```

## Examples

You can find examples of the LangGraph specification together with the generated LangGraph stubs in the [examples](./examples) directory.