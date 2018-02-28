from aiohttp import web
from aiohttp_swagger import *

from lightning_rest.lightning import LightningRpc

routes = web.RouteTableDef()


@routes.get('/api/getinfo')
async def getinfo(request):
    """
    ---
    description: Show information about this node.
    tags:
    - getinfo
    produces:
    - application/json
    responses:
        "200":
            description: successful operation.
    """
    return web.json_response(request.app['rpc'].getinfo())


@routes.post('/api/connect/{peer_id}')
async def connect(request):
    """
    ---
    description: Connect to {id} at {host} (which can end in ':port' if not default)
    tags:
    - connect
    produces:
    - application/json
    parameters:
    - in: path
      name: peer_id
      description: peer id
      required: true
      type: string
    - in: body
      name: body
      required: true
      schema:
        type: object
        properties:
          host:
            type: string
          port:
            type: string
    responses:
        "200":
            description: successful operation.
    """
    data = await request.json()

    peer_id = request.match_info.get('peer_id', None)
    host = data.get('host', None)
    port = data.get('port', None)

    return web.json_response(request.app['rpc'].connect(peer_id, host, port))


@routes.post('/api/nodes')
async def node_list(request):
    """
    ---
    description: Show all nodes in our local network view.
    tags:
    - nodes
    produces:
    - application/json
    responses:
        "200":
            description: successful operation.
    """
    return web.json_response(request.app['rpc'].listnodes())


@routes.post('/api/channels')
async def channel_list(request):
    """
    ---
    description: Show all known channels.
    tags:
    - channels
    produces:
    - application/json
    parameters:
    - in: body
      name: body
      description: short channel id
      required: false
      schema:
        type: object
        properties:
          short_channel_id:
            type: integer
    responses:
        "200":
            description: successful operation.
    """
    data = await request.json()

    short_channel_id = data.get('short_channel_id', None)

    return web.json_response(request.app['rpc'].listchannels(short_channel_id=short_channel_id))


@routes.post('/api/peers')
async def peer_list(request):
    """
    ---
    description: Show current peers, if {level} is set, include logs for {id}
    tags:
    - peers
    produces:
    - application/json
    responses:
        "200":
            description: successful operation.
    """

    return web.json_response(request.app['rpc'].listpeers())


@routes.get('/api/peers/{peer_id}')
async def peer_detail(request):
    """
    ---
    description: Show current peers, if {level} is set, include logs for {id}
    tags:
    - peers
    produces:
    - application/json
    parameters:
    - in: path
      name: peer_id
      description: peer id
      required: true
      type: string
    responses:
        "200":
            description: successful operation.
    """
    peer_id = request.match_info.get('peer_id', None)

    return web.json_response(request.app['rpc'].listpeers(peer_id=peer_id))


@routes.post('/api/funds')
def fund_list(request):
    """
    ---
    description: Show available funds from the internal wallet.
    tags:
    - funds
    produces:
    - application/json
    responses:
        "200":
            description: successful operation.
    """
    return web.json_response(request.app['rpc'].listfunds())


@routes.post('/api/routes/{peer_id}')
async def route_find(request):
    """
    ---
    description: Show route to {id} for {msatoshi}, using {riskfactor} and optional {cltv} (default 9), if specified search from {source} otherwise use this node as source.
    tags:
    - routes
    produces:
    - application/json
    parameters:
    - in: path
      name: peer_id
      description: peer id
      required: true
      type: string
    - in: body
      name: body
      required: true
      schema:
        type: object
        properties:
          msatoshi:
            type: string
          riskfactor:
            type: string
          cltv:
            type: string
    responses:
        "200":
            description: successful operation.
    """
    data = await request.json()

    peer_id = request.match_info.get('peer_id', None)
    msatoshi = data.get('msatoshi', None)
    riskfactor = data.get('riskfactor', None)
    cltv = data.get('cltv', None)

    return web.json_response(request.app['rpc'].getroute(peer_id, msatoshi, riskfactor, cltv=cltv))


@routes.post('/api/invoices/{label}')
async def invoice_list(request):
    """
    ---
    description: Show invoice {label} (or all, if no {label})
    tags:
    - invoices
    produces:
    - application/json
    parameters:
    - in: path
      name: label
      description: label
      required: false
      type: string
    responses:
        "200":
            description: successful operation.
    """
    label = request.match_info.get('label', None)

    return web.json_response(request.app['rpc'].listinvoices(label=label))


@routes.post('/api/invoices')
async def invoice_add(request):
    """
    ---
    description: Create an invoice for {msatoshi} with {label} and {description} with optional {expiry} seconds (default 1 hour)
    tags:
    - invoices
    produces:
    - application/json
    parameters:
    - in: body
      name: body
      required: false
      schema:
        type: object
        properties:
          msatoshi:
            type: integer
          label:
            type: string
          description:
            type: string
          expiry:
            type: integer
    responses:
        "200":
            description: successful operation.
    """
    data = await request.json()

    msatoshi = data.get('msatoshi', None)
    label = data.get('label', None)
    description = data.get('description', None)
    expiry = data.get('expiry', None)

    return web.json_response(request.app['rpc'].invoice(msatoshi, label, description, expiry=expiry))


