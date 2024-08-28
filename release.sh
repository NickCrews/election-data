#!/bin/bash
# eg ./releash.sh v2024-04-25_0
TAG=$1
git tag "$TAG"
git push --tags
gh release create --notes "" "$TAG" data/cleaned.parquet