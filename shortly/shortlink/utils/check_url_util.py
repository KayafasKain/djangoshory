from urllib.parse import urlparse

def is_valid_url(url):
    parts = urlparse(url)
    return parts.scheme in ('http', 'https')