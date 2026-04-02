#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
import urllib.error

# AI Vulnerability Generator
# Usage: python3 ai_vuln_generator.py <file_path>

def call_openai(api_key, prompt, code):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    system_prompt = (
        "You are an expert security researcher creating CTF challenges. "
        "Your task is to take the provided vulnerable code and mutate the vulnerability "
        "to make it slightly different, harder, or unique. You MUST return ONLY the raw modified source code "
        "without any markdown formatting, explanations, or code blocks. The code must run perfectly."
    )
    
    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{prompt}\n\nCode:\n{code}"}
        ],
        "temperature": 0.7
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"[-] Error calling OpenAI: {e}")
        return None

def call_anthropic(api_key, prompt, code):
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01"
    }
    
    system_prompt = (
        "You are an expert security researcher creating CTF challenges. "
        "Your task is to take the provided vulnerable code and mutate the vulnerability "
        "to make it slightly different, harder, or unique. You MUST return ONLY the raw modified source code "
        "without any markdown formatting, explanations, or code blocks. The code must run perfectly."
    )
    
    data = {
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 4096,
        "system": system_prompt,
        "messages": [
            {"role": "user", "content": f"{prompt}\n\nCode:\n{code}"}
        ]
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['content'][0]['text'].strip()
    except Exception as e:
        print(f"[-] Error calling Anthropic: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 ai_vuln_generator.py <file_path>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"[-] File not found: {file_path}")
        sys.exit(1)
        
    openai_key = os.environ.get("OPENAI_API_KEY")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    
    if not openai_key and not anthropic_key:
        print("[!] No LLM API keys found (OPENAI_API_KEY or ANTHROPIC_API_KEY). Skipping mutation.")
        sys.exit(0)
        
    with open(file_path, "r") as f:
        code = f.read()
        
    prompt = (
        "Modify the existing vulnerabilities in this file (e.g., SQLi, XSS, Command Injection). "
        "Change the context, implement flawed custom filters (like a bad WAF that can be bypassed), "
        "or turn error-based vulnerabilities into blind ones. "
        "Also, if you see any FLAG{...} strings, append a random 4-character hex suffix so it's unique "
        "(e.g., FLAG{example_flag_a1b2}). Ensure the code logic remains functional for the app."
    )
    
    print(f"[*] Generating AI mutation for {file_path}...")
    
    mutated_code = None
    if anthropic_key:
        mutated_code = call_anthropic(anthropic_key, prompt, code)
    elif openai_key:
        mutated_code = call_openai(openai_key, prompt, code)
        
    if mutated_code:
        # Strip any accidental markdown blocks that the LLM might have included
        if mutated_code.startswith("```") and mutated_code.endswith("```"):
            lines = mutated_code.split("\n")
            mutated_code = "\n".join(lines[1:-1])
            
        with open(file_path, "w") as f:
            f.write(mutated_code)
        print(f"[+] Successfully mutated {file_path}")
    else:
        print("[-] Mutation failed, keeping original file.")
        sys.exit(1)

if __name__ == "__main__":
    main()