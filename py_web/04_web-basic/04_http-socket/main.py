import json
import logging
import mimetypes
import socket
import urllib.parse
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from threading import Thread

HTTP_SERVER_IP = ""
HTTP_SERVER_PORT = 3000

SOCKET_SERVER_IP = "127.0.0.1"
SOCKET_SERVER_PORT = 5000
SOCKET_SERVER_TYPE = socket.AF_INET
SOCKET_SERVER_PROTOCOL = socket.SOCK_DGRAM
SOCKET_BYTES = 1024

JSON_FILENAME = "data.json"
JSON_STORAGE = "storage"

BASE_DIR = Path()


def send_data_to_socket(body):
    logging.debug("Send data via socket.")
    client_socket = socket.socket(SOCKET_SERVER_TYPE, SOCKET_SERVER_PROTOCOL)
    client_socket.sendto(body, (SOCKET_SERVER_IP, SOCKET_SERVER_PORT))
    client_socket.close()


class HttpGetHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read(int(self.headers["Content-Length"]))

        send_data_to_socket(body)

        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

    def do_GET(self):
        route = urllib.parse.urlparse(self.path)

        match route.path:
            case "/":
                self.send_html("index.html")
            case "/message":
                self.send_html("message.html")
            case _:
                file = BASE_DIR / route.path[1:]
                if file.exists():
                    self.send_static(file)
                else:
                    self.send_html("error.html")

    def send_html(self, filename, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        with open(filename, "rb") as f:
            self.wfile.write(f.read())

    def send_static(self, filename, status_code=200):
        self.send_response(status_code)
        mime_type, *rest = mimetypes.guess_type(filename)
        if mime_type:
            self.send_header("Content-type", mime_type)
        else:
            self.send_header("Content-type", "text/plain")
            pass
        self.end_headers()

        with open(filename, "rb") as f:
            self.wfile.write(f.read())


# socket server main function
def run_socket_server(ip, port):
    logging.debug("Start socket server.")
    server_socket = socket.socket(SOCKET_SERVER_TYPE, SOCKET_SERVER_PROTOCOL)
    server = (ip, port)
    server_socket.bind(server)
    try:
        while True:
            data, address = server_socket.recvfrom(SOCKET_BYTES)
            save_data(data)
            # print(f"Data from addr: {address}, Data: {data}")
    except KeyboardInterrupt:
        logging.info("Socket server stopped.")
    finally:
        logging.debug("Stop socket server.")
        server_socket.close()


def save_data(data):
    body = urllib.parse.unquote_plus(data.decode())
    try:
        payload = {
            key: value for key, value in [el.split("=") for el in body.split("&")]
        }

        # if destination file or directory not exists
        if not BASE_DIR.joinpath(JSON_STORAGE + "/" + JSON_FILENAME).exists():
            # if directory not exist
            if not BASE_DIR.joinpath(JSON_STORAGE).exists():
                # create directory
                BASE_DIR.joinpath(JSON_STORAGE).mkdir(exist_ok=True)
            unpacked = {}
        else:
            # read file content if exist
            with open(
                BASE_DIR.joinpath(JSON_STORAGE + "/" + JSON_FILENAME),
                "r",
                encoding="utf-8",
            ) as fh:
                unpacked = json.load(fh)

        # preformatted data
        entry = {
            str(datetime.now()): {
                "username": payload.get("username"),
                "message": payload.get("message"),
            }
        }

        # add data to json content
        unpacked.update(entry)
        # write whole json data to file
        with open(
            BASE_DIR.joinpath(JSON_STORAGE + "/" + JSON_FILENAME), "w", encoding="utf-8"
        ) as fh:
            json.dump(unpacked, fh, ensure_ascii=False)

    except ValueError as e:
        logging.error(f"Parse error: {body}.\n{e}")
    except OSError as e:
        logging.error(f"File error: {body}.\n{e}")


# http server main function
def run_http_server(port, ip="", server_class=HTTPServer, handler_class=HttpGetHandler):
    logging.debug("Start http server.")
    server_address = (ip, port)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        logging.debug("Stop http server.")
        http.server_close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")
    logging.debug("Starting app.")

    threads = [
        Thread(target=run_socket_server, args=(SOCKET_SERVER_IP, SOCKET_SERVER_PORT)),
        Thread(target=run_http_server, args=(HTTP_SERVER_PORT, HTTP_SERVER_IP)),
    ]
    [th.start() for th in threads]
    [th.join() for th in threads]
