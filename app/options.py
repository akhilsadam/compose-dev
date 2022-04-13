class options:
    appname = "compose"
    apiversion='v0.0.2'
    host = "0.0.0.0"
    redhost = "" # internal
    port = 5026
    redport = 6379
    baseurl = f"http://{host}:{port}"
    mdfile = "app/static/api.md"
    readmelink = "https://github.com/akhilsadam/compose"
    template = "templates/"

    def sethost(host):
        """Set Redis host ip address
        Args:
            host (str): ip address
        """
        options.redhost=host