#!/usr/bin/env python3
"""
UPMICE INFRASTRUCTURE - brain_core.py
Cognitive Engine Service Layer, Command Sandbox Guards, and EDR Stealth Evaluators.
"""
import os
import json
import httpx
from openai import OpenAI

OLLAMA_UPSTREAM_URL = "http://localhost:11434"
OPENROUTER_URL = "https://openrouter.ai"

class OllamaProxyEngine:
    def __init__(self, model="llama3.2"):
        self.model = model

    async def generate_response(self, system_prompt: str, prompt: str, api_key: str = None) -> str:
        if api_key and api_key != "your_key" and api_key != "":
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {
                "model": "meta-llama/llama-3-8b-instruct:free",
                "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
            }
            async with httpx.AsyncClient(timeout=60.0) as client:
                res = await client.post(OPENROUTER_URL, json=payload, headers=headers)
                return res.json()["choices"][0]["message"]["content"]
        
        # Local fallback simulation tracking rules if off-grid
        return f"[UPMICE Brain Simulation Output]\nProcessed Command: {prompt[:50]}..."

class SecuritySandboxGuard:
    def __init__(self):
        self.blacklist = ["rm -rf /", "mkfs", "dd if=", "shutdown", "reboot", "format"]
        self.allowed_tools = ["msfvenom", "nmap", "sqlmap", "nuclei", "adb", "dirb", "gobuster"]

    def verify_command(self, cmd: str) -> tuple:
        cmd_lower = cmd.lower().strip()
        if any(bad in cmd_lower for bad in self.blacklist):
            return False, "Dangerous keyword detected inside sandbox evaluation."
        return True, "Safe"

class KimiClusterBridge:
    def __init__(self):
        self.api_key = os.getenv("MOONSHOT_API_KEY", "your_api_key_here")
        self.client = OpenAI(api_key=self.api_key, base_url="https://moonshot.cn")

    def deep_research(self, query: str) -> str:
        try:
            completion = self.client.chat.completions.create(
                model="moonshot-v1-8k",
                messages=[{"role": "user", "content": query}]
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"[-] Kimi Bridge unavailable: {e}"

ollama_brain = OllamaProxyEngine()
sandbox_guard = SecuritySandboxGuard()
kimi_bridge = KimiClusterBridge()
