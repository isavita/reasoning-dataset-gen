import litellm

TIMEOUT = 120
def generate_completion(
    model_name: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.7,
    timeout: int = TIMEOUT
) -> str:
    """Simple wrapper for litellm completion"""
    try:
        response = litellm.completion(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            timeout=timeout,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating completion: {e}")
        return ""
