const { named, star } = await import("./index.mjs");

console.log(`${star}:${named}:${globalThis.evaluationOrder.join(",")}`);
