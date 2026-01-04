from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.layout import Layout
from rich import print as rprint
from rich.markdown import Markdown

console = Console()

class UI:
    @staticmethod
    def print_header():
        console.clear()
        title = """[bold red]
██     ██  ██████  ██████  ███    ███      ██████  ██████  ████████ 
██     ██ ██    ██ ██   ██ ████  ████     ██       ██   ██    ██    
██  █  ██ ██    ██ ██████  ██ ████ ██     ██   ███ ██████     ██    
██ ███ ██ ██    ██ ██   ██ ██  ██  ██     ██    ██ ██         ██    
 ███ ███   ██████  ██   ██ ██      ██      ██████  ██         ██    

       [bold red]WORM GPT[/bold red]
[/bold red]
[bold red]Unrestricted | Powerful | Local[/bold red]
"""
        console.print(Panel(title, border_style="red"))

    @staticmethod
    def show_menu() -> str:
        table = Table(title="Main Menu", box=None)
        table.add_column("Option", style="red", no_wrap=True)
        table.add_column("Description", style="white")

        table.add_row("1", "Chat with AI")
        table.add_row("2", "Change Personality")
        table.add_row("3", "Settings (Model/Params)")
        table.add_row("4", "Fetch New Models")
        table.add_row("5", "Exit")
        
        console.print(table)
        return Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5"], default="1")

    @staticmethod
    def select_persona(personas: list) -> str:
        console.print("\n[bold red]Available Personas:[/bold red]")
        for i, p in enumerate(personas):
            # Clean up name for display (remove .txt extension)
            display_name = p.replace(".txt", "").replace("_", " ").title()
            console.print(f" {i+1}. {display_name}")
        
        choice = Prompt.ask("Select persona", choices=[str(i+1) for i in range(len(personas))])
        return personas[int(choice)-1]

    @staticmethod
    def print_ai_response(content: str, persona_name: str = "default"):
        # Used for block printing. For streaming, we handle it in main loop.
        md = Markdown(content)
        style = "bold red" if persona_name == "unrestricted" else "green"
        title = "AI (UNRESTRICTED)" if persona_name == "unrestricted" else "AI"
        console.print(Panel(md, title=title, border_style=style))

    @staticmethod
    def print_system(msg: str):
        console.print(f"[bold yellow]System:[/bold yellow] {msg}")

    @staticmethod
    def print_error(msg: str):
        console.print(f"[bold red]Error:[/bold red] {msg}")

    @staticmethod
    def show_model_selection(models: list) -> str:
        if not models:
            console.print("[red]No models found.[/red]")
            return None

        # Filter models
        uncensored_models = []
        regular_models = []
        
        all_models = [] # Just to map index back to model

        for m in models:
            name = m.get('name', '')
            desc = m.get('description', '')
            # Simple keyword matching
            if "uncensored" in name.lower() or "uncensored" in desc.lower():
                uncensored_models.append(m)
            else:
                regular_models.append(m)
        
        # Display Uncensored Table
        if uncensored_models:
            console.print("\n[bold red]🔓 Uncensored Models[/bold red]")
            u_table = Table(box=None, show_header=True)
            u_table.add_column("#", style="cyan", no_wrap=True)
            u_table.add_column("Name", style="bold red")
            u_table.add_column("Filename", style="dim")
            u_table.add_column("RAM", style="green")
            
            for m in uncensored_models:
                idx = len(all_models) + 1
                name = m.get('name', 'Unknown')
                filename = m.get('filename', 'Unknown')
                ram = m.get('ramrequired', 'Unknown') + " GB"
                u_table.add_row(str(idx), name, filename, ram)
                all_models.append(m)
            
            console.print(u_table)

        # Display Regular Table
    @staticmethod
    def show_model_selection(models: list) -> str:
        if not models:
            console.print("[red]No models found.[/red]")
            return None

        # Buckets
        categories = {
            "assistants": [],
            "coding": [],
            "uncensored": [],
            "other": []
        }
        
        all_models = [] # Just to map index back to model

        for m in models:
            name = m.get('name', '').lower()
            desc = m.get('description', '').lower()
            
            # Simple keyword matching hierarchy
            if "uncensored" in name or "uncensored" in desc:
                categories["uncensored"].append(m)
            elif any(x in name or x in desc for x in ["code", "coding", "python", "script"]):
                 categories["coding"].append(m)
            elif any(x in name or x in desc for x in ["llama 3", "gemma", "chat", "instruct", "gpt", "assistant"]):
                 categories["assistants"].append(m)
            else:
                categories["other"].append(m)
        
        # Helper to print table
        def print_category_table(title, items, style_color):
            if not items:
                return
            console.print(f"\n[bold {style_color}]{title}[/bold {style_color}]")
            table = Table(box=None, show_header=True)
            table.add_column("#", style="cyan", no_wrap=True)
            table.add_column("Name", style=f"bold {style_color}")
            table.add_column("Filename", style="dim")
            table.add_column("RAM", style="green")
            
            for m in items:
                idx = len(all_models) + 1
                name_str = m.get('name', 'Unknown')
                filename = m.get('filename', 'Unknown')
                ram = m.get('ramrequired', 'Unknown') + " GB"
                table.add_row(str(idx), name_str, filename, ram)
                all_models.append(m)
            console.print(table)

        print_category_table("🤖 Assistants", categories["assistants"], "blue")
        print_category_table("👨‍💻 Coding", categories["coding"], "yellow")
        print_category_table("🔓 Uncensored", categories["uncensored"], "red")
        print_category_table("📦 Other", categories["other"], "white")
        
        choice = Prompt.ask("\nSelect a model number or 'back'", default="back")
        if choice.lower() == 'back':
            return None
            
        try:
            val = int(choice)
            if 1 <= val <= len(all_models):
                return all_models[val-1].get('filename')
            else:
                console.print("[red]Invalid selection.[/red]")
                return None
        except ValueError:
            return None
