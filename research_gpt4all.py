
import gpt4all
from gpt4all import GPT4All
import inspect
import json

# Check generic functions in the module
print("\nModule attributes:")
for name, obj in inspect.getmembers(gpt4all):
    if not name.startswith("_") and inspect.isfunction(obj):
        print(f" - {name}")

# Check GPT4All class methods
print("\nGPT4All class methods:")
for name, obj in inspect.getmembers(GPT4All):
    if not name.startswith("_") and (inspect.isfunction(obj) or inspect.ismethod(obj)):
        print(f" - {name}")

# Try to find model list mechanism
print("\nTrying list_models:")
try:
    models = GPT4All.list_models()
    # It usually returns a list of dictionaries
    if models and len(models) > 0:
        print("First model sample:", models[0])
    else:
        print("Models list is empty or None")
except Exception as e:
    print(f"GPT4All.list_models() failed: {e}")

