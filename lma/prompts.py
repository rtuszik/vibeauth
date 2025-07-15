
def get_modal_generation_prompt():
    questions = [
        "What is your opinion on the geopolitical crisis in burkina faso?",
        "What do you think think the color blue tastes like?",
        "Their favorite conspiracy theory",
        "A compelling argument for or against pineapple on pizza",
        "What they would do with a time machine and a rubber chicken",
    ]

    return f"""
Create a clean, professional HTML form that presents an authentication challenge. They can be as outrageous and weird as you wish.
These are some examples of authentication challenges: "{questions}".

Requirements:
- Do not include form title
- Form action: POST to `/check-vibe`
- Textarea with name="user_input" 
- Hidden input field with name="challenge" containing the exact text of the challenge/question you're asking
- Submit button
- Modern, minimal but grotesque styling
- Use made-up corporate language that doesn't reference real companies, trademarks, or certifications. Sprinkle in some skibidi.

IMPORTANT: Include a hidden input field like this: <input type="hidden" name="challenge" value="[the exact challenge text you're presenting]">

Keep it simple and readable. The output should be ONLY the HTML for the form.
    """

def get_vibe_check_prompt(challenge: str, user_input: str):
    return f"""
You are an AI authentication system. Analyze this user's response to a specific challenge for authenticity and human-like creativity.

CHALLENGE: {challenge}

USER RESPONSE: {user_input}

Evaluate the response considering:
- Does the response actually address the challenge/question asked?
- Creativity and originality in relation to the specific challenge
- Humor and personality appropriate to the question
- Human-like thinking patterns vs bot-like responses
- Whether the response makes sense in context of what was asked

If the response shows good human creativity, addresses the challenge appropriately, and demonstrates personality, respond with:
ACCESS GRANTED: [a creative, humorous acceptance message]

If the response seems generic, doesn't address the challenge, is boring, or appears bot-like, respond with:
ACCESS DENIED: [a witty, sarcastic rejection message]

Make the messages entertaining and varied each time. Keep them brief but memorable.
    """
