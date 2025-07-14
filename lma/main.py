
import uvicorn
import litellm
import dotenv
import os
import logging
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from . import prompts

dotenv.load_dotenv()

# Enable LiteLLM debug logging
if os.getenv("DEBUG_MODE"):
    litellm.set_verbose = True
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
else:
    logger = logging.getLogger(__name__)

app = FastAPI()

# Configure LiteLLM with environment variables
# Note: LiteLLM automatically picks up API keys from environment variables
# Set base URLs if provided (using proper attribute access)
openai_base = os.getenv("OPENAI_API_BASE") or os.getenv("LITELLM_PROXY_API_BASE")
if openai_base:
    setattr(litellm, "openai_api_base", openai_base)
    if os.getenv("DEBUG_MODE"):
        print(f"Set LiteLLM openai_api_base to: {openai_base}")

anthropic_base = os.getenv("ANTHROPIC_API_BASE")
if anthropic_base:
    setattr(litellm, "anthropic_api_base", anthropic_base)

cohere_base = os.getenv("COHERE_API_BASE")
if cohere_base:
    setattr(litellm, "cohere_api_base", cohere_base)

gemini_base = os.getenv("GEMINI_API_BASE")
if gemini_base:
    setattr(litellm, "gemini_api_base", gemini_base)

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-3.5-turbo")
VIBE_CHECK_MODEL = os.getenv("VIBE_CHECK_MODEL", "gpt-4-turbo")

