class options:
    appname = "flask-redis"
    apiversion='v0.0.1'
    host = "0.0.0.0"
    redhost = "" # internal
    port = 5026
    redport = 6379
    baseurl = f"http://{host}:{port}"
    mdfile = "app/static/api.md"

    def sethost(host):
        """Set Redis host ip address

        Args:
            host (str): ip address
        """
        options.redhost=host