#!/bin/bash
# filepath: /Users/david/projects/filebundler/scripts/uv-build.sh

set -e

# Remove the dist directory if it exists
if [ -d "dist" ]; then
    echo "Removing existing dist/ directory..."
    rm -rf dist/
fi

# Run uv build
echo "Building with uv..."
uv build && uv publish

echo "Build complete. New artifacts are in dist/"