@routes.delete('/api/invoices/{label}')
async def invoice_del(request):
    """
    ---
    description: Delete unpaid invoice {label} with {status}
    tags:
    - invoices
    produces:
    - application/json
    parameters:
    - in: path
      name: label
      description: label
      required: true
      type: string
    - in: body
      name: body
      required: false
      schema:
        type: object
        properties:
          label:
            type: string
          status:
            type: string
    responses:
        "200":
            description: successful operation.
    """
    data = await request.json()
    label = request.match_info.get('label', None)
    status = data.get('status', None)

    return web.json_response(request.app['rpc'].delinvoice(label, status))


@routes.post('/api/payments')
async def payment_list(request):
    """
    ---
    description: Show outgoing payments, regarding {bolt11} or {payment_hash} if set Can only specify one of {bolt11} or {payment_hash}
    tags:
    - payments
    produces:
    - application/json
    parameters:
    - in: body
      name: body
      required: false
      schema:
        type: object
        properties:
          bolt11:
            type: string
          payment_hash:
            type: string
    responses:
        "200":
            description: successful operation.
    """

    data = await request.json()
    bolt11 = data.get('bolt11', None)
    payment_hash = data.get('payment_hash', None)

    return web.json_response(request.app['rpc'].listpayments(bolt11=bolt11, payment_hash=payment_hash))


@routes.post('/api/payments/decode')
async def payment_decode(request):
    """
    ---
    description: Decode {bolt11}, using {description} if necessary
    tags:
    - payments
    produces:
    - application/json
    parameters:
    - in: body
      name: body
      required: false
      schema:
        type: object
        properties:
          bolt11:
            type: string
          description:
            type: string
    responses:
        "200":
            description: successful operation.
    """
    data = await request.json()

    bolt11 = data.get('bolt11', None)
    description = data.get('description', None)

    return web.json_response(request.app['rpc'].decodepay(bolt11, description=description))


@routes.post('/api/payments/add')
async def payment_add(request):
    """
    ---
    description: Send payment specified by {bolt11} with optional {msatoshi} (if and only if {bolt11} does not have amount), {description} (required if {bolt11} uses description hash) and {riskfactor} (default 1.0)
    tags:
    - payments
    produces:
    - application/json
    parameters:
    - in: body
      name: body
      required: false
      schema:
        type: object
        properties:
          bolt11:
            type: string
          msatoshi:
            type: integer
          description:
            type: string
          riskfactor:
            type: string
    responses:
        "200":
            description: successful operation.
    """
    data = await request.json()

    bolt11 = data.get('bolt11', None)
    msatoshi = data.get('msatoshi', None)
    description = data.get('description', None)
    riskfactor = data.get('riskfactor', None)

    return web.json_response(
        request.app['rpc'].pay(bolt11, msatoshi=msatoshi, description=description, riskfactor=riskfactor))


@routes.get('/api/dev/blockheight')
async def dev_blockheight(request):
    """
    ---
    description: Show current block height.
    tags:
    - dev
    produces:
    - application/json
    responses:
        "200":
            description: successful operation.
    """

    return web.json_response(request.app['rpc'].dev_blockheight())


@routes.post('/api/dev/setfees')
async def dev_setfees(request):
    """
    ---
    description: Set feerate in satoshi-per-kw for {immediate}, {normal} and {slow} (each is optional, when set, separate by spaces) and show the value of those three feerates
    tags:
    - dev
    produces:
    - application/json
    parameters:
    - in: body
      name: body
      required: true
      schema:
        type: object
        properties:
          immediate:
            type: integer
          normal:
            type: integer
          slow:
            type: integer
    responses:
        "200":
            description: successful operation.
    """
    data = await request.json()

    immediate = data.get('immediate', None)
    normal = data.get('normal', None)
    slow = data.get('slow', None)

    return web.json_response(request.app['rpc'].dev_setfees(immediate, normal=normal, slow=slow))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--bind', '-b', default='0.0.0.0', metavar='ADDRESS',
                        help='Specify alternate bind address '
                             '[default: all interfaces]')
    parser.add_argument('port', action='store',
                        default=8000, type=int,
                        nargs='?',
                        help='Specify alternate port [default: 8000]')
    parser.add_argument('path', action='store',
                        default='~/.lightning/lightning-rpc', type=str,
                        nargs='?',
                        help='Lightning RPC Socket Path [default: ~/.lightning/lightning-rpc]')
    args = parser.parse_args()

    app = web.Application()
    app['rpc'] = LightningRpc(args.path)
    app.router.add_routes(routes)

    setup_swagger(app,
                  title="Rest API for the `lightningd` daemon.")

    web.run_app(app, host=args.bind, port=args.port)
