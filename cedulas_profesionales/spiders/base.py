from logging import ERROR
import re
from scrapy import Spider
from scrapy.http import Request
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
from scrapy.spidermiddlewares.httperror import HttpError

class BaseSpider(Spider):
    name = "main"

    def __init__(self, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)
        self.results = None

    def errback_httpbin(self, failure):
        """Manage all network failures."""
        self.log(f"error: {repr(failure)}", level=ERROR)
        error_message = ""

        if failure.check(HttpError):
            response = failure.value.response
            error_message = f"HttpError {response.status} on {response.url}"
            self.log(error_message, level=ERROR)
        elif failure.check(DNSLookupError):
            request = failure.request
            error_message = f"DNSLookupError on {request.url}"
            self.log(error_message, level=ERROR)
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            error_message = f"TimeoutError on {request.url}"
            self.log(error_message, level=ERROR)
        else:
            request = failure.request
            error_message = f"MaxRetryError on {request.url}"
            self.log(error_message, level=ERROR)

        self.results = error_message

    @staticmethod
    def clean_text(text):
        """Clean extracted text by removing extra spaces and newlines."""
        if text:
            return re.sub(r'\s+', ' ', text).strip()
        return text
