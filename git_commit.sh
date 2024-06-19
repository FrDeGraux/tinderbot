#!/bin/bash

# Check if an argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <string>"
  exit 1
fi

# Assign the first argument to a variable
command_name="$1"


git add .
echo "Running command: $command_name"
git push origin master

