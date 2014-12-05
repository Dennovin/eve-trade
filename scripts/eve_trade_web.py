#!/usr/bin/env python

import psycopg2.extras

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.netutil
import tornado.web

import evetrade

application = tornado.web.Application([
        (r"/item-stats/(.*)", evetrade.ItemStatsHandler),
        (r"/daily-stats/(.*)", evetrade.DailyStatsHandler),
        (r"/static/(.*)", evetrade.StaticHandler),
        ])

if __name__ == "__main__":
    evetrade.Config.add_argument("--listen-address", dest="listen_address", default="localhost", help="Listen address")
    evetrade.Config.add_argument("--listen-port", dest="listen_port", default=8000, help="Listen port")
    evetrade.Config.add_argument("--unix-socket", dest="unix_socket", default=None, help="Unix socket path")

    args = evetrade.Config.parse_args()

    if args.unix_socket:
        server = tornado.httpserver.HTTPServer(application)
        socket = tornado.netutil.bind_unix_socket(args.unix_socket)
        server.add_socket(socket)
    else:
        application.listen(args.listen_port, address=args.listen_address)

    evetrade.DB.prepare()
    tornado.ioloop.IOLoop.instance().start()
