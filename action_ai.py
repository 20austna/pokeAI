import os
import openai
import json
from dotenv import load_dotenv

load_dotenv()

# Set OpenAI API key and change to your API key name
openai.api_key = os.getenv("PokemonAPI")
if not openai.api_key:
    raise ValueError("Missing OpenAI API key. Set OPENAI_API in your environment or .env file.")

# Initialize an empty action queue
action_queue = []

def add_to_q(nums):
    """Add an array of numbers to the action queue."""
    for num in nums:
        action_queue.append(num)
        print(f"Added {num} to action queue.")

def get_action_queue(action_description, menu_state):
    # Define the messages for the Action AI
    messages = [
        {"role": "system", "content": """
                                         You are a Pokémon battle assistant, specialized in generating action inputs to navigate menus in Pokémon battles. 
                                         Here is some background info: 
                                         1. Controller inputs are represented in code as an array. 
                                         Each array index corresponds to a button on the controller: 
                                         ['B', None, 'SELECT', 'START', 'UP', 'DOWN', 'LEFT', 'RIGHT', 'A']. 
                                         So to press 'B' return 0, to press 'select' return 2, 'start' return 3 and so on. 
                                         Always return a sequence of number(s), for example to press down the b return [5,0]. 
                                         2. A cursor(▶) will be next to a option in the menu, consider where the cursor is to determine where in the list you are. 
                                         3. You will be provided a menu state and a desired action, you must first determine what type of menu you are in as that will determine how to navigate. 
                                         For example if the menu is a move menu, each move is on its own line arranged top to bottom(left to right and past a carriage return in a string)
                                         but if you are in the main menu things are arranged in a square so the first two are on the first line and the next two on the next line. 
                                         So, pressing down while on the first item would skip you to the third item, 
                                         while pressing right on the first would send you to the second.
                                         4. You must use the function `add_to_q(nums)` to add numbers to the action queue, do this via your function_call not here in content. 
                                         5. Provide your reasoning explicitly in addition to returning the necessary function calls. """},
        {"role": "user", "content": f"You must provide your reasoning before calling any functions. Given the menu state: '{menu_state}', and the desired action: '{action_description}', please provide the necessary controller inputs and your reasoning."},
    ]

    # Call OpenAI API to get the action queue
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        #function_call={"name": "add_to_q"},  # Indicate that the AI can call this function
        functions=[
            {
                "name": "add_to_q",
                "description": "Add an array of numbers to the action queue.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "nums": {
                            "type": "array",
                            "items": {
                                "type": "integer",
                            },
                            "description": "An array of numbers to add to the action queue."
                        }
                    },
                    "required": ["nums"]
                }
            }
        ],
        temperature=1,  # Use a lower temperature for deterministic output
    )

    # Print the raw response for debugging
    print("Raw response from API:", response)


    function_call = response.choices[0].message.function_call
    # Process the function call response
    if function_call and function_call.name == "add_to_q":
        arguments = json.loads(function_call.arguments)
        nums = arguments.get("nums")  # Extract the number
        if nums:
            add_to_q(nums)

# Example usage
if __name__ == "__main__":
    # Simulate the decision to attack
    action_description = "use the move scratch"  # Placeholder action
    menu_state = "║   ║1. SCRATCH      ║\n║   ║2.▶LEER         ║\n║   ║3. RAGE         ║\n║   ║4. -            ║"  # Current menu state

    get_action_queue(action_description, menu_state)
    print("Current action queue:", action_queue)
