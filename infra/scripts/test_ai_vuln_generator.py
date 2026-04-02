import os
import sys
import tempfile
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from infra.scripts import ai_vuln_generator

def test_call_openai_mocked():
    with patch("urllib.request.urlopen") as mock_urlopen:
        # Mock the response
        mock_response = mock_urlopen.return_value.__enter__.return_value
        mock_response.read.return_value = b'{"choices": [{"message": {"content": "mocked_code"}}]}'
        
        result = ai_vuln_generator.call_openai("fake_key", "prompt", "code")
        assert result == "mocked_code"

def test_call_anthropic_mocked():
    with patch("urllib.request.urlopen") as mock_urlopen:
        # Mock the response
        mock_response = mock_urlopen.return_value.__enter__.return_value
        mock_response.read.return_value = b'{"content": [{"text": "mocked_anthropic_code"}]}'
        
        result = ai_vuln_generator.call_anthropic("fake_key", "prompt", "code")
        assert result == "mocked_anthropic_code"

def test_main_no_args():
    with patch("sys.argv", ["ai_vuln_generator.py"]):
        with patch("sys.exit") as mock_exit:
            mock_exit.side_effect = SystemExit
            try:
                ai_vuln_generator.main()
            except SystemExit:
                pass
            mock_exit.assert_called_with(1)

def test_main_no_keys(tmp_path):
    test_file = tmp_path / "test.py"
    test_file.write_text("print('test')")
    
    with patch("sys.argv", ["ai_vuln_generator.py", str(test_file)]):
        with patch.dict("os.environ", {}, clear=True):
            with patch("sys.exit") as mock_exit:
                mock_exit.side_effect = SystemExit
                try:
                    ai_vuln_generator.main()
                except SystemExit:
                    pass
                mock_exit.assert_called_with(0)

def test_main_successful_mutation(tmp_path):
    test_file = tmp_path / "test.py"
    test_file.write_text("original code")
    
    with patch("sys.argv", ["ai_vuln_generator.py", str(test_file)]):
        with patch.dict("os.environ", {"OPENAI_API_KEY": "fake_key"}, clear=True):
            with patch("infra.scripts.ai_vuln_generator.call_openai", return_value="mutated code"):
                ai_vuln_generator.main()
                
    assert test_file.read_text() == "mutated code"
