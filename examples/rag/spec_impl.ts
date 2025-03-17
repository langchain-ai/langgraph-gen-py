/* This file was generated using `langgraph-gen` version 0.0.4.

This file provides a placeholder implementation for the corresponding stub.

Replace the placeholder implementation with your own logic.
*/
import { Annotation } from "@langchain/langgraph";

import { RagWorkflow } from "spec"

const agent = RagWorkflow(Annotation.Root({ foo: Annotation<string>() }), {
    retrieve: (state) => {
        console.log("In node: retrieve")
        return {} // Add your state update logic here
    },
    generate: (state) => {
        console.log("In node: generate")
        return {} // Add your state update logic here
    },
});

const compiled_agent = agent.compile();
console.log(await compiled_agent.invoke({ foo: "bar" }));