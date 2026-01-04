import sys
import os

# Ensure we can import from current dir
sys.path.append(os.getcwd())

from core.config import ConfigManager
from core.personas import PersonaManager

def test_config():
    print("Testing ConfigManager...")
    config = ConfigManager("test_config.yaml")
    assert config.settings.max_tokens == 200
    config.update(max_tokens=500)
    
    # Reload to check persistence
    config2 = ConfigManager("test_config.yaml")
    assert config2.settings.max_tokens == 500
    print("ConfigManager: OK")
    
    # Cleanup
    if os.path.exists("test_config.yaml"):
        os.remove("test_config.yaml")

def test_personas():
    print("Testing PersonaManager...")
    pm = PersonaManager()
    assert "coder" in pm.list_personas()
    p = pm.get_persona("coder")
    assert "expert software engineer" in p.system_prompt
    print("PersonaManager: OK")

if __name__ == "__main__":
    try:
        test_config()
        test_personas()
        print("ALL CHECKS PASSED")
    except Exception as e:
        print(f"FAILED: {e}")
        sys.exit(1)
