from common.entities import Paste
from scraper.common import ScrapePageBase


class PastePageScraper(ScrapePageBase):
    BASE_PASTE_URL = 'https://pastebin.com/'

    def __init__(self, paste_key):
        super().__init__(self.__class__.BASE_PASTE_URL + paste_key)

    def _process_response(self, soup):
        paste = Paste()
        url_tag = soup.find("meta", property="og:url")
        url = url_tag['content'] if url_tag else ''

        url_parts = url.rstrip('/').split('/')
        paste.key = url_parts[-1] if url_parts else ''
        paste.url = url

        user_tag = soup.select(".username a")
        paste.user = user_tag[0].text if user_tag else ''

        date_tag = soup.select(".date span")
        paste.date = date_tag[0]['title'] if date_tag else ''

        title_tag = soup.select(".info-top h1")
        paste.title = title_tag[0].text if title_tag else ''

        paste.content = ''
        for content_title_tag in soup.select(".post-view .content__title"):
            if content_title_tag.text.strip() == "RAW Paste Data":
                content_tag = content_title_tag.find_next_sibling("textarea")
                if content_tag:
                    paste.content = content_tag.text
                break
        return paste

    def _process_post_response(self, paste):
        paste.cleanup()
        return super()._process_post_response(paste)
