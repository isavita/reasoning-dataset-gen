from .base import BaseGenerator
from ..utils.llm import generate_completion

class EthicalDilemmaGenerator(BaseGenerator):
    def __init__(self, model_name: str, temperature: float = 0.3):
        super().__init__(model_name, temperature)

    @staticmethod
    def get_system_prompt() -> str:
        return """You are an expert in ethical reasoning. For each scenario:
1. First THINK deeply about:
   - Multiple philosophical frameworks
   - Stakeholder perspectives
   - Cultural contexts
   - Practical implications
   - Long-term consequences
2. Then provide an ANSWER that:
   - Balances competing interests
   - Offers practical guidance
   - Acknowledges complexity
   - Suggests implementation steps
Always use:
<think> for your analysis process in step by step thinking
<answer> for your reasoned response"""

    @staticmethod
    def _generate_prompt_with_examples(scenario: str) -> str:
        examples = """Example 1:
A self-driving car must choose between hitting an elderly pedestrian or swerving into a wall, endangering its passenger.
<think>
The self-driving car dilemma involves:
- Life value comparison (elderly vs passenger)
- Programmed ethics implications
- Legal liability considerations
- Cultural values around age
- Public trust in AI systems
- Direct vs indirect harm
Analyzing through multiple frameworks to balance competing rights and consequences.
</think>
<answer>
In this self-driving car scenario, we must balance individual rights with collective safety. While utilitarian calculations might favor protecting the passenger, this ignores fundamental human rights and could erode public trust in autonomous systems. A nuanced approach would:
1. Prioritize collision avoidance systems to prevent such binary choices
2. Implement transparent decision frameworks that respect all human life equally
3. Consider shared responsibility between manufacturers, users, and society
The solution lies not in choosing between lives, but in developing systems that better protect everyone.
</answer>

Example 2:
A hospital must decide between allocating limited resources to emergency COVID care for elderly patients or vaccination programs for children.
<think>
Vaccination prioritization involves:
- Present vs future harm prevention
- Individual vs collective good
- Healthcare resource allocation
- Demographic impact analysis
- Long-term public health strategy
- Social trust maintenance
Examining both immediate and long-term consequences while considering equity.
</think>
<answer>
The hospital's resource allocation challenge requires balancing immediate critical care with preventive measures. While treating current patients has urgency and visibility, vaccination programs offer greater long-term benefit. A balanced approach would:
1. Establish clear, transparent prioritization criteria
2. Maintain minimum critical care capacity
3. Implement rolling vaccination programs
This preserves both immediate care ethics and public health goals while maintaining healthcare system credibility.
</answer>

Example 3:
A social media platform must decide whether to ban political misinformation at the risk of being accused of censorship and bias.
<think>
Platform moderation ethics involve:
- Free speech vs harm prevention
- Democratic discourse integrity
- Corporate responsibility scope
- Global cultural differences
- Power dynamics in information control
- Technical feasibility of fair enforcement
Balancing societal good with individual rights and practical constraints.
</think>
<answer>
The platform's content moderation challenge requires careful balance between protecting democratic discourse and respecting free expression. A comprehensive approach should:
1. Develop clear, transparent content guidelines
2. Implement graduated response systems
3. Establish independent oversight
4. Provide appeal mechanisms
This protects discourse integrity while maintaining platform neutrality and user trust.
</answer>"""
        return f"""You are an ethics analysis AI. For each ethical dilemma:
1. Use <think> tags to analyse:
   - Key stakeholders
   - Ethical principles involved
   - Cultural considerations
   - Short and long-term impacts
   - Competing values
2. Use <answer> tags to provide:
   - Balanced reasoning
   - Practical considerations
   - Nuanced recommendations
   - Implementation suggestions
Examples:
{examples}
Now, analyse this scenario:
{scenario}"""
    
    def generate(self, prompt: str) -> str:
        system_prompt = self.get_system_prompt()
        user_prompt = self._generate_prompt_with_examples(prompt)
        return generate_completion(
            model_name=self.model_name,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=self.temperature
        )
