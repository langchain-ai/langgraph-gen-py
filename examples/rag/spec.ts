/* This is an automatically generated file. Do not modify it.

This file was generated using `langgraph-gen` version 0.0.4.
To regenerate this file, run `langgraph-gen` with the source `YAML` file as an argument.

Usage:

1. Add the generated file to your project.
2. Create a new agent using the stub.

```typescript
import { RagWorkflow } from "spec"


const StateAnnotation = Annotation.Root({
    // Define your state properties here
    foo: Annotation<string>(),
});

const agent = CustomAgentStub(Annotation.Root({ foo: Annotation<string>() }), {
    retrieve: (state) => console.log("In node: retrieve"),
    generate: (state) => console.log("In node: generate"),
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

export function RagWorkflow<TAnnotation extends AnyAnnotationRoot>(
  stateAnnotation: TAnnotation,
  impl: {
    retrieve: (state: TAnnotation["State"]) => TAnnotation["Update"],
    generate: (state: TAnnotation["State"]) => TAnnotation["Update"],
  }
) {
  return new StateGraph(stateAnnotation)
    .addNode("retrieve", impl.retrieve)
    .addNode("generate", impl.generate)
    .addEdge(START, "retrieve")
    .addEdge("retrieve", "generate")
    .addEdge("generate", END)
}