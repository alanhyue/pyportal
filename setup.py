from setuptools import setup, find_packages

# Read the README file for long description
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pyportal",
    version="1.0.0",
    description="Import Python script from any directory or git commit history.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Alan Yue",
    author_email="alanyue@example.com",  # Placeholder email - replace with actual email
    url="https://github.com/alanyue/pyportal",  # Placeholder URL - replace with actual repo
    license="MIT",

    # Automatically find packages
    packages=find_packages(),

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    keywords="import python scripts git version control",
)
