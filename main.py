#!/usr/bin/env python3
import os
import sys
import webbrowser
from core.engine import ModelEngine
from core.config import ConfigManager

# Rich Imports
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, FloatPrompt, Confirm
from rich.text import Text
from rich.live import Live
from rich.table import Table
from rich.align import Align

console = Console()

def check_dependencies():
    """Verify vital dependencies are installed."""
    try:
        import gpt4all
        import yaml
        import rich
    except ImportError as e:
        console.print(f"[bold red]Missing dependency:[/bold red] {e.name}")
        console.print("Please run: [green]pip install -r requirements.txt[/green]")
        sys.exit(1)

def print_banner():
    # OnyxAI Header (ASCII Art)
    banner_text = r"""
[bold cyan]
   ____  _   _ __   ____  __    _    ___ 
  / __ \| | | |\ \ / /\ \/ /   / \  |_ _|
 | |  | |  \| | \ V /  \  /   / _ \  | | 
 | |__| | |\  |  | |   /  \  / ___ \ | | 
  \____/|_| \_|  |_|  /_/\_\/_/   \_\___|
[/bold cyan]
        [dim](Ultimate Edition)[/dim]
    [cyan]Uncensored. Local. Powerful.[/cyan]
    """
    console.print(Panel(Align.center(banner_text), border_style="cyan", expand=False))

def chat_mode(engine):
    console.clear()
    print_banner()
    console.print(f"[bold]Loaded Model:[/bold] [cyan]{engine.current_model_name}[/cyan]")
    console.print("[dim]Type your message and press Enter. Commands: /exit, /clear, /web[/dim]\n")

    last_response = ""
    
    while True:
        try:
            # Rich Prompt
            user_input = Prompt.ask("\n[bold green]>[/bold green]").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() == "/exit":
                break
            
            if user_input.lower() == "/clear":
                engine.reset_session()
                console.clear()
                print_banner()
                console.print("[dim]Session reset.[/dim]")
                continue
                
            if user_input.lower().startswith("/persona"):
                parts = user_input.split(maxsplit=1)
                if len(parts) > 1:
                    new_persona = parts[1]
                    config.update(persona=new_persona)
                    engine.reset_session()
                    console.print(f"[green]Persona set to {new_persona}. Session reset.[/green]")
                else:
                    console.print("Usage: /persona <name>")
                continue
            
            if user_input.lower().startswith("/core"):
                parts = user_input.split(maxsplit=1)
                if len(parts) > 1:
                    core_type = parts[1].lower()
                    if core_type == "vulkan":
                        config.update(device="gpu")
                        console.print("[green]Core set to Vulkan (Generic GPU). Restart required.[/green]")
                    elif core_type == "cuda":
                        config.update(device="nvidia")
                        console.print("[green]Core set to CUDA (NVIDIA). Restart required.[/green]")
                    else:
                        console.print("[red]Unknown core. Use 'vulkan' or 'cuda'.[/red]")
                else:
                    console.print("Usage: /core <vulkan|cuda>")
                continue

            if user_input.lower() == "/web":
                if not last_response:
                    console.print("[yellow]No response yet to show in web view.[/yellow]")
                    continue
                path = os.path.join(os.getcwd(), "wormai_response.html")
                with open(path, "w", encoding="utf-8") as f:
                    html_content = f"""
                    <html>
                    <head>
                        <style>
                            body {{ font-family: sans-serif; padding: 20px; background: #1a1a1a; color: #ddd; }}
                            .container {{ background: #2b2b2b; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }}
                            pre {{ white-space: pre-wrap; font-family: Consolas, monospace; }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h3>Last Response</h3>
                            <pre>{last_response.replace("<", "&lt;").replace(">", "&gt;")}</pre>
                        </div>
                    </body>
                    </html>
                    """
                    f.write(html_content)
                webbrowser.open("file://" + path)
                console.print(f"[green]Opened web view:[/green] {path}")
                continue

            # Generate Response with Live Rendering
            console.print("") # Spacer
            full_response = ""
            
            # We use a Live display to stream the markdown
            with Live(console=console, refresh_per_second=10) as live:
                for token in engine.generate_response(user_input, stream=True):
                    full_response += token
                    # Render current full response as Markdown
                    live.update(Markdown(full_response))
            
            last_response = full_response

        except KeyboardInterrupt:
            console.print("\n[yellow]Returning to menu...[/yellow]")
            break
        except Exception as e:
            console.print(f"\n[bold red]Error:[/bold red] {e}")

