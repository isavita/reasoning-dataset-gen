import re
from .base import BaseScorer

class FormatScorer(BaseScorer):
    def __init__(self):
        super().__init__()
        self.tag_pattern = re.compile(r'(<think>|</think>|<answer>|</answer>)')

    def score(self, text: str) -> int:
        # Extract all tags in the order they appear
        tags = self.tag_pattern.findall(text)
        # Define the required exact sequence of tags
        required_sequence = ['<think>', '</think>', '<answer>', '</answer>']
        # Check if the extracted tags match the required sequence exactly
        return 1 if tags == required_sequence else 0
