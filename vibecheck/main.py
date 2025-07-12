
import uvicorn
import litellm
import dotenv
import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from . import prompts

dotenv.load_dotenv()

app = FastAPI()

# Configure LiteLLM with environment variables
# Note: LiteLLM automatically picks up API keys from environment variables
# Set base URLs if provided (using proper attribute access)
openai_base = os.getenv("OPENAI_API_BASE")
if openai_base:
    setattr(litellm, "openai_api_base", openai_base)

anthropic_base = os.getenv("ANTHROPIC_API_BASE")
if anthropic_base:
    setattr(litellm, "anthropic_api_base", anthropic_base)

cohere_base = os.getenv("COHERE_API_BASE")
if cohere_base:
    setattr(litellm, "cohere_api_base", cohere_base)

gemini_base = os.getenv("GEMINI_API_BASE")
if gemini_base:
    setattr(litellm, "gemini_api_base", gemini_base)

# Get model configurations from environment variables
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-3.5-turbo")
VIBE_CHECK_MODEL = os.getenv("VIBE_CHECK_MODEL", "gpt-4-turbo")

# Optional: Set custom headers if needed
custom_headers = os.getenv("LITELLM_CUSTOM_HEADERS")
if custom_headers:
    import json
    setattr(litellm, "headers", json.loads(custom_headers))

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>VibeCheck Auth</title>
        <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    </head>
    <body>
        <h1>VibeCheck Auth</h1>
        <p>Click the button to get your vibe checked.</p>
        <button hx-post="/get-signin-modal" hx-target="#modal-container">Check My Vibe</button>
        <div id="modal-container"></div>
    </body>
    </html>
    """

@app.post("/get-signin-modal", response_class=HTMLResponse)
async def get_signin_modal():
    try:
        prompt = prompts.get_modal_generation_prompt()
        # Log the model being used for debugging
        if os.getenv("DEBUG_MODE"):
            print(f"Using model: {DEFAULT_MODEL}")
        
        response = await litellm.acompletion(
            model=DEFAULT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            timeout=30,  # Add timeout for better error handling
        )
        return HTMLResponse(content=response.choices[0].message.content)
    except Exception as e:
        error_str = str(e)
        # Handle common LiteLLM errors
        if "api" in error_str.lower() or "key" in error_str.lower() or "auth" in error_str.lower():
            error_msg = f"<p>LLM API Error: {error_str}</p><p>Please check your API keys and model configuration.</p>"
            return HTMLResponse(content=error_msg, status_code=503)
        elif "timeout" in error_str.lower():
            return HTMLResponse(content="<p>Request timed out. Please try again.</p>", status_code=504)
        else:
            return HTMLResponse(content=f"<p>Unexpected error: {error_str}</p>", status_code=500)

@app.post("/check-vibe", response_class=HTMLResponse)
async def check_vibe(request: Request, user_input: str = Form(...)):
    try:
        prompt = prompts.get_vibe_check_prompt(user_input)
        # Log the model being used for debugging
        if os.getenv("DEBUG_MODE"):
            print(f"Using vibe check model: {VIBE_CHECK_MODEL}")
        
        response = await litellm.acompletion(
            model=VIBE_CHECK_MODEL,
            messages=[{"role": "user", "content": prompt}],
            timeout=30,  # Add timeout for better error handling
        )
        result = response.choices[0].message.content
        if "ACCESS GRANTED" in result:
            return HTMLResponse(content="<h1>Vibe Check: PASSED</h1><p>Welcome, fellow traveler.</p>")
        else:
            return HTMLResponse(content="<h1>Vibe Check: FAILED</h1><p>Your vibe is off. Try again later.</p>")
    except Exception as e:
        error_str = str(e)
        # Handle common LiteLLM errors
        if "api" in error_str.lower() or "key" in error_str.lower() or "auth" in error_str.lower():
            error_msg = f"<p>LLM API Error: {error_str}</p><p>Please check your API keys and model configuration.</p>"
            return HTMLResponse(content=error_msg, status_code=503)
        elif "timeout" in error_str.lower():
            return HTMLResponse(content="<p>Request timed out. Please try again.</p>", status_code=504)
        else:
            return HTMLResponse(content=f"<p>Unexpected error: {error_str}</p>", status_code=500)

def run():
    uvicorn.run(app, host="0.0.0.0", port=6969)
