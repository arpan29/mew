class BaseClient(object):

    host = None
    headers = None
    secure = False

    def __init__(self, service_conf, extra_headers):
        self.host = service_conf.get("HOST")
        self.headers = service_conf.get("HEADERS")

        if extra_headers:
            for key, value in extra_headers.items():
                self.headers[key] = value

    def get_baseurl(self):
        protocol = "https://" if self.secure else "http://"
        return protocol + self.host

    def get_headers(self):
        return self.headers

    def get_filter_string(self, filters):
        if not filters:
            return ""
        filter_str = ""
        for key, value in filters.items():
            filter_str += str(key) + "=" + ",".join([str(v) for v in value]) + "&"
        return filter_str

    def get_include_string(self, includes):
        return ",".join([str(u) for u in includes]) if includes else ''
