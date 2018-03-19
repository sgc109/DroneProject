from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
import ast

from jsonrpc import JSONRPCResponseManager, dispatcher
import time

def reply(s):
    fp = open('serverPic/img' + str(time.time()) + '.jpg','wb')
    fp.write(s.decode('base64'))
    fp.close()

@Request.application
def application(request):
    dispatcher['isAlive'] = lambda s : reply(s)
  
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')

if __name__ == '__main__':
    run_simple('localhost', 10000, application)
