from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import threading


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<html><body><h1>BLAHBLAH</h1></body></html>".encode())
        return


def run(httpd):
    httpd.serve_forever()
    return


def run_server(server_address, httpd, interval):
    print("Starting local server...")
    server = threading.Thread(target=run, args=[httpd])
    server.setDaemon(
        True
    )  # so that main thread sleeps for however long we want the server open and shuts it down
    server.start()
    time.sleep(interval)
    print("Shutting down local server...")
    httpd.shutdown()
    return


def main():
    server_address = ("", 9090)
    httpd = HTTPServer(server_address, handler)
    # start server and keep it up for interval
    run_server(server_address, httpd, interval=20)
    # how long to keep the server down
    time.sleep(40)
    # restart server
    run_server(server_address, httpd, interval=400)


if __name__ == "__main__":
    main()
