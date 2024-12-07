@echo off
echo =====================================================
echo Python Package Build and Publish Script
echo =====================================================
echo.

:: Step 1: Confirm before building the package
set /p confirmBuild="Do you want to build the package? (y/n): "
if /i "%confirmBuild%" NEQ "y" (
    echo Skipping package build.
    goto :end
)

echo Building the package...
python -m build
if %errorlevel% NEQ 0 (
    echo Error occurred while building the package. Exiting.
    goto :end
)
echo Package built successfully.
echo.

:: Step 2: Confirm before uploading to PyPI
set /p confirmUpload="Do you want to upload the package to PyPI? (y/n): "
if /i "%confirmUpload%" NEQ "y" (
    echo Skipping package upload.
    goto :end
)

echo Uploading the package to PyPI...
twine upload dist/*
if %errorlevel% NEQ 0 (
    echo Error occurred while uploading the package. Exiting.
    goto :end
)
echo Package uploaded successfully.
echo.

:end
echo Process completed.
pause
