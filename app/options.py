class options:
    appname = "compose"
    apiversion='v0.0.2'
    host = "0.0.0.0"
    redhost = "" # internal
    port = 5026
    proxy = ""
    redport = 6379
    baseurl = f"http://{host}:{port}{proxy}"
    deployurl = "https://isp-proxy.tacc.utexas.edu"
    mdfile = "app/static/api.md"
    readmelink = "https://github.com/akhilsadam/compose"
    template = "templates/"

    def sethost(rhost):
        """Set Redis host ip address
        Args:
            rhost (str): ip address
        """
        options.redhost=rhost

    def setproxy(pxy):
        """Set nginx proxy ip address
        Args:
            pxy (str): ip address extension
        """
        options.proxy=f"/{pxy}"
        options.baseurl = f"http://{options.host}:{options.port}{options.proxy}"
    
    def getURL() -> str:
        """Get baseurl for documentation generator
        Returns:
            str : baseurl
        """
        if options.proxy == "":
            return f"http://localhost:{options.port}{options.proxy}"
        return f"{options.deployurl}{options.proxy}"