def responseheaders(ctx, flow):
    """
    Enables streaming for all responses.
    """
    flow.response.stream = True