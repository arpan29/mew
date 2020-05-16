import logging
import requests


class HttpClient(object):
    def __init__(self, timeout=60):
        self.__timeout = timeout

    def set_timeout(self, timeout):
        self.__timeout = timeout
        return self

    def get(self, **kwargs):
        """Sends a GET request.
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        logging.info("GET URL: {url}, HEADERS: {headers}".format(url=kwargs.get("url", ""), headers=kwargs.get("headers", "")))
        kwargs["timeout"] = self.__timeout
        r = requests.get(**kwargs)
        r.raise_for_status()
        return r

    def delete(self, **kwargs):
        """Sends a DELETE request.
        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        logging.info("DELETE URL: {url}, HEADERS: {headers}".format(url=kwargs.get("url", ""), headers=kwargs.get("headers", "")))
        kwargs["timeout"] = self.__timeout
        r = requests.delete(**kwargs)
        r.raise_for_status()
        return r

    def post(self, **kwargs):
        """Sends a POST request.
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        logging.info("POST URL: {url}, HEADERS: {headers}".format(url=kwargs.get("url", ""), headers=kwargs.get("headers", "")))
        kwargs["timeout"] = self.__timeout
        r = requests.post(**kwargs)
        r.raise_for_status()
        return r

    def put(self, **kwargs):
        """Sends a PUT request.
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        logging.info("PUT URL: {url}, HEADERS: {headers}".format(url=kwargs.get("url", ""), headers=kwargs.get("headers", "")))
        kwargs["timeout"] = self.__timeout
        r = requests.put(**kwargs)
        r.raise_for_status()
        return r
