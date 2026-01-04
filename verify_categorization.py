
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

def test_categorization():
    print("Testing Model Categorization UI...")
    
    mock_models = [
        {'name': 'Llama 3 Instruct', 'description': 'Safety optimized.', 'filename': 'llama3.gguf', 'ramrequired': '8', 'parameters': '8B'},
        {'name': 'Wizard Uncensored', 'description': 'No guardrails.', 'filename': 'wizard-uncensored.gguf', 'ramrequired': '8', 'parameters': '7B'},
        {'name': 'Nous Hermes', 'description': 'Trained on uncensored data.', 'filename': 'hermes.gguf', 'ramrequired': '16', 'parameters': '13B'},
        {'name': 'Code Llama', 'description': 'Coding model.', 'filename': 'codellama.gguf', 'ramrequired': '4', 'parameters': '7B'}
    ]
    
    # We want to see if the table creation is called twice (once for each category)
    # And check if the indices are correct 1..4
    
    with patch('interface.cli.console.print') as mock_print:
        with patch('rich.prompt.Prompt.ask', return_value="2"): # Select Wizard Uncensored (should be #2 probably, or #1 in uncensored list?)
            # Wait, my logic assigns indices sequentially across both lists.
            # Uncensored comes first.
            # 1. Wizard Uncensored
            # 2. Nous Hermes
            # 3. Llama 3
            # 4. Code Llama
            
            selected = UI.show_model_selection(mock_models)
            print(f"User selected #2, which mapped to: {selected}")
            assert selected == 'hermes.gguf' # Should be the second uncensored one
            
        with patch('rich.prompt.Prompt.ask', return_value="3"):
            selected = UI.show_model_selection(mock_models)
            print(f"User selected #3, which mapped to: {selected}")
            assert selected == 'llama3.gguf' # First regular one

    print("Categorization logic passed.")

if __name__ == "__main__":
    test_categorization()