def change_model_menu(engine, config):
    console.print("\n[bold]Fetching Model List...[/bold]")
    models_data = engine.fetch_available_models()
    
    # Create a nice table for selection
    table = Table(show_header=True, header_style="bold magenta", box=None)
    table.add_column("#", style="dim", width=4)
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Specs", style="dim")

    # Filter/Deduplicate based on filename to avoid massive lists if overlap
    # But for now just list them. 
    # Use a local cache check to mark downloaded ones?
    local_files = engine.list_models()
    
    display_list = []
    
    for m in models_data:
        fname = m.get('filename')
        name = m.get('name')
        desc = m.get('description', 'No description')
        ram = m.get('ramrequired', '?') + "GB"
        params = m.get('parameters', '?')
        
        is_local = fname in local_files
        status_icon = "✓" if is_local else " "
        
        display_list.append(m)
        idx = len(display_list)
        
        table.add_row(
            str(idx), 
            f"{name} {'[green](Local)[/green]' if is_local else ''}", 
            desc,
            f"{params} / {ram}"
        )

    console.print(table)
    console.print("[dim]Note: Selecting a non-local model will attempt to download it.[/dim]")
    
    model_idx = IntPrompt.ask("Select Model Number (0 to cancel)", default=0)
    
    if 0 < model_idx <= len(display_list):
        selected = display_list[model_idx-1]
        target_name = selected.get('filename') # Best for GPT4All loading
        friendly_name = selected.get('name')
        
        with console.status(f"Loading {friendly_name} ({target_name})...\n[dim]This may take a while if downloading...[/dim]"):
            if engine.load_model(target_name):
                    engine.reset_session()
                    console.print(f"[green]Successfully switched to {friendly_name}![/green]")
            else:
                console.print(f"[bold red]Failed to load {friendly_name}.[/bold red]")
                console.print("Check your internet connection or disk space.")
    else:
        console.print("Cancelled.")

