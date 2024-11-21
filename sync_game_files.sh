#!/bin/bash

# Define source and destination paths
SOURCE_DIR="/home/borg/cse434/pokeAI/PokemonSilver-GbColor"
DEST_DIR="/home/borg/vretro/lib/python3.12/site-packages/retro/data/stable/PokemonSilver-GbColor"

# Create destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Copy files from source to destination
cp -r "$SOURCE_DIR"/* "$DEST_DIR"

echo "PokemonSilver-GbColor has been synced to $DEST_DIR"
