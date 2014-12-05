#!/usr/bin/env python

import psycopg2.extras

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.netutil
import tornado.web

from evetrade import DB, Config, StaticHandler, ItemStatsHandler

application = tornado.web.Application([
        (r"/item-stats/(.*)", ItemStatsHandler),
        (r"/static/(.*)", StaticHandler),
        ])

if __name__ == "__main__":
    Config.add_argument("--listen-address", dest="listen_address", default="localhost", help="Listen address")
    Config.add_argument("--listen-port", dest="listen_port", default=8000, help="Listen port")
    Config.add_argument("--unix-socket", dest="unix_socket", default=None, help="Unix socket path")

    args = Config.parse_args()

    if args.unix_socket:
        server = tornado.httpserver.HTTPServer(application)
        socket = tornado.netutil.bind_unix_socket(args.unix_socket)
        server.add_socket(socket)
    else:
        application.listen(args.listen_port, address=args.listen_address)

    DB.prepare()
    tornado.ioloop.IOLoop.instance().start()
