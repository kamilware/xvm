#!/bin/sh

if [ -z "$1" ]; then
  echo "Usage: $0 <version>"
  exit 1
fi

VERSION="v$1"

git tag "$VERSION"

git push origin "$VERSION"
echo "Tag $VERSION created and pushed to origin."
