import os
import uvicorn
import litellm
import dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from . import prompts

dotenv.load_dotenv()

app = FastAPI()

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
        response = await litellm.acompletion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return HTMLResponse(content=response.choices[0].message.content)
    except Exception as e:
        return HTMLResponse(content=f"<p>Error generating modal: {e}</p>")

@app.post("/check-vibe", response_class=HTMLResponse)
async def check_vibe(request: Request, user_input: str = Form(...)):
    try:
        prompt = prompts.get_vibe_check_prompt(user_input)
        response = await litellm.acompletion(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        result = response.choices[0].message.content
        if "ACCESS GRANTED" in result:
            return HTMLResponse(content="<h1>Vibe Check: PASSED</h1><p>Welcome, fellow traveler.</p>")
        else:
            return HTMLResponse(content="<h1>Vibe Check: FAILED</h1><p>Your vibe is off. Try again later.</p>")
    except Exception as e:
        return HTMLResponse(content=f"<p>Error checking vibe: {e}</p>")

def run():
    uvicorn.run(app, host="0.0.0.0", port=6969)
