# Reasoning Quality Dataset Generator

A tool for generating and evaluating AI-generated content with a focus on reasoning quality. Currently supports joke generation and scoring, with an extensible framework for adding new content types.

## Project Structure

```
.
├── src/
│   ├── generators/    # Content generators
│   ├── scorers/       # Quality scorers
│   └── utils/         # Shared utilities
├── tests/             # Test files
├── data/              # Generated datasets
└── notebooks/         # Jupyter notebooks
```

## Quick Start

```python
from src.generators import JokeGenerator
from src.scorers import FormatScorer, JokeScorer

# Initialize
joke_gen = JokeGenerator(model_name="mistral/mistral-small-latest")
format_scorer = FormatScorer()
joke_scorer = JokeScorer(model_name="mistral/mistral-small-latest")

# Generate and score
prompt = "Tell me a programming joke"
response = joke_gen.generate(prompt)
scores = {
    'format': format_scorer.score(response),
    'quality': joke_scorer.score(prompt, response)
}
```

## Running Tests

```bash
pip install pytest
python -m pytest
```

## Adding New Generators/Scorers

1. Create new class in `src/generators/` or `src/scorers/`
2. Inherit from appropriate base class
3. Implement required methods