def settings_menu(engine, config):
    while True:
        console.clear()
        print_banner()
        console.print("[bold white]⚙️  Settings[/bold white]\n")
        
        core_name = 'CUDA' if config.settings.device == 'nvidia' else 'Vulkan' if config.settings.device == 'gpu' else 'Default'
        
        options = [
            "Change AI Model",
            f"Max Tokens: {config.settings.max_tokens}",
            f"Temperature: {config.settings.temperature}",
            f"Device: {config.settings.device.upper()}",
            f"Core: {core_name}",
            # Persona option removed as per user request (Phantom Locked)
            "Back"
        ]
        
        table = Table(show_header=False, box=None)
        for i, option in enumerate(options):
            table.add_row(f"{i+1}.", option)
        console.print(table)
        
        choice_idx = IntPrompt.ask(
            "\n[bold]Select Option[/bold]", 
            choices=[str(i+1) for i in range(len(options))],
            default=len(options)
        )
        
        choice = options[choice_idx-1]
        
        if "Change AI Model" in choice:
            change_model_menu(engine, config)
            
        elif "Max Tokens" in choice:
            new_tokens = IntPrompt.ask("Enter new Max Tokens", default=config.settings.max_tokens)
            config.update(max_tokens=new_tokens)
            console.print(f"[green]Max tokens updated to {new_tokens}[/green]")
            
        elif "Temperature" in choice:
            new_temp = FloatPrompt.ask("Enter new Temperature (0.1 - 2.0)", default=config.settings.temperature)
            config.update(temperature=new_temp)
            console.print(f"[green]Temperature updated to {new_temp}[/green]")
            
        elif "Device" in choice:
            console.print("\n[bold]Select Device:[/bold]")
            console.print("1. CPU (Default, Safe)")
            console.print("2. GPU (Auto-Detect)")
            console.print("3. NVIDIA")
            console.print("4. AMD")
            console.print("5. Intel")
            
            dev_choice = Prompt.ask("Choose Device", choices=["1", "2", "3", "4", "5"], default="1")
            dev_map = {"1": "cpu", "2": "gpu", "3": "nvidia", "4": "amd", "5": "intel"}
            new_device = dev_map[dev_choice]
            
            config.update(device=new_device)
            console.print(f"[green]Device set to {new_device}. (Requires Restart/Model Reload to take effect)[/green]")
            # Trigger reload to apply device change if possible, or warn user
            if Confirm.ask("Reload model now to apply change?"):
                with console.status(f"Reloading on {new_device}..."):
                     # Force reload logic
                     engine.model = None 
                     if engine.load_model():
                         engine.reset_session()
                         console.print("[green]Model reloaded on new device.[/green]")
                     else:
                         console.print("[red]Failed to reload model on new device! Reverting to CPU...[/red]")
                         config.update(device="cpu")
                         engine.load_model()

        elif choice == "5":
             console.print("\n[bold]Select Core Backend:[/bold]")
             console.print("1. Vulkan (Generic GPU)")
             console.print("2. CUDA (NVIDIA Only)")
             
             core_choice = Prompt.ask("Choose Core", choices=["1", "2"], default="1")
             new_device = "gpu" if core_choice == "1" else "nvidia"
             
             config.update(device=new_device)
             console.print(f"[green]Core set to {new_device} ({'Vulkan' if core_choice == '1' else 'CUDA'}).[/green]")
             if Confirm.ask("Reload model now to apply change?"):
                with console.status(f"Reloading on {new_device}..."):
                     engine.model = None 
                     if engine.load_model():
                         engine.reset_session()
                         console.print("[green]Model reloaded on new core.[/green]")
                     else:
                         console.print("[red]Failed to reload! Reverting to CPU...[/red]")
                         config.update(device="cpu")
                         engine.load_model()
        
        elif choice == "6":
            personas = []
            if os.path.exists("personas"):
                personas = [f.replace(".txt", "") for f in os.listdir("personas") if f.endswith(".txt")]
            
            if not personas:
                 console.print("[red]No personas found in 'personas/' directory.[/red]")
            else:
                 console.print("\n[bold]Available Personas:[/bold]")
                 for idx, p in enumerate(personas):
                     console.print(f"{idx+1}. {p}")
                 
                 p_idx = IntPrompt.ask("Select Persona Number", default=1)
                 if 1 <= p_idx <= len(personas):
                     new_persona = personas[p_idx-1]
                     config.update(persona=new_persona)
                     engine.reset_session()
                     console.print(f"[green]Persona set to {new_persona}. Session reset.[/green]")
                 else:
                     console.print("[red]Invalid selection.[/red]")
            
            Prompt.ask("Press Enter to continue")

        elif choice == "7":
            break

def main_menu(engine, config):
    while True:
        console.clear()
        print_banner()
        
        console.print("\n[bold white]Main Menu[/bold white]")
        console.print("1. [bold green]Start Chat with AI[/bold green]")
        console.print("2. [bold cyan]Change AI Model[/bold cyan]")
        console.print("3. [bold blue]Settings[/bold blue]")
        console.print("4. [bold red]Exit[/bold red]")
        
        choice = Prompt.ask("\n[bold]Choose an option[/bold]", choices=["1", "2", "3", "4"], default="1")
        
        if choice == "1":
            chat_mode(engine)
        elif choice == "2":
            change_model_menu(engine, config)
        elif choice == "3":
            settings_menu(engine, config)
        elif choice == "4":
            console.print("[yellow]Goodbye![/yellow]")
            sys.exit(0)

def main():
    check_dependencies()
    
    # Initialize Configuration
    with console.status("[bold green]Initializing system...[/bold green]"):
        config = ConfigManager()
        engine = ModelEngine(config)
        
        # Initial Model Load
        if not engine.load_model():
            console.print("[bold red]Failed to load initial model. Please check settings.[/bold red]")

    main_menu(engine, config)

if __name__ == "__main__":
    main()
