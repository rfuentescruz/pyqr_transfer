from __future__ import print_function

import os
import socket
import sys

try:
    from SimpleHTTPServer import SimpleHTTPRequestHandler
except ImportError:
    from http.server import SimpleHTTPRequestHandler

try:
    from SocketServer import TCPServer as HTTPServer
except ImportError:
    from http.server import HTTPServer

import pyqrcode


class Handler(SimpleHTTPRequestHandler):
    def do_HEAD(self, path=None):
        if path is None:
            path = sys.argv[1]
        self.send_head(path)

    def do_GET(self):
        path = sys.argv[1]
        self.do_HEAD(path)
        with open(path, 'rb') as f:
            self.copyfile(f, self.wfile)

    def send_head(self, path):
        try:
            fs = os.stat(path)
            self.send_response(200)
            self.send_header('Content-Type', self.guess_type(path))
            self.send_header('Content-Length', str(fs[6]))
            self.send_header(
                'Content-Disposition',
                'attachment;filename=%s' % os.path.basename(path)
            )
            self.end_headers()
        except OSError:
            self.send_error(404, "File not found")


def get_internal_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 53))
    return s.getsockname()[0]


def usage():
    print('Usage: %s /path/to/file\n' % os.path.basename(sys.argv[0]))
    print(
        'Generates a QR code that will allow you to transfer the specified\n'
        'file to a mobile device in the same network.\n'
    )


def main():
    if len(sys.argv) <= 1:
        print('Please specify a file.')
        usage()
        sys.exit(1)

    server = HTTPServer(('0.0.0.0', 0), Handler)
    server.timeout = 60

    link = 'http://%s:%s' % (get_internal_ip(), server.socket.getsockname()[1])
    print(
        'Scan the QR code below with a phone that is on the same network as '
        'this computer,\nor go directly to this URL using your phone\'s '
        'browser: %s.\nThe link is only valid for %d seconds' % (
            link, server.timeout
        )
    )
    qr = pyqrcode.create(link, version=4)
    print(qr.terminal())

    server.handle_request()
    sys.exit(0)


if __name__ == '__main__':
    main()
