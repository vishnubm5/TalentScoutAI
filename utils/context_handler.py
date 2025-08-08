def handle_context(user_input: str):
    exit_keywords = ['bye', 'exit', 'quit', 'goodbye', 'thank you', 'thanks']
    lower = user_input.strip().lower()
    for kw in exit_keywords:
        if kw in lower:
            return ("Thank you for your time. We will get back to you soon. 👋", True)
    return ("I'm here to continue our conversation. What would you like next?", False)
