import httpx
from datetime import datetime


class HLTVClient:
    base_url: str = "https://www.hltv.org/"
    default_headers: dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "DNT": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://www.hltv.org/",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "1"
    }

    @classmethod
    def fetch_page(cls, path: str, **kwargs) -> str:
        """
        Fetches the HTML content of a page given its path.

        Args:
        path (str): The path of the page to fetch.
        **kwargs: Additional keyword arguments to pass to the request.

        Returns:
        str: The HTML content of the page.
        """
        headers = cls.default_headers.copy()
        extra_headers = kwargs.pop("headers", {})
        headers.update(extra_headers)
        url = cls.base_url + path
        try:
            response = httpx.get(url, headers=headers, **kwargs)
            response.raise_for_status()
            return response.text
        except httpx.RequestError as e:
            print(f"An error occurred while requesting {url}: {e}")
            return ""

    @classmethod
    def validate_hltv_url(cls, base_path: str, path: str = "") -> str:
        """
        Validates URLs for the best of the month on HLTV, testing dates from 1 to 30 for the current month.

        Args:
        base_path (str): The base path to be tested.

        Returns:
        str: The most recent valid URL found, or None if no valid URL is found.
        """
        current_date = datetime.now()
        year = current_date.year
        month = current_date.strftime("%B").lower()
        valid_urls = []

        for day in range(1, 31):
            date_path = f"{base_path}/{year}/{month}/{day:02d}/{path}"
            full_url = cls.base_url + date_path
            try:
                response = httpx.get(full_url, headers=cls.default_headers)
                if response.status_code == 200:
                    valid_urls.append(date_path)
            except httpx.RequestError:
                continue

        if valid_urls:
            return valid_urls[-1]  # Return the most recent valid URL

        return ""
