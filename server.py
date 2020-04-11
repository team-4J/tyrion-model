from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import logging

port = 8084
img = "test.jpg"
bashCommand = "alpr " + str(img)

class S(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/execute/tyrion':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            result = output.decode("utf-8").split("-")[1]

            plate_result = result.split(" ")[1].split("\t")[0]
            score_result = result.split(" ")[3].split("\n")[0]
            to_return = "{\"license_plate\": \"" + str(plate_result) + "\", \"score\": \"" + str(score_result) + "\"}"

            self.wfile.write(bytes(to_return, "utf-8"))
            logging.info(" [status:200] [license_plate:" + str(plate_result) + "] [score:" + str(score_result) + "]")
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes("{\"message\": \"Not found\"}", "utf-8"))

def run(server_class=HTTPServer, handler_class=S, port=port):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info(' watson-model listening at port ' + str(port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
