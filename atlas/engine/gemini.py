import os
import json
import urllib.request
import urllib.error
from typing import Optional

class GeminiEngine:
    """A lightweight, zero-dependency client for the Gemini API."""

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.0-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model_name
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

    def ask(self, system_prompt: str, user_prompt: str, json_mode: bool = False) -> str:
        if not self.api_key:
            return "ERROR: GEMINI_API_KEY not configured."
            
        url = f"{self.base_url}/models/{self.model_name}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        
        full_prompt = f"{system_prompt}\n\nUSER TASK: {user_prompt}"
        payload = {
            "contents": [{"parts": [{"text": full_prompt}]}]
        }
        
        if json_mode:
            payload["generationConfig"] = {"response_mime_type": "application/json"}

        req_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=req_data, headers=headers, method="POST")
        
        try:
            with urllib.request.urlopen(req) as response:
                res_body = response.read().decode("utf-8")
                data = json.loads(res_body)
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8")
            return f"Gemini API Error {e.code}: {err_msg}"
        except Exception as e:
            return f"Gemini Client Error: {str(e)}"

DefaultEngine = GeminiEngine()
