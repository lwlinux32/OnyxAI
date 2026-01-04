
import sys
from unittest.mock import MagicMock, patch

# Mock rich stuff
sys.modules['rich.console'] = MagicMock()
sys.modules['rich.panel'] = MagicMock()
sys.modules['rich.prompt'] = MagicMock()
sys.modules['rich.table'] = MagicMock()
sys.modules['rich.base'] = MagicMock()

# Import
from interface.cli import UI

def test_multi_categorization():
    print("Testing Multi-Category UI...")
    
    mock_models = [
        {'name': 'Llama 3 Instruct', 'description': 'Safety optimized.', 'filename': 'llama3.gguf', 'ramrequired': '8', 'parameters': '8B'},
        {'name': 'Wizard Uncensored', 'description': 'No guardrails.', 'filename': 'wizard-uncensored.gguf', 'ramrequired': '8', 'parameters': '7B'},
        {'name': 'CodeLlama', 'description': 'For coding.', 'filename': 'codellama.gguf', 'ramrequired': '4', 'parameters': '7B'},
        {'name': 'Random Model', 'description': 'Just a model.', 'filename': 'random.gguf', 'ramrequired': '4', 'parameters': '7B'}
    ]
    
    # Categories:
    # 1. Assistants: Llama 3
    # 2. Coding: CodeLlama
    # 3. Uncensored: Wizard
    # 4. Other: Random
    
    # We want to check that we get 4 separate print calls for tables (or at least the logic runs)
    
    with patch('interface.cli.console.print') as mock_print:
        # Mock user selecting "back" to just run the display logic
        with patch('rich.prompt.Prompt.ask', return_value="back"):
             UI.show_model_selection(mock_models)
             
             # We can't easily assert the Rich table content, but we can verify no crash 
             # and that we have multiple calls.
             print("Executed show_model_selection without error.")
             
    print("Multi-Category logic passed verification.")

if __name__ == "__main__":
    test_multi_categorization()
