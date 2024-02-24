#!/usr/bin/env python3

import json
from http.server import HTTPServer, BaseHTTPRequestHandler

class AlertHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers.get('content-length', 0))
        data = json.loads(self.rfile.read(content_len))
        print("Received %u %s alerts:" % (len(data["alerts"]), data["status"]))
        print("\tGrouping ables:")
        for k,v in data['groupLabels'].items():
          print("\t\t%s: %s" % (k, v))
        print("\tCommon labels:")
        for k,v in data['commonLabels'].items():
          print("\t\t%s: %s" % (k, v))
        print("\tCommon annotations:")
        for k,v in data['commonAnnotations'].items():
          print("\t\t%s: %s" % (k, v))
        print("\t\tAlert details:")
        for idx, alert in enumerate(data['alerts']):
            print("\t\t\tAlert %u:" % idx)
            print("\t\t\t\tLabels: %r" % alert['labels'])
            print("\t\t\t\tAnnotations: %r" % alert['annotations'])

        self.send_response(200)
        self.end_headers()

if __name__ == '__main__':
   httpd = HTTPServer(('', 9595), AlertHandler)
   httpd.serve_forever()
