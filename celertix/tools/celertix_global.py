from sanic import Sanic
from sanic_auth import Auth 
from sanic import Blueprint,response

clx = Sanic(__name__)
Clxauth = Auth(clx)
ClxBlr = Blueprint
ClxRsp = response

# Route Registry
ClxRegistry = sky.blueprint