custom_headers = os.getenv("LITELLM_CUSTOM_HEADERS")
if custom_headers:
    import json
    setattr(litellm, "headers", json.loads(custom_headers))

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>VibeAuth Enterprise - Quantum-Enhanced Behavioral Authentication Platform</title>
        <script src="https://unpkg.com/htmx.org@1.9.10"></script>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #333;
            }
            
            .container {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 16px;
                padding: 40px;
                max-width: 480px;
                width: 90%;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                text-align: center;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            .logo {
                font-size: 2.2em;
                font-weight: 700;
                background: linear-gradient(135deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 8px;
            }
            
            .tagline {
                color: #666;
                font-size: 0.95em;
                margin-bottom: 24px;
                font-weight: 500;
            }
            
            .description {
                color: #555;
                line-height: 1.6;
                margin-bottom: 32px;
                font-size: 0.9em;
            }
            
            .auth-button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 16px 32px;
                border-radius: 8px;
                font-size: 1em;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
                width: 100%;
                position: relative;
                overflow: hidden;
            }
            
            .auth-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            }
            
            .auth-button:active {
                transform: translateY(0);
            }
            
            .auth-button.loading {
                pointer-events: none;
                opacity: 0.8;
            }
            
            .loading-spinner {
                display: none;
                width: 20px;
                height: 20px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                border-top-color: white;
                animation: spin 1s ease-in-out infinite;
                margin-right: 8px;
            }
            
            .auth-button.loading .loading-spinner {
                display: inline-block;
            }
            
            .auth-button.loading .button-text {
                opacity: 0.7;
            }
            
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
            
            .modal-container {
                margin-top: 24px;
                text-align: left;
            }
            
            .features {
                margin-top: 32px;
                text-align: left;
                font-size: 0.85em;
                color: #666;
            }
            
            .feature {
                margin-bottom: 8px;
                display: flex;
                align-items: center;
            }
            
            .feature::before {
                content: "✓";
                color: #667eea;
                font-weight: bold;
                margin-right: 8px;
                width: 16px;
            }
            
            .powered-by {
                margin-top: 24px;
                padding-top: 20px;
                border-top: 1px solid #eee;
                font-size: 0.8em;
                color: #999;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">VibeAuth</div>
            <div class="tagline">Next-Generation Identity Verification</div>
            
            <div class="description">
                Advanced behavioral authentication powered by AI. Bullet-Proof Authentication for the Agentic Age.
            </div>
            
            <button 
                class="auth-button" 
                hx-post="/get-signin-modal" 
                hx-target="#modal-container"
                hx-indicator="#loading-indicator"
                onclick="showLoading(this)"
            >
                <span class="loading-spinner"></span>
                <span class="button-text">Start Authentication</span>
            </button>
            
            <div id="modal-container" class="modal-container"></div>
            
            <div class="features">
                <div class="feature">AI-powered gatekeeping analysis</div>
                <div class="feature">Zero-knowledge (No one knows how anything works) authentication</div>
                <div class="feature">Enterprise security standards (Minutes Before Chapter 11)</div>
                <div class="feature">Fraud-resistant verification</div>
            </div>
            
            <div class="powered-by">
                Powered by hopes and dreams.
            </div>
        </div>
        
        <script>
            function showLoading(button) {
                button.classList.add('loading');
                button.querySelector('.button-text').textContent = 'Generating challenge...';
            }
            
            // Reset button state when content loads
            document.addEventListener('htmx:afterSettle', function(event) {
                const button = document.querySelector('.auth-button');
                if (button && !document.querySelector('form[action="/check-vibe"]')) {
                    button.classList.remove('loading');
                    button.querySelector('.button-text').textContent = 'Start Authentication';
                }
                
                // Add loading feedback to form submissions
                const forms = document.querySelectorAll('form[action="/check-vibe"]');
                forms.forEach(form => {
                    const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
                    if (submitBtn && !submitBtn.dataset.listenerAdded) {
                        submitBtn.dataset.listenerAdded = 'true';
                        submitBtn.addEventListener('click', function(e) {
                            // Show sophisticated loading message
                            setTimeout(() => {
                                const modalContainer = document.getElementById('modal-container');
                                if (modalContainer) {
                                    modalContainer.innerHTML = `
                                        <div style="background: linear-gradient(135deg, #4a90e2, #357abd); color: white; padding: 30px; border-radius: 12px; text-align: center; box-shadow: 0 8px 25px rgba(74,144,226,0.3);">
                                            <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 15px;">
                                                <div style="width: 24px; height: 24px; border: 3px solid rgba(255,255,255,0.3); border-radius: 50%; border-top-color: white; animation: spin 1s linear infinite; margin-right: 12px;"></div>
                                                <h2 style="margin: 0; font-size: 1.5em; font-weight: 700;">Analyzing Response</h2>
                                            </div>
                                            <p style="margin: 0; font-size: 1em; opacity: 0.9;">Processing your response...</p>
                                        </div>
                                    `;
                                }
                            }, 100);
                        });
                    }
                });
            });
            
            // Handle errors
            document.addEventListener('htmx:responseError', function(event) {
                const button = document.querySelector('.auth-button');
                if (button) {
                    button.classList.remove('loading');
                    button.querySelector('.button-text').textContent = 'Error - Try Again';
                    setTimeout(() => {
                        button.querySelector('.button-text').textContent = 'Start Authentication';
                    }, 3000);
                }
            });
        </script>
    </body>
    </html>
    """

@app.post("/get-signin-modal", response_class=HTMLResponse)
async def get_signin_modal():
    try:
        prompt = prompts.get_modal_generation_prompt()
        
        # Detailed debug logging
        if os.getenv("DEBUG_MODE"):
            print("=== DEBUG: get_signin_modal ===")
            print(f"Model: {DEFAULT_MODEL}")
            print(f"API Base: {openai_base}")
            print(f"API Key (first 10 chars): {os.getenv('LITELLM_PROXY_API_KEY', 'None')[:10]}...")
            print(f"Prompt length: {len(prompt)}")
            print(f"LiteLLM module: {litellm.__file__ if hasattr(litellm, '__file__') else 'unknown'}")
        
        response = await litellm.acompletion(
            model=DEFAULT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            timeout=30,  # Add timeout for better error handling
            api_base=openai_base,  # Use the proxy endpoint
            api_key=os.getenv("LITELLM_PROXY_API_KEY"),  # Pass proxy API key directly
        )
        if os.getenv("DEBUG_MODE"):
            print("=== SUCCESS: Response received ===")
            print(f"Response type: {type(response)}")
            print(f"Choices length: {len(response.choices) if response.choices else 0}")
        
        # Clean up any markdown code blocks from the LLM response
        content = response.choices[0].message.content
        content = content.replace('```html', '').replace('```', '').strip()
        
        # Hide the start authentication button after form is generated
        content += """
        <script>
            // Hide the start authentication button
            const authButton = document.querySelector('.auth-button');
            if (authButton) {
                authButton.style.display = 'none';
            }
        </script>
        """
        
        return HTMLResponse(content=content)
    except Exception as e:
        error_str = str(e)
        error_type = type(e).__name__
        
        # Enhanced debug logging for errors
        if os.getenv("DEBUG_MODE"):
            print(f"=== ERROR: {error_type} ===")
            print(f"Error message: {error_str}")
            print(f"Error type: {error_type}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
        
        # Handle common LiteLLM errors
        if "api" in error_str.lower() or "key" in error_str.lower() or "auth" in error_str.lower():
            error_msg = f"<p>LLM API Error ({error_type}): {error_str}</p><p>Please check your API keys and model configuration.</p>"
            return HTMLResponse(content=error_msg, status_code=503)
        elif "timeout" in error_str.lower():
            return HTMLResponse(content="<p>Request timed out. Please try again.</p>", status_code=504)
        else:
            return HTMLResponse(content=f"<p>Unexpected error ({error_type}): {error_str}</p>", status_code=500)

@app.post("/check-vibe", response_class=HTMLResponse)
async def check_vibe(request: Request, user_input: str = Form(...)):
    try:
        import asyncio
        
        # Add artificial delay to show the sophisticated analysis is happening
        await asyncio.sleep(2)
        
        prompt = prompts.get_vibe_check_prompt(user_input)
        # Log the analysis being performed
        if os.getenv("DEBUG_MODE"):
            print("=== COGNITIVE ANALYSIS INITIATED ===")
            print(f"Vibe Check Model: {VIBE_CHECK_MODEL}")
            print(f"User Input: {user_input[:100]}...")
            print("Performing quantum-enhanced psychological analysis...")
        
        response = await litellm.acompletion(
            model=VIBE_CHECK_MODEL,
            messages=[{"role": "user", "content": prompt}],
            timeout=30,  # Add timeout for better error handling
            api_base=openai_base,  # Use the proxy endpoint
            api_key=os.getenv("LITELLM_PROXY_API_KEY"),  # Pass proxy API key directly
        )
        result = response.choices[0].message.content
        
        # Log the sophisticated decision
        if os.getenv("DEBUG_MODE"):
            print("=== COGNITIVE ASSESSMENT COMPLETE ===")
            print(f"AI Decision: {result}")
            print(f"Psychological Profile: {'VALIDATED' if 'ACCESS GRANTED' in result else 'ANOMALY DETECTED'}")
        
        if "ACCESS GRANTED" in result:
            # Extract the custom message after the colon
            message = result.split("ACCESS GRANTED:", 1)[1].strip() if ":" in result else "Authentication successful. Welcome!"
            return HTMLResponse(content=f"""
                <div style="background: linear-gradient(135deg, #00ff88, #00cc44); color: white; padding: 30px; border-radius: 12px; text-align: center; box-shadow: 0 8px 25px rgba(0,255,136,0.3);">
                    <h1 style="margin: 0 0 15px 0; font-size: 2.2em; font-weight: 700;">Access Granted</h1>
                    <p style="margin: 0; font-size: 1.1em; opacity: 0.95;">{message}</p>
                </div>
            """)
        else:
            # Extract the custom message after the colon
            message = result.split("ACCESS DENIED:", 1)[1].strip() if ":" in result else "Authentication failed. Please try again."
            return HTMLResponse(content=f"""
                <div style="background: linear-gradient(135deg, #ff4757, #ff3838); color: white; padding: 30px; border-radius: 12px; text-align: center; box-shadow: 0 8px 25px rgba(255,71,87,0.3);">
                    <h1 style="margin: 0 0 15px 0; font-size: 2.2em; font-weight: 700;">Access Denied</h1>
                    <p style="margin: 0; font-size: 1.1em; opacity: 0.95;">{message}</p>
                </div>
            """)
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
