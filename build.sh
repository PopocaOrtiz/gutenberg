#!/bin/bash

# Create a temporary directory for the build
mkdir -p .aws-sam/build

# Install dependencies
pip install -r src/requirements.txt -t src/

# Build the SAM application
sam build

# Deploy the application
sam deploy --guided
