
import sys
from unittest.mock import MagicMock, patch

# Mock rich stuff to avoid UI clutter during test
sys.modules['rich.console'] = MagicMock()
sys.modules['rich.panel'] = MagicMock()
sys.modules['rich.prompt'] = MagicMock()
sys.modules['rich.table'] = MagicMock()
sys.modules['rich.layout'] = MagicMock()
sys.modules['rich.markdown'] = MagicMock()

# Now import our modules
from core.engine import ModelEngine
from core.config import ConfigManager
from interface.cli import UI

def test_fetch_and_select():
    print("Testing fetch and select logic...")
    config = MagicMock()
    engine = ModelEngine(config)
    
    # Mock specific gpt4all result
    mock_models = [
        {'name': 'Test Model', 'filename': 'test.gguf', 'ramrequired': '4', 'parameters': '7B'},
        {'name': 'Another Model', 'filename': 'another.gguf', 'ramrequired': '8', 'parameters': '13B'}
    ]
    
    with patch('core.engine.GPT4All.list_models', return_value=mock_models):
        models = engine.fetch_available_models()
        print(f"Fetched {len(models)} models.")
        assert len(models) == 2
        
    print("Testing UI selection logic...")
    # Test valid selection
    with patch('rich.prompt.Prompt.ask', return_value="1"):
        # We need to mock console.print to not crash
        with patch('interface.cli.console.print') as mock_print:
             selected = UI.show_model_selection(models)
             print(f"Selected: {selected}")
             assert selected == 'test.gguf'
             
    # Test picking "back"
    with patch('rich.prompt.Prompt.ask', return_value="back"):
         selected = UI.show_model_selection(models)
         print(f"Selected: {selected}")
         assert selected is None
         
    print("Tests passed!")

if __name__ == "__main__":
    test_fetch_and_select()
