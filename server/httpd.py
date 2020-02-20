import http.server
import socketserver
import re
import config
import log
import traceback
import cherrypy
from cherrypy._cpserver import Server

logger = log.create_logger(__name__)

@cherrypy.expose
class CommandsApi(object):
    def __init__(self, broker):
        self.broker = broker

    @cherrypy.tools.json_out()
    def GET(self):
        logger.debug("Parse port from %s", cherrypy.request.base)
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        return self.broker.get_commands()

    @cherrypy.tools.json_out()
    def POST(self, number):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        path_pattern = re.compile("([0-9]+)")
        match = path_pattern.match(number)
        if match:
            command = match.group(1)
            logger.debug("Recognized httpd command %s", command)
            try:
                logger.debug("Executing command %s", command)
                self.broker.on_command(command)
                result = 'Command executed'
            except:
                traceback.print_exc()
                result = 'Command recognized but failed'
        else:
            logger.warning("Command number can be number only")
            result = 'Unsupported command number'
        return {'message': result}

    def _cp_dispatch(self, vpath):
        if len(vpath) == 1:
            cherrypy.request.params['number'] = vpath.pop()
            return self
        return vpath

@cherrypy.expose
class ClientsApi(object):
    @cherrypy.tools.json_out()
    def POST(self):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        logger.debug("I see client request")
        return {'status': 'ok'}


conf = {
        '/': {'request.dispatch':  cherrypy.dispatch.MethodDispatcher(),
                 'tools.sessions.on': False,
                 'tools.response_headers.on': True,
                 'tools.response_headers.headers': [('Content-Type', 'application/json')]}
            }

def start_httpd(broker, client):
    cherrypy.tree.mount(CommandsApi(broker), '/commands', conf)
    server = Server()
    server.socket_port = 8090
    server.subscribe()
    cherrypy.tree.mount(ClientsApi(), '/clients', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()