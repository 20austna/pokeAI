# PokeAI

![License](https://img.shields.io/badge/license-MIT-blue)

## Table of Contents
- [About the Project](#about-the-project)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## About the Project

Provide a short description of your project here:
- What does it do?
- Why did you create it?
- What problem does it solve?

### Built With
- [stable-retro](https://github.com/Farama-Foundation/stable-retro)
- [Gym Retro](https://github.com/openai/retro.git)
- [OpenAI Platform](https://platform.openai.com/docs/api-reference/introduction)

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites
- [Required Software 1](https://link-to-software.com)
- [Required Software 2](https://link-to-software.com)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/20austna/pokeAI.git
   ```
2. Navigate to the project directory:
   ```bash
   cd pokeAI
   ```
3. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate   # On Windows
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the project:
   ```bash
   python test.py  # Replace with entry point
   ```

## Adding Game Integration Files

To run the project, you need to integrate the game files into `gym-retro`:

1. Copy the `retro_integration/PokemonSilver-GbColor` folder from this repository.
2. Place it in the following directory within your virtual environment:
   
   ```bash
   venv/lib/python3.12/site-packages/retro/data/stable/
   ```

   Ensure that the path `venv/lib/python3.12/site-packages/retro/data/stable/PokemonSilver-GbColor` exists and contains the integration files.

**Note**: The ROM file itself is not included and must be legally obtained and added to the `PokemonSilver-GbColor` folder separately.

## Usage

Provide examples and instructions on how to use your project effectively. Include screenshots or code snippets as necessary.

## Features
- Feature 1: Brief description
- Feature 2: Brief description
- Feature 3: Brief description


## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Nathaniel Austen - 20austna@gmail.com
TODO: Other contributor's names and emails

Project Link: https://github.com/20austna/pokeAI
