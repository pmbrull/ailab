#!/bin/bash

echo "Downloading Ollama..."
apt update && apt install -y curl
curl -fsSL https://ollama.com/install.sh | sh

echo "Starting Ollama server..."
ollama serve &

echo "Waiting for Ollama server to be active..."
while [ "$(ollama list | grep 'NAME')" == "" ]; do
  sleep 1
done


ollama pull mxbai-embed-large
