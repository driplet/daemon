import auth
import en_us

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.websocket
import tornado.options

import functools
import asyncio
import subprocess
import threading
import time
import sys
import os
import json

from zeroless import (Client)

class ChannelHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def on_open(self):
        print("connection made")

    def on_message(self, message):
        try:
            request = json.loads(message)
        except:
            self.write_message("Malformed request.")
            return

        if "authentication" not in request or "serviceid" not in request:
            self.write_message("Malformed request.")
            return

        auth_status = auth.verify(
            request['authentication']['client_id'], request['authentication']['token'])
        if not auth_status:
            self.write_message(en_us.AUTH_FAILED)
            return

        self.write_message("Authentication was successful.")
        x = threading.Thread(target=self.bind, args=[
                         request['serviceid']])
        x.start()

    def bind(self, serviceid):
        asyncio.set_event_loop(asyncio.new_event_loop())
        client = Client()
        client.connect_local(port=9876)
        listen = client.sub()
        for item in listen:
            data = json.loads(item.decode('utf-8'))
            if data["service_id"] == serviceid:
                self.write_message(data["content"])

def main():
    asyncio.set_event_loop(asyncio.new_event_loop())
    # Create tornado application and supply URL routes
    application = tornado.web.Application([
        (r'/', ChannelHandler)
    ])

    # Setup HTTP Server
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(3142, "127.0.0.1")

    # Start IO/Event loop
    tornado.ioloop.IOLoop.instance().start()


main()