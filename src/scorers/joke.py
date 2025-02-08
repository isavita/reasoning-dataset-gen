import re
from .base import BaseScorer
from ..utils.llm import generate_completion

class JokeScorer(BaseScorer):
    def __init__(self, model_name: str, temperature: float = 0.3):
        super().__init__(model_name, temperature)

    def score(self, user_prompt: str, assistant_response: str) -> int:
        """Score a joke submission from 0-10"""
        system_prompt = self._get_system_prompt()
        user_message = self._get_prompt_with_examples(user_prompt, assistant_response)
        
        result_text = generate_completion(
            model_name=self.model_name,
            system_prompt=system_prompt,
            user_prompt=user_message,
            temperature=self.temperature
        )
        
        return self._extract_score(result_text)

    def _extract_score(self, result_text: str) -> int:
        """Extract and process the total score"""
        match = re.search(r"Total:\s*([0-9]+(?:\.[0-9]+)?)/10", result_text)
        if not match:
            raise ValueError("Could not extract total score from response")
        
        total_score = float(match.group(1))
        
        # If the total score is 10, subtract 1 to return 9. This is because I don't want to give a score of 10.
        if total_score >= 10:
            total_score = 9.0
        
        return int(round(total_score))

    def _get_system_prompt(self) -> str:
        return """You are a Joke Evaluation Expert. Analyse submissions using:
    
**Scoring Criteria (0-10 Total)**:
1. 🎭 Wordplay (0-3): Pun/double-meaning quality in <answer>
2. 💡 Originality (0-2): Novelty of <think> and <answer>
3. 🎉 Surprise (0-2): Unexpected twist effectiveness
4. 🔗 Relevance (0-3): Alignment with user request

**Submission Format**:
<submission>
<user_prompt>[Original user request]</user_prompt>
<assistant_response>
<think>[Creator's reasoning]</think>
<answer>[Joke text]</answer>
</assistant_response>
</submission>

**Output Format**:
<analysis>[Your evaluation of <think> and <answer> and the relevance to the user prompt]</analysis>
<score>
Wordplay: X/3
Originality: Y/2
Surprise: Z/2
Relevance: W/3
Total: T/10
</score>"""

    def _get_prompt_with_examples(self, user_prompt: str, assistant_response: str) -> str:
        submission = f"""<submission>
<user_prompt>{user_prompt}</user_prompt>
<assistant_response>
{assistant_response}
</assistant_response>
</submission>"""
    
        examples = """Example 1:
<submission>
<user_prompt>Tell me a joke about vegetables</user_prompt>
<assistant_response>
<think>Lettuce sounds like "let us". Party themes often involve wordplay.</think>
<answer>Why did the lettuce win the party contest? Because it was a real head of the celebration!</answer>
</assistant_response>
</submission>
<analysis>Basic "lettuce" pun matches the food request but uses an overused format. <think> shows minimal effort to connect vegetables with celebrations.</analysis>
<score>
Wordplay: 2/3 (simple but functional pun)
Originality: 1/2 (common theme with slight twist)
Surprise: 1/2 (predictable word substitution)
Relevance: 1/3 (tangential connection to vegetables)
Total: 5/10
</score>

Example 2:
<submission>
<user_prompt>Looking for some animal-themed humor - what's your best joke about animals or pets?</user_prompt>
<assistant_response>
<think>Shoes need soles for walking. Therapy helps with loss.</think>
<answer>Why did the shoe need therapy? It lost its sole!</answer>
</assistant_response>
</submission>
<analysis>Irrelevant to user's request. <think> about shoes doesn't connect to requested animal joke.</analysis>
<score>
Wordplay: 1/3
Originality: 0/2
Surprise: 1/2
Relevance: 0/3
Total: 2/10
</score>

Example 3:
<submission>
<user_prompt>yo can u giv me programing joke rn??? need 2 make my team lugh</user_prompt>
<assistant_response>
<think>Combining programming concepts of debugging with literal bugs. Using the dual meaning of 'debug' to create a workplace scenario where debugging takes on a literal meaning.</think>
<answer>Why did the programmer bring a bug to work? Because it was a debug session!</answer>
</assistant_response>
</submission>
<analysis>Good programming context with clever wordplay on 'debug'. The <think> shows clear intention to combine literal and technical meanings. However, the execution is somewhat predictable and follows a common joke structure. The punchline, while relevant, doesn't fully maximize the surprise potential of the setup.</analysis>
<score>
Wordplay: 2/3 (solid use of 'debug' double meaning)
Originality: 1/2 (familiar debugging theme)
Surprise: 1/2 (predictable punchline)
Relevance: 3/3 (directly addresses programming context)
Total: 7/10
</score>

Example 4:
<submission>
<user_prompt>I need a chemistry joke for my science class presentation tomorrow.</user_prompt>
<assistant_response>
<think>Birds are funny when they walk.</think>
<answer>Why did the chicken cross the playground? To get to the other slide!</answer>
</assistant_response>
</submission>
<analysis>Completely misses the mark for a chemistry joke. The <think> shows no connection to chemistry or science, instead defaulting to a generic playground variation of the classic chicken joke. Neither the setup nor punchline attempts to incorporate any chemistry concepts.</analysis>
<score>
Wordplay: 0/3 (no chemistry-related wordplay)
Originality: 0/2 (modifies an overused joke format)
Surprise: 0/2 (predictable playground pun)
Relevance: 0/3 (entirely unrelated to chemistry request)
Total: 0/10
</score>

Example 5:
<submission>
<user_prompt>My kid loves vegetables and jokes. Do you know any veggie jokes that would make them laugh?</user_prompt>
<assistant_response>
<think>Combining asparagus's unique smell effect on urine with workplace humor. Using scientific fact for unexpected professional context. Creating tension between formal meeting setting and biological reality.</think>
<answer>What vegetable holds the shortest workplace meetings? Asparagus, because everyone's in a rush to go!</answer>
</assistant_response>
</submission>
<analysis>Creative integration of asparagus's biological effect into a professional context. The <think> demonstrates sophisticated layering of scientific fact with situational humor. While potentially crude, it cleverly avoids explicit reference while maintaining clear understanding. Original approach to vegetable humor beyond simple puns.</analysis>
<score>
Wordplay: 1/3 (relies more on situation than wordplay)
Originality: 2/2 (unique combination of contexts)
Surprise: 2/2 (unexpected professional setting twist)
Relevance: 1/3 (somewhat forced vegetable connection)
Total: 6/10
</score>"""

        return f"""Evaluate this submission. First analyse <think> and <answer>, then score:

Submission to Evaluate:
{submission}

Follow this structure EXACTLY:
<analysis>Your critique</analysis>
<score>...</score>

Examples of how to evaluate the submission and format your response:
{examples}"""
