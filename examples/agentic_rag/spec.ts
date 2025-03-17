/* This is an automatically generated file. Do not modify it.

This file was generated using `langgraph-gen` version 0.0.4.
To regenerate this file, run `langgraph-gen` with the source `YAML` file as an argument.

Usage:

1. Add the generated file to your project.
2. Create a new agent using the stub.

```typescript
import { AgenticRag } from "spec"


const StateAnnotation = Annotation.Root({
    // Define your state properties here
    foo: Annotation<string>(),
});

const agent = CustomAgentStub(Annotation.Root({ foo: Annotation<string>() }), {
    agent: (state) => console.log("In node: agent"),
    retrieve: (state) => console.log("In node: retrieve"),
    rewrite: (state) => console.log("In node: rewrite"),
    generate: (state) => console.log("In node: generate"),
    is_relevant: (state) => {
        console.log("In condition: is_relevant");
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

export function AgenticRag<TAnnotation extends AnyAnnotationRoot>(
  stateAnnotation: TAnnotation,
  impl: {
    agent: (state: TAnnotation["State"]) => TAnnotation["Update"],
    retrieve: (state: TAnnotation["State"]) => TAnnotation["Update"],
    rewrite: (state: TAnnotation["State"]) => TAnnotation["Update"],
    generate: (state: TAnnotation["State"]) => TAnnotation["Update"],
    is_relevant: (state: TAnnotation["State"]) => string,
  }
) {
  return new StateGraph(stateAnnotation)
    .addNode("agent", impl.agent)
    .addNode("retrieve", impl.retrieve)
    .addNode("rewrite", impl.rewrite)
    .addNode("generate", impl.generate)
    .addEdge(START, "agent")
    .addEdge("agent", "retrieve")
    .addConditionalEdges(
        "retrieve",
        impl.is_relevant,
        [
            "rewrite",
            "generate",
        ]
    )
    .addEdge("rewrite", "agent")
    .addEdge("generate", END)
}