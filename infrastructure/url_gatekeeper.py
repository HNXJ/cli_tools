import urllib.parse

ALLOWED_DOMAINS = {
    "localhost",
    "127.0.0.1",
    "google.com"  # Recursively allows colab.research.google.com, docs, www, etc.
}

def is_url_authorized(target_url: str) -> bool:
    try:
        parsed_url = urllib.parse.urlparse(target_url)
        hostname = parsed_url.hostname
        
        if not hostname: 
            return False
            
        # Exact match
        if hostname in ALLOWED_DOMAINS: 
            return True
            
        # Subdomain match
        for domain in ALLOWED_DOMAINS:
            if hostname.endswith("." + domain): 
                return True
                
        return False
        
    except Exception as e:
        print(f"[SECURITY ERROR] Parse Failed: {e}")
        return False
