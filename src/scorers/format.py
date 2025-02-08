import re
from .base import BaseScorer

class FormatScorer(BaseScorer):
    def __init__(self):
        super().__init__()
        self.think_open = re.compile(r'<think>')
        self.think_close = re.compile(r'</think>')
        self.answer_open = re.compile(r'<answer>')
        self.answer_close = re.compile(r'</answer>')

    def score(self, text: str) -> int:
        if (self.think_open.search(text) and
            self.think_close.search(text) and
            self.answer_open.search(text) and
            self.answer_close.search(text)):
            return 1
        return 0
