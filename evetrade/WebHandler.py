import locale
import pkg_resources
import tornado.template
import tornado.web

from Config import Config
from DB import DB

class WebHandler(tornado.web.RequestHandler):
    loader = None

    def __init__(self, *args, **kwargs):
        super(WebHandler, self).__init__(*args, **kwargs)

        locale.setlocale(locale.LC_ALL, Config.get("locale"))

        if WebHandler.loader is None:
            WebHandler.loader = tornado.template.Loader(pkg_resources.resource_filename(__name__, "templates"))

        self.loader = WebHandler.loader
        self.session = DB.session()

    def number_format(self, number, decimals=0):
        return locale.format("%.0{}f".format(decimals), number, grouping=True)

    def on_finish(self):
        self.session.close()

class StaticHandler(tornado.web.StaticFileHandler):
    def initialize(self):
        super(StaticHandler, self).initialize(pkg_resources.resource_filename(__name__, "static"))
