import http.server
import socketserver
import re
import config
import log
import traceback
import cherrypy
import clients
from cherrypy._cpserver import Server
import jwt
import time

logger = log.create_logger(__name__)

def check_security(request):
    if request.base.endswith(str(config.HTTPD_PUBLIC_PORT)):
        logger.debug("Public access detected, checking jwt")
        token = request.headers.get('AUTHORIZATION')
        if not token:
            logger.error("Authorization header missing")
        elif token.startswith("Bearer "):
            token = token[7:]
            logger.debug("Found token %s", token)
            all_clients = clients.get_clients()
            for client in all_clients:
                try:
                    # https://stackoverflow.com/a/32804171
                    decoded = jwt.decode(token, client.get('key'), algorithms='RS256')
                    if (check_time(decoded)):
                        return client
                    #print(decoded)
                except ValueError:
                    logger.warn("Skipping key %s as it can't be parsed", client.get('key'))
        else:
            logger.error("Unknown authorization")
        raise cherrypy.HTTPError(403, message="Token missing or wrong")

def check_time(token):
    current_epoch = time.time()
    token_time = token.get('jti')
    if token_time:
        diff = current_epoch - int(token_time) / 1000.0
        logger.debug("Detected time diff: %f seconds", diff)
        return diff < 120
    return False

@cherrypy.expose
class CommandsApi(object):
    def __init__(self, broker):
        self.broker = broker

    @cherrypy.tools.json_out()
    def GET(self):
        check_security(cherrypy.request)
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
    @cherrypy.tools.json_in()
    def POST(self):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        data = cherrypy.request.json
        clients.register_client(data.get('key'), data.get('message'))
        return {'status': 'ok'}

    @cherrypy.tools.json_out()
    def GET(self):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        return clients.get_clients()

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def PUT(self, id):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        return clients.update_client(id, cherrypy.request.json)

    @cherrypy.tools.json_out()
    def DELETE(self, id):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        if clients.delete_client(id):
            return {'status': 'ok'}
        else:
            return {'status': 'ko'}

    def _cp_dispatch(self, vpath):
        if len(vpath) == 1:
            cherrypy.request.params['id'] = vpath.pop()
            return self
        return vpath


conf = {
        '/': {'request.dispatch':  cherrypy.dispatch.MethodDispatcher(),
                 'tools.sessions.on': False,
                 'tools.response_headers.on': True,
                 'tools.response_headers.headers': [('Content-Type', 'application/json')]}
            }

def start_httpd(broker, client):
    cherrypy.tree.mount(CommandsApi(broker), '/commands', conf)
    server = Server()
    server.socket_port = config.HTTPD_PUBLIC_PORT
    server.subscribe()
    cherrypy.tree.mount(ClientsApi(), '/clients', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()