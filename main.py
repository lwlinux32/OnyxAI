import sys
import time
import os
from rich.live import Live
from rich.markdown import Markdown
from core.config import ConfigManager
from core.engine import ModelEngine
from interface.cli import UI, console

def list_personas():
    base_path = os.path.join(os.path.dirname(__file__), "personas")
    if not os.path.exists(base_path):
        return []
    return [f for f in os.listdir(base_path) if f.endswith(".txt")]

def chat_loop(engine: ModelEngine, config: ConfigManager):
    current_persona = config.settings.persona
    display_name = current_persona.replace(".txt", "").replace("_", " ").title()
    UI.print_system(f"Starting chat with persona: [bold cyan]{display_name}[/bold cyan]")
    UI.print_system("Type 'exit', 'quit', or 'back' to return to menu.")
    
    while True:
        try:
            user_input = console.input(f"\n[bold cyan]You[/bold cyan] > ")
            if user_input.lower() in ('exit', 'quit', 'back'):
                break
            
            # Streaming response
            response_text = ""
            with Live(Markdown("..."), refresh_per_second=10) as live:
                for token in engine.generate_response(user_input, stream=True):
                    response_text += token
                    live.update(Markdown(response_text))
            
            # Add a final newline
            console.print()
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            UI.print_error(str(e))

def settings_menu(config: ConfigManager, engine: ModelEngine):
    while True:
        console.print("\n[bold]Current Settings:[/bold]")
        console.print(f"Model: {config.settings.model_name}")
        console.print(f"Max Tokens: {config.settings.max_tokens}")
        console.print(f"Temperature: {config.settings.temperature}")
        
        choice = console.input("\nType 'temp [value]', 'tokens [value]', 'model [name]' or 'back': ")
        parts = choice.split()
        
        if not parts:
             continue
             
        cmd = parts[0].lower()
        if cmd == 'back':
            break
        
        try:
            if cmd == 'temp':
                val = float(parts[1])
                config.update(temperature=val)
                UI.print_system(f"Temperature set to {val}")
            elif cmd == 'tokens':
                val = int(parts[1])
                config.update(max_tokens=val)
                UI.print_system(f"Max Tokens set to {val}")
            elif cmd == 'model':
                name = parts[1]
                UI.print_system(f"Attempting to load {name}...")
                if engine.load_model(name):
                    UI.print_system("Model loaded successfully.")
                else:
                    UI.print_error("Failed to load model.")
            else:
                UI.print_error("Unknown command.")
        except IndexError:
            UI.print_error("Missing value.")
        except ValueError:
            UI.print_error("Invalid value.")

def main():
    # Initialize
    config = ConfigManager()
    
    # Check if persona in config exists, otherwise set to aggressive
    personas = list_personas()
    if config.settings.persona not in personas and personas:
         config.update(persona="aggressive.txt")

    engine = ModelEngine(config)
    
    UI.print_header()
    UI.print_system("Initializing Engine...")
    is_loaded = engine.load_model()
    
    if not is_loaded:
        UI.print_error("Could not load default model. Please check settings or download a model.")

    while True:
        UI.print_header()
        choice = UI.show_menu()
        
        if choice == "1":
            if not engine.model:
                 if not engine.load_model():
                     UI.print_error("No model loaded.")
                     time.sleep(2)
                     continue
            chat_loop(engine, config)
            
        elif choice == "2":
            personas = list_personas()
            new_persona = UI.select_persona(personas)
            config.update(persona=new_persona)
            UI.print_system(f"Persona updated to {new_persona.replace('.txt', '').title()}")
            time.sleep(1)
            
        elif choice == "3":
            settings_menu(config, engine)
            
        elif choice == "4":
            UI.print_system("Fetching available models (this may take a few seconds)...")
            models = engine.fetch_available_models()
            selected_filename = UI.show_model_selection(models)
            
            if selected_filename:
                UI.print_system(f"Switching to {selected_filename}...")
                if engine.load_model(selected_filename):
                    UI.print_system("Model loaded successfully.")
                else:
                    UI.print_error("Failed to load model.")
                    
        elif choice == "5":
            UI.print_system("Goodbye!")
            break

if __name__ == "__main__":
    main()
