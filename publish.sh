#!/bin/bash

echo "====================================================="
echo " Python Package Build and Publish Script"
echo "====================================================="
echo

# Step 1: Confirm before building the package
read -p "Do you want to build the package? (y/n): " confirmBuild
if [[ "$confirmBuild" != "y" && "$confirmBuild" != "Y" ]]; then
    echo "Skipping package build."
else
    echo "Building the package..."
    python -m build
    if [[ $? -ne 0 ]]; then
        echo "Error occurred while building the package. Exiting."
        exit 1
    fi
    echo "Package built successfully."
    echo
fi

# Step 2: Confirm before uploading to PyPI
read -p "Do you want to upload the package to PyPI? (y/n): " confirmUpload
if [[ "$confirmUpload" != "y" && "$confirmUpload" != "Y" ]]; then
    echo "Skipping package upload."
else
    echo "Uploading the package to PyPI..."
    twine upload dist/*
    if [[ $? -ne 0 ]]; then
        echo "Error occurred while uploading the package. Exiting."
        exit 1
    fi
    echo "Package uploaded successfully."
    echo
fi

echo "Process completed."
