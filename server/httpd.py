import http.server
import socketserver
import re
import config
import log
import logging
import traceback
import cherrypy
import clients
from cherrypy._cpserver import Server
import jwt
import security

logger = log.create_logger(__name__)
es_logger = log.create_es_logger('CMLserver')

def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    if cherrypy.request.method == "OPTIONS":
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PATCH, PUT, DELETE, OPTIONS'
        cherrypy.response.headers["Access-Control-Allow-Headers"] = "X-Mobile, Authorization, Origin, X-Requested-With, Content-Type, Accept"

@cherrypy.expose
class CommandsApi(object):
    def __init__(self, broker, securityObject):
        self.broker = broker
        self.sec = securityObject

    @cherrypy.tools.json_out()
    def GET(self):
        if self.sec.is_public_access(cherrypy.request):
            client = self.sec.find_client(cherrypy.request)
            if client:
                if client.get('all_commands'):
                    return self.broker.get_commands()
                else:
                    allowed = set(client.get('commands', []))
                    all_commands = self.broker.get_commands()
                    logger.debug(all_commands)
                    return [com for com in all_commands if com['number'] in allowed]
            else:
                logger.debug("Client not found")
                return []
        else:
            return self.broker.get_commands()

    @cherrypy.tools.json_out()
    def POST(self, number):
        es_logger.debug("Incoming command request for {}".format(number))
        client = self.sec.command(cherrypy.request, number)
        path_pattern = re.compile("([0-9]+)")
        match = path_pattern.match(number)
        if match:
            command = match.group(1)
            logger.debug("Recognized httpd command %s", command)
            try:
                logger.debug("Executing command %s", command)
                es_logger.debug("Executing command {} by client {}".format(command, client.get('message', '?') if client is not None else "internal"))
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
    def __init__(self, securityObject):
        self.sec = securityObject

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        data = cherrypy.request.json
        clients.register_client(data.get('key'), data.get('message'))
        return {'status': 'ok'}

    @cherrypy.tools.json_out()
    def GET(self):
        self.sec.only_internal(cherrypy.request)
        return clients.get_clients()

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def PUT(self, id):
        self.sec.only_internal(cherrypy.request)
        return clients.update_client(id, cherrypy.request.json)

    @cherrypy.tools.json_out()
    def DELETE(self, id):
        self.sec.only_internal(cherrypy.request)
        if clients.delete_client(id):
            return {'status': 'ok'}
        else:
            return {'status': 'ko'}

    def OPTIONS(self, id):
        return None

    def _cp_dispatch(self, vpath):
        if len(vpath) == 1:
            cherrypy.request.params['id'] = vpath.pop()
            return self
        return vpath


conf = {
        '/': {
                 'tools.sessions.on': False,
                 'tools.response_headers.on': True,
                 'tools.response_headers.headers': [('Content-Type', 'application/json'), ('Access-Control-Allow-Origin', '*')],
                 'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                 'tools.CORS.on': True
              }
        }

def start_httpd(broker, client):
    securityObject = security.Security()
    cherrypy.tools.CORS = cherrypy.Tool('before_handler', CORS)
    cherrypy.tree.mount(CommandsApi(broker, securityObject), '/commands', conf)
    server = Server()
    server.socket_port = config.HTTPD_PUBLIC_PORT
    server.socket_host = '0.0.0.0'
    server.subscribe()
    cherrypy.config.update( {'server.socket_host': '0.0.0.0'} )
    cherrypy.tree.mount(ClientsApi(securityObject), '/clients', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()