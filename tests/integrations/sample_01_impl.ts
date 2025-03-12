/* This file was generated using `langgraph-gen` version 0.0.3.

This file provides a placeholder implementation for the corresponding stub.

Replace the placeholder implementation with your own logic.
*/
import { Annotation } from "@langchain/langgraph";

import { createAgent } from "sample_01"

const agent = createAgent(Annotation.Root({ foo: Annotation<string>() }), {
    Node_1: (state) => {
        console.log("In node: Node 1")
        return {} // Add your state update logic here
    },
    Node_2: (state) => {
        console.log("In node: Node 2")
        return {} // Add your state update logic here
    },
    Node_3: (state) => {
        console.log("In node: Node 3")
        return {} // Add your state update logic here
    },
    conditional_edge: (state) => {
        console.log("In condition: conditional_edge");
        throw new Error("Implement me. Returns one of the paths.");
    },
});

const compiled_agent = agent.compile();
console.log(await compiled_agent.invoke({ foo: "bar" }));