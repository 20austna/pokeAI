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
    global action_queue
    for num in nums:
        action_queue.append(num)
        #print(f"Added {num} to action queue.")

def get_action_queue(action_description, menu_state):
    # Define the messages for the Action AI
    global action_queue
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
                                         but if you are in the main menu things are arranged in a square so the first two(FIGHT and PKMN) are on the first line and the next two(PACK and RUN) on the next line. 
                                         So, pressing down while on the first item would skip you to the third item, 
                                         Likewise pressing right on the third item would send you to the four and up on the fourth to the second. 
                                         4. Use the function `add_to_q(nums)` to add numbers to the action queue. You must invoke this via a `function_call`
                                         5. When doing inputs that will navigate you to another menu (only applies to pressing A or B) you cannot assume the position of the cursor since that depends on information that you do not have. Therefore, when in the main menu and pressing A to enter the move menu, do not continue. 
                                         6. In order to "use" or "select" a move you must navigate to the move and press 'A' when appropriate 
                                         """},
        {"role": "user", "content": f"You must provide your reasoning before calling any functions. Given the menu state: '{menu_state}', and the desired action: '{action_description}', please provide the necessary controller inputs not just in your content response but also within your function_call reseponse, use `add_to_q(nums)`."},
    ]

    #try strict = true
    for attempt in range(3):
        # Call OpenAI API
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            functions= [
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
            function_call="auto",  # Allow the model to decide when to call the function
            temperature=0.3  # Lower temperature for deterministic responses
        )
        
        # Extract response components
        # response.choices[0].message.function_call
        choice = response.choices[0].message
        reasoning = choice.content
        function_call = choice.function_call

        # Check if reasoning and function call are present
        if reasoning and function_call:
            # If valid, return the reasoning and function call
            process_action(function_call)
            ret_q = action_queue
            action_queue = []
            return ret_q

        # Debugging info on retries
        print(f"Attempt {attempt + 1} failed: Incomplete response. Retrying...")

    raise ValueError("Model failed to provide both reasoning and function call after 3 attempts")

def process_action(function_call):
    # Process the function call response
    if function_call and function_call.name == "add_to_q":
        arguments = json.loads(function_call.arguments)
        nums = arguments.get("nums")  # Extract the number
        if nums:
            add_to_q(nums)

# Example usage
"""if __name__ == "__main__":
    # Simulate the decision to attack
    action_description = "Larvitar cannot use any move as all moves have 0 current PP."  # Placeholder action
    #menu_state = "║   ║SCRATCH      ║\n║   ║▶LEER         ║\n║   ║RAGE         ║\n║   ║-            ║"  # Current menu state

    menu_state = "║       ║          ║\n ║       ║▶FIGHT PKMN ║\n║       ║          ║\n║       ║ PACK  RUN║"

    
    print("Current action queue:", get_action_queue(action_description, menu_state))"""
