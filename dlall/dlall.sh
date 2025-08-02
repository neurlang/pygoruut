#!/bin/bash

# Files
HASHES_FILE="hashes.txt"
LENGTHS_FILE="lengths.txt"
VERSION="v0.6.3"


wget https://github.com/neurlang/goruut/releases/download/$VERSION/goruut-android-arm64
wget https://github.com/neurlang/goruut/releases/download/$VERSION/goruut-darwin-amd64
wget https://github.com/neurlang/goruut/releases/download/$VERSION/goruut-darwin-arm64
wget https://github.com/neurlang/goruut/releases/download/$VERSION/goruut-freebsd-386
wget https://github.com/neurlang/goruut/releases/download/$VERSION/goruut-freebsd-amd64
wget https://github.com/neurlang/goruut/releases/download/$VERSION/goruut-freebsd-arm
wget https://github.com/neurlang/goruut/releases/download/$VERSION/goruut-freebsd-arm64
wget https://github.com/neurlang/goruut/releases/download/$VERSION/goruut-linux-386
wget https://github.com/neurlang/goruut/releases/download/$VERSION/goruut-linux-amd64
wget https://github.com/neurlang/goruut/releases/download/$VERSION/goruut-linux-arm
wget https://github.com/neurlang/goruut/releases/download/$VERSION/goruut-linux-arm64
wget https://github.com/neurlang/goruut/releases/download/$VERSION/goruut-linux-riscv64
wget https://github.com/neurlang/goruut/releases/download/$VERSION/goruut-windows-386
wget https://github.com/neurlang/goruut/releases/download/$VERSION/goruut-windows-amd64
wget https://github.com/neurlang/goruut/releases/download/$VERSION/goruut-windows-arm
wget https://github.com/neurlang/goruut/releases/download/$VERSION/goruut-windows-arm64


sha256sum goruut-* > hashes.txt
ls -l goruut-* | cut -d ' ' -f 5,10 > lengths.txt


# Version details

BASE_URL="https://github.com/neurlang/goruut/releases/download/$VERSION/"

# Initialize releases array
echo "releases = ["

# Read lengths.txt and iterate over each line
while read -r length name; do
  # Extract the hash for the corresponding name from hashes.txt
  hash=$(grep "$name" "$HASHES_FILE" | awk '{print $1}')
  
  # Extract architecture and OS from the name
  IFS='-' read -ra parts <<< "$name"
  os="${parts[1]}"
  arch="${parts[2]}"

  # Generate the required entry
  echo "  ["
  echo "    100, \"$VERSION\","
  echo "    $length,"
  echo "    \"$hash\","
  echo "    \"$arch\", \"$os\","
  echo "    [\"$BASE_URL\"],"
  echo "  ],"

done < "$LENGTHS_FILE"

# Close releases array
echo "]"
