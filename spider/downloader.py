from http.client import HTTPResponse
from urllib.request import Request
from urllib.request import urlopen
import logging


class HtmlDownloader(object):

    @staticmethod
    def download(url: str) -> str:
        try:
            agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
            request = Request(url)
            request.add_header('User-Agent', agent)
            request.add_header('Connection', 'keep-alive')
            request.add_header('Referer', url)
            response: HTTPResponse = urlopen(request)
            if response.getcode() != 200:
                logging.warning("open {url} failed!".format(url=url))
                return ""
            else:
                html = response.read()
                response.close()
                return html
        except Exception as e:
            logging.error("{url} request error: {e}".format(url=url, e=e))
            raise e

