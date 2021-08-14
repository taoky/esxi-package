#!/usr/bin/python
from daemon import Daemon
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import subprocess
import sys
import time
import ConfigParser


config = ConfigParser.RawConfigParser()
config.read(['/etc/runner.config', '../../etc/runner.config'])


class MessageCache:
    def __init__(self):
        self.message = ""
        self.message_last_updated = None

    def update(self):
        if self.message_last_updated is None or time.time() - self.message_last_updated > 120:
            # 120s or init
            process = subprocess.Popen(config.get("runner", "cmd").split(" "), cwd=config.get("runner", "cwd"), stdout=subprocess.PIPE)
            output = process.communicate()[0]
            if process.returncode != 0:
                self.message = "process returns {}".format(process.returncode)
            else:
                self.message = output
            self.message_last_updated = time.time()
        return self.message


message_cache = MessageCache()


class Handler(BaseHTTPRequestHandler):
    def setup(self):
        self.timeout = 5
        BaseHTTPRequestHandler.setup(self)

    def do_GET(self):
        message = message_cache.update()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message)
        self.wfile.write('\n')


class MyDaemon(Daemon):
    def run(self):
        server = HTTPServer(('0', 8888), Handler)
        print 'Starting server, use <Ctrl-C> to stop'
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    daemon = MyDaemon("/tmp/runner.pid", stdout="/tmp/runner.stdout", stderr="/tmp/runner.stderr")
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
