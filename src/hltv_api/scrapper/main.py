import httpx


class HLTVClient:
    base_url: str = "https://www.hltv.org/"
    default_headers: dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "DNT": "1",  # Do Not Track Request Header
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://www.hltv.org/",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "1"
    }

    def fetch_page(self, path: str, **kwargs) -> str:
        headers = self.default_headers.copy()
        extra_headers = kwargs.pop("headers", {})
        headers.update(extra_headers)
        url = self.base_url + path
        response = httpx.get(url, headers=headers, **kwargs)
        response.raise_for_status()  # Raises an exception for HTTP errors
        return response.text
