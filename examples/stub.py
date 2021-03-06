"""
    This is a script stub, with definitions for all events.
"""
def start(ctx, argv):
    """
        Called once on script startup, before any other events.
    """
    ctx.log("start")

def clientconnect(ctx, client_connect):
    """
        Called when a client initiates a connection to the proxy. Note that a
        connection can correspond to multiple HTTP requests
    """
    ctx.log("clientconnect")

def serverconnect(ctx, server_connection):
    """
        Called when the proxy initiates a connection to the target server. Note that a
        connection can correspond to multiple HTTP requests
    """
    ctx.log("serverconnect")

def request(ctx, flow):
    """
        Called when a client request has been received.
    """
    ctx.log("request")


def responseheaders(ctx, flow):
    """
        Called when the response headers for a server response have been received,
        but the response body has not been processed yet. Can be used to tell mitmproxy
        to stream the response.
    """
    ctx.log("responseheaders")

def response(ctx, flow):
    """
       Called when a server response has been received.
    """
    ctx.log("response")

def error(ctx, flow):
    """
        Called when a flow error has occured, e.g. invalid server responses, or
        interrupted connections. This is distinct from a valid server HTTP error
        response, which is simply a response with an HTTP error code.
    """
    ctx.log("error")

def clientdisconnect(ctx, client_disconnect):
    """
        Called when a client disconnects from the proxy.
    """
    ctx.log("clientdisconnect")

def done(ctx):
    """
        Called once on script shutdown, after any other events.
    """
    ctx.log("done")
