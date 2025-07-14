import random

def get_modal_generation_prompt():
    questions = [
        "their opinion on garden gnomes",
        "a haiku about their lunch",
        "what they think the color blue tastes like",
        "their favorite conspiracy theory",
        "a compelling argument for or against pineapple on pizza",
        "what they would do with a time machine and a rubber chicken",
    ]

    question = random.choice(questions)

    return f"""
Create a clean, professional HTML form that presents the authentication challenge: "{question}".

Requirements:
- Form action: POST to `/check-vibe`
- Textarea with name="user_input" 
- Submit button
- Modern, minimal styling
- Include subtle hint that this is fictional AI-powered authentication
- Use made-up corporate language that doesn't reference real companies, trademarks, or certifications

Keep it simple and readable. The output should be ONLY the HTML for the form.
    """

def get_vibe_check_prompt(user_input: str):
    return f"""
You are an AI authentication system. Analyze this user response for authenticity and human-like creativity:

{user_input}

Evaluate for:
- Creativity and originality
- Humor and personality
- Human-like thinking patterns
- Not bot-like or generic

If the response shows good human creativity and personality, respond with:
ACCESS GRANTED: [a creative, humorous acceptance message]

If the response seems generic, boring, or bot-like, respond with:
ACCESS DENIED: [a witty, sarcastic rejection message]

Make the messages entertaining and varied each time. Keep them brief but memorable.
    """
