import re

class UserAgentWrapper:
    def __init__(self, user_agent: str):
        self.ua = user_agent.casefold()
    def parse_user_agent(self):
        os = "Unknown"
        if "windows" in self.ua :
            os = "Windows"
        elif "linux" in self.ua :
            os = "Linux"
        elif "macos" in self.ua or "mac os" in self.ua:
            os = "MacOS"
        elif "android" in self.ua :
            os = "Android"
        elif "iphone" in self.ua or "iphad" in self.ua:
            os = "iOS"
        browser = "Unknown"
        if "firefox" in self.ua:
            browser = "Firefox"
        elif "chrome" in self.ua:
            browser = "Chrome"
        elif "edge" in self.ua:
            browser = "Edge"
        elif "safari" in self.ua:
            browser = "Safari"
        return {
            "os": os,
            "browser": browser,
            "full": self.ua
        }