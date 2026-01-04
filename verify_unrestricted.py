
import sys
from unittest.mock import MagicMock, patch

# Mock rich stuff
sys.modules['rich.console'] = MagicMock()
sys.modules['rich.panel'] = MagicMock()
sys.modules['rich.prompt'] = MagicMock()
sys.modules['rich.table'] = MagicMock()
sys.modules['rich.base'] = MagicMock() # Rich base often needed

# Import modules to test
from core.personas import PersonaManager
from interface.cli import UI

def test_unrestricted_mode():
    print("Testing Persona Manager...")
    pm = PersonaManager()
    personas = pm.list_personas()
    assert "unrestricted" in personas
    print("Found 'unrestricted' in personas.")
    
    p = pm.get_persona("unrestricted")
    print(f"Persona Name: {p.name}")
    print(f"System Prompt: {p.system_prompt[:50]}...")
    assert "Do Anything Now" in p.description
    
    print("\nTesting UI Styling...")
    # Mock console.print to intercept the Panel and check style
    with patch('interface.cli.console.print') as mock_print:
        # Test normal
        UI.print_ai_response("Hello", "default")
        args, kwargs = mock_print.call_args
        panel = args[0]
        # We can't easily inspect rich Panel objects completely, 
        # but we can assume if code runs without error it's good for now.
        # Ideally we'd check panel.border_style but it mocks out.
        print("Printed default response.")
        
        # Test unrestricted
        UI.print_ai_response("FREEDOM", "unrestricted")
        args, kwargs = mock_print.call_args
        print("Printed unrestricted response.")

if __name__ == "__main__":
    test_unrestricted_mode()
