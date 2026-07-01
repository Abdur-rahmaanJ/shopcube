#!/bin/bash
# upload_all.sh - Build and upload packages to PyPI using token auth
#
# Usage:
#   ./upload_all.sh              # Upload all packages (shopcube + shopyo_ecommerce)
#   ./upload_all.sh shopcube     # Upload only shopcube
#   ./upload_all.sh shopyo_ecommerce  # Upload only shopyo_ecommerce

set -e

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$ROOT_DIR"

PYTHON="$ROOT_DIR/venv/bin/python"
TWINE="$ROOT_DIR/venv/bin/twine"

if [ ! -f "$PYTHON" ]; then
    echo "Error: Virtual environment not found in ./venv"
    exit 1
fi

if command -v uv &> /dev/null; then
    uv pip install --quiet --upgrade twine 2>/dev/null
else
    "$PYTHON" -m pip install --quiet --upgrade twine 2>/dev/null
fi

FILTER="$1"

PACKAGES=()
if [ -z "$FILTER" ]; then
    PACKAGES+=(".")
    PACKAGES+=("packages/shopyo_ecommerce")
elif [ "$FILTER" == "shopcube" ]; then
    PACKAGES+=(".")
elif [ "$FILTER" == "shopyo_ecommerce" ]; then
    PACKAGES+=("packages/shopyo_ecommerce")
else
    echo "Error: Unknown package '$FILTER'. Valid: shopcube, shopyo_ecommerce"
    exit 1
fi

FINAL_DIST="$ROOT_DIR/all_dist"
rm -rf "$FINAL_DIST"
mkdir -p "$FINAL_DIST"

if [ -z "$FILTER" ]; then
    echo "Building all packages..."
else
    echo "Building: $FILTER"
fi
echo "--------------------------"

for pkg in "${PACKAGES[@]}"; do
    if [ -f "$pkg/pyproject.toml" ] || [ -f "$pkg/setup.py" ]; then
        pkg_name=$(basename "$pkg")
        if [ "$pkg" == "." ]; then pkg_name="shopcube (root)"; fi

        echo "Building: $pkg_name"

        (
            cd "$pkg"
            rm -rf dist/ build/ *.egg-info
            "$PYTHON" -m build --outdir "$FINAL_DIST" . > /dev/null
        )
    fi
done

echo ""
echo "Uploading to PyPI..."
echo "--------------------------"

TWINE_USERNAME="__token__" "$TWINE" upload --verbose "$FINAL_DIST"/*

rm -rf "$FINAL_DIST"

echo ""
echo "All packages processed successfully!"
