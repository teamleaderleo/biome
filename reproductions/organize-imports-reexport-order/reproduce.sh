#!/bin/sh
set -eu

cp index.mjs index.original.mjs
trap 'mv index.original.mjs index.mjs' EXIT

before=$(node consumer.mjs)
./node_modules/.bin/biome check index.mjs --write >/dev/null
after=$(node consumer.mjs)

printf 'before: %s\n' "${before#1:2:}"
printf 'after: %s\n' "${after#1:2:}"

test "$before" = "1:2:star,named"
test "$after" = "1:2:named,star"
