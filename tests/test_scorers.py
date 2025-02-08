import pytest
from src.scorers.format import FormatScorer

def test_format_scorer():
    scorer = FormatScorer()
    
    # Test case 1: No tags
    assert scorer.score("Hello, world!") == 0
    
    # Test case 2: Only think tags
    assert scorer.score("<think>Thinking</think>Some text") == 0
    
    # Test case 3: All tags present
    text = "<think>Thought process</think><answer>The punchline</answer>"
    assert scorer.score(text) == 1
    
    # Test case 4: Missing closing tag
    assert scorer.score("<think>Thought<answer>Punchline</answer>") == 0

    # Test case 5: Missing opening tag
    assert scorer.score("Some text<answer>Punchline</answer>") == 0

    # Test case 6: Missing closing tag
    assert scorer.score("<think>Thought<answer>Punchline") == 0

    # Test case 7: Overlapping tags
    assert scorer.score("<think>Thought<answer>Punchline</think></answer>") == 0

    # Test case 8: Overlapping tags
    assert scorer.score("<think>Thought<answer>Punchline</answer></think>") == 0


def run_tests():
    pytest.main(['tests'])
