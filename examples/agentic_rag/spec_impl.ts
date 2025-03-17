/* This file was generated using `langgraph-gen` version 0.0.4.

This file provides a placeholder implementation for the corresponding stub.

Replace the placeholder implementation with your own logic.
*/
import { Annotation } from "@langchain/langgraph";

import { AgenticRag } from "spec"

const agent = AgenticRag(Annotation.Root({ foo: Annotation<string>() }), {
    agent: (state) => {
        console.log("In node: agent")
        return {} // Add your state update logic here
    },
    retrieve: (state) => {
        console.log("In node: retrieve")
        return {} // Add your state update logic here
    },
    rewrite: (state) => {
        console.log("In node: rewrite")
        return {} // Add your state update logic here
    },
    generate: (state) => {
        console.log("In node: generate")
        return {} // Add your state update logic here
    },
    is_relevant: (state) => {
        console.log("In condition: is_relevant");
        throw new Error("Implement me. Returns one of the paths.");
    },
});

const compiled_agent = agent.compile();
console.log(await compiled_agent.invoke({ foo: "bar" }));