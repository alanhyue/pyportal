#!/bin/bash

echo "====================================================="
echo " Python Package Build and Publish Script"
echo "====================================================="
echo

# Function to get package version from setup.py
get_version() {
    python -c "import re; print(re.search(r'version=\"([^\"]+)\"', open('setup.py').read()).group(1))"
}

# Step 1: Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/
echo "Cleaned."
echo

# Step 2: Confirm before building the package
read -p "Do you want to build the package? (y/n): " confirmBuild
if [[ "$confirmBuild" != "y" && "$confirmBuild" != "Y" ]]; then
    echo "Skipping package build."
else
    echo "Building the package..."
    python setup.py sdist bdist_wheel
    if [[ $? -ne 0 ]]; then
        echo "Error occurred while building the package. Exiting."
        exit 1
    fi
    echo "Package built successfully."
    echo
fi

# Step 3: Confirm before uploading to PyPI
read -p "Do you want to upload the package to PyPI? (y/n): " confirmUpload
if [[ "$confirmUpload" != "y" && "$confirmUpload" != "Y" ]]; then
    echo "Skipping package upload."
else
    # Get version for confirmation
    VERSION=$(get_version)
    echo "Uploading the package to PyPI..."
    echo "Package version: $VERSION"

    # Upload using explicit file paths
    twine upload dist/pyportal-$VERSION.tar.gz dist/pyportal-$VERSION-py3-none-any.whl
    if [[ $? -ne 0 ]]; then
        echo "Error occurred while uploading the package. Exiting."
        exit 1
    fi
    echo "Package uploaded successfully!"
    echo "Package should be available at: https://pypi.org/project/pyportal/$VERSION/"
    echo
fi

echo "Process completed."
