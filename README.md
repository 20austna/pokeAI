# PokeAI

![License](https://img.shields.io/badge/license-MIT-blue)

## Table of Contents
- [About the Project](#about-the-project)
- [Getting Started](#getting-started)
- [License](#license)
- [Contact](#contact)

## About the Project

PokeAI utilizes openAIs chatAI and a fork of gym-retro(Stable-Retro) to have chatGPT play Pokemon. 

### Built With
- [stable-retro](https://github.com/Farama-Foundation/stable-retro)
- [Gym Retro](https://github.com/openai/retro.git)
- [OpenAI Platform](https://platform.openai.com/docs/api-reference/introduction)

## Getting Started

To get a local copy up and running, follow these steps.

### Prerequisites
- [Stable Retro](https://github.com/Farama-Foundation/stable-retro)
- [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
- Legal Pokemon Silver ROM

### Installation
1. Install Stable Retro Dependencies: 
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-pip git zlib1g-dev libopenmpi-dev ffmpeg
   ```
2. Clone Stable-Retro:
   ```bash
   git clone https://github.com/Farama-Foundation/stable-retro.git
   cd stable-retro
   ```
3. Create and activate a virtual environment (recommended):
   ```bash
   virtualenv --system-site-packages -p python3 /path/to/venv
   source venv/bin/activate 
   ```
4. Install Stable-Retro as editable to virtual environment:
   ```bash
   pip3 install -e .
   ```
5. Install stable baselines 3 version that supports gymnasium & install openGL:
   ```bash
   pip3 install stable_baselines3[extra]
   sudo apt-get install python3-opengl
   ```
6. (In whatever directory you want pokeAI) clone pokeAI:
   ```bash
   git clone git@github.com:20austna/pokeAI.git
   ```
7. Add Game Integration files to retro
   ```bash
   cp -r /path/to/pokeAI/PokemonSilver-GbColor /path/to/venv/lib/python3.XX/site-packages/retro/data/stable/PokemonSilver-GbColor
   ```
8. Run the project(ensure you have a legally obtained PokemonSilver ROM, see below):
   ```bash
   /path/to/venv/bin/python silver.py
   ```

**Note**: The ROM file itself is not included and must be legally obtained and added to the `/path/to/venv/lib/python3.XX/site-packages/retro/data/stable/PokemonSilver-GbColor` folder separately.


## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Nathaniel Austen - 20austna@gmail.com

Ariah Peregrina - peregran@miamioh.edu

Malak Lamsettef - lamsetm@miamioh.edu

Mihir Tamrakr - tamrakm@miamioh.edu

Project Link: https://github.com/20austna/pokeAI
