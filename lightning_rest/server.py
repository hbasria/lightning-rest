import json

from klein import Klein

from lightning_rest.lightning import LightningRpc


def response(resp):
    return json.dumps(resp)


class LightningRest(object):
    app = Klein()

    def __init__(self, path):
        self.rpc = LightningRpc(path)

    @app.route('/')
    def home(self, request):
        return """<html>
                    <style>body {padding:20px;max-width:800px;pre { background-color:#eee; }</style>
                    <body>
                        <h2>endpoints:</h2>
                        <p>
                            <ul>                            
                                <li><pre>/api/addr/new</pre></li>
                                <li><pre>/api/channels</pre></li>
                                <li><pre>/api/funds</pre></li>
                                <li><pre>/api/invoices</pre></li>
                                <li><pre>/api/payments</pre></li>
                                <li><pre>/api/nodes</pre></li>
                                <li><pre>/api/peers</pre></li>
                                <li><pre>/api/peers/{peer_id}</pre></li>
                                <li><pre>/api/routes/{peer_id}?msatoshi={msatoshi}&riskfactor={riskfactor}&cltv={cltv}</pre></li>
                                <li><pre>/api/dev/blockheight</pre></li>
                                <li><pre>/api/dev/setfees</pre></li>
                            </ul>
                        </p>                                                
                    </body>
                </html>"""

    @app.route('/api/channels', methods=['GET'])
    def channels(self, request):
        short_channel_id = request.args.get('short_channel_id', None)
        return response(self.rpc.listchannels(short_channel_id=short_channel_id))

    @app.route('/api/invoices', methods=['GET'])
    def invoices(self, request):
        label = request.args.get('label', None)
        return response(self.rpc.listinvoices(label=label))

    @app.route('/api/payments', methods=['GET'])
    def payments(self, request):
        bolt11 = request.args.get('bolt11', None)
        payment_hash = request.args.get('payment_hash', None)

        return response(self.rpc.listpayments(bolt11=bolt11, payment_hash=payment_hash))

    @app.route('/api/nodes', methods=['GET'])
    def nodes(self, request):
        return response(self.rpc.listnodes())

    @app.route('/api/peers', methods=['GET'])
    def peers(self, request):
        return response(self.rpc.listpeers())

    @app.route('/api/peers/<string:peer_id>', methods=['GET'])
    def get_peer(self, request, peer_id):
        return response(self.rpc.getpeer(peer_id))

    @app.route('/api/routes/<string:peer_id>', methods=['GET'])
    def get_route(self, request, peer_id):
        msatoshi = request.args.get('msatoshi', None)
        riskfactor = request.args.get('riskfactor', None)
        cltv = request.args.get('cltv', None)

        return response(self.rpc.getroute(peer_id, msatoshi, riskfactor, cltv=cltv))

    @app.route('/api/dev/blockheight', methods=['GET'])
    def peers(self, request):
        return response(self.rpc.dev_blockheight())

    @app.route('/api/dev/setfees', methods=['POST'])
    def set_fees(self, request):
        immediate = request.args.get('immediate', None)
        normal = request.args.get('normal', None)
        slow = request.args.get('slow', None)

        return response(self.rpc.dev_setfees(immediate, normal=normal, slow=slow))

    @app.route('/api/addr/new', methods=['POST'])
    def newaddr(self, request):
        addrtype = request.args.get('addrtype', 'p2sh-segwit')
        return response(self.rpc.newaddr(addrtype=addrtype))

    @app.route('/api/funds', methods=['GET'])
    def funds(self, request):
        return response(self.rpc.listfunds())


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

    server = LightningRest(args.path)
    server.app.run(args.bind, args.port)
