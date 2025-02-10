from .base import BaseGenerator
from ..utils.llm import generate_completion

class JokeGenerator(BaseGenerator):
    @staticmethod
    def get_system_prompt() -> str:
        return """You are an AI assistant that produces jokes. You should think about the joke first, then produce it.
You should use the <think> tag to think about the joke, and the <answer> tag to produce the joke.
Do not use any other tags or anything else in your response."""

    def generate(self, prompt: str) -> str:
        system_prompt = self.get_system_prompt()
        examples = self._get_examples()
        full_prompt = f"{system_prompt}\n\nExamples:\n{examples}\n\nNow, produce a joke for: {prompt}"
        
        return generate_completion(
            model_name=self.model_name,
            system_prompt=system_prompt,
            user_prompt=full_prompt,
            temperature=self.temperature
        )

    def _get_examples(self) -> str:
        return """Example 1:
Give me a spooky joke about body parts that's not too scary for kids
<think>I want to create anatomy humor. Skeletons are inherently funny because they're literal "bare bones." What do they lack? Flesh/organs. "Guts" has a double meaning - both literal organs and figurative courage. This sets up a pun opportunity.</think>
<answer>Why don't skeletons fight each other? They don't have the guts!</answer>

Example 2:
Make a joke mixing doctors n computers plz? something ironic
<think>Tech support jokes work well with personification. "Doctor" visits imply sickness. Common computer issues include viruses. Let's combine these - a computer catching a "virus" works literally (tech) and metaphorically (biology). Adds irony since computers are supposed to fix problems, not have them.</think>
<answer>Why did the computer go to the doctor? It had a virus!</answer>

Example 3:
science teacher needs chemistry pun for lesson intro - atoms maybe?
<think>Science humor opportunity. Atoms are fundamental but abstract. "Make up everything" has dual meaning - literal composition vs deception. Personifying atoms as untrustworthy creates surprise. Bonus science nod to their constant motion/making bonds.</think>
<answer>Why don't scientists trust atoms? Because they make up everything!</answer>"""
