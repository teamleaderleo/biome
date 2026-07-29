# `organizeImports` re-export evaluation-order reproduction

This is a standalone reproduction for Biome 2.5.6.

Biome's `organizeImports` action sorts these adjacent re-export declarations by source:

```js
export * from "./star.mjs";
export { named } from "./named.mjs";
```

After `biome check --write`, the named re-export comes first. Both target modules run top-level code, so the observable evaluation order changes from `star,named` to `named,star`.

## Run

```sh
npm install
sh reproduce.sh
```

Expected output:

```text
before: star,named
after: named,star
```

## Safety implication

The action is currently recommended and marked safe. Reordering multiple re-export declarations can change program behaviour, so that part of the action should either preserve source order or be classified as unsafe.

This directory is investigation material in a fork. It is not an upstream report or submission.
