/* This is an automatically generated file. Do not modify it.

This file was generated using `langgraph-gen` version 0.0.3.
To regenerate this file, run `langgraph-gen` with the source `YAML` file as an argument.

Usage:

1. Add the generated file to your project.
2. Create a new agent using the stub.

```typescript
import { createAgent } from "sample_02"


const StateAnnotation = Annotation.Root({
    // Define your state properties here
    foo: Annotation<string>(),
});

const agent = CustomAgentStub(Annotation.Root({ foo: Annotation<string>() }), {
    Node_1: (state) => console.log("In node: Node 1"),
    Node_2: (state) => console.log("In node: Node 2"),
    conditional_edge: (state) => {
        console.log("In condition: conditional_edge");
        throw new Error("Implement me. Returns one of the paths.");
    },
});

const compiled_agent = agent.compile();
console.log(await compiled_agent.invoke({ foo: "bar" }));
```

*/
import {
    StateGraph,
    START,
    END,
    type AnnotationRoot,
} from "@langchain/langgraph";

type AnyAnnotationRoot = AnnotationRoot<any>;

export function createAgent<TAnnotation extends AnyAnnotationRoot>(
  stateAnnotation: TAnnotation,
  impl: {
    Node_1: (state: TAnnotation["State"]) => TAnnotation["Update"],
    Node_2: (state: TAnnotation["State"]) => TAnnotation["Update"],
    conditional_edge: (state: TAnnotation["State"]) => string,
  }
) {
  return new StateGraph(stateAnnotation)
    .addNode("Node 1", impl.Node_1)
    .addNode("Node 2", impl.Node_2)
    .addConditionalEdges(
        START,
        impl.conditional_edge,
        [
            "Node 1",
            "Node 2",
            END,
        ]
    )
    .addEdge("Node 1", "Node 2")
    .addEdge("Node 2", END)
}