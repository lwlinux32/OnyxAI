
from core.engine import ModelEngine
from unittest.mock import MagicMock, patch

def test_extra_models():
    print("Testing Supplementary Models...")
    config = MagicMock()
    engine = ModelEngine(config)
    
    # Mock empty native list
    with patch('core.engine.GPT4All.list_models', return_value=[]):
        models = engine.fetch_available_models()
        print(f"Fetched {len(models)} models (expected > 0 from extras).")
        assert len(models) >= 4
        
        filenames = [m['filename'] for m in models]
        assert 'wizardLM-13B-Uncensored.ggmlv3.q4_0.bin' in filenames
        assert 'nous-hermes-2-mistral-7b.Q4_0.gguf' in filenames
        print("Confirmed extra models are present.")

    # Mock native list colliding with extra
    mock_native = [{'filename': 'nous-hermes-2-mistral-7b.Q4_0.gguf', 'name': 'Native Hermes'}]
    with patch('core.engine.GPT4All.list_models', return_value=mock_native):
        models = engine.fetch_available_models()
        # Should still be >= 4, but 'Native Hermes' should be preserved or duplicates handled
        # My logic was: if extra not in existing, append.
        # So 'Native Hermes' is in existing. The extra 'Nous Hermes' has same filename.
        # So it should NOT append the extra version.
        
        hermes = next(m for m in models if m['filename'] == 'nous-hermes-2-mistral-7b.Q4_0.gguf')
        print(f"Hermes Name: {hermes['name']}") 
        assert hermes['name'] == 'Native Hermes'
        print("Confirmed native models take precedence over extras.")

if __name__ == "__main__":
    test_extra_models()
