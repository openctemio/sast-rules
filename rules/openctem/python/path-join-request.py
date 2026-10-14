import os

def read(request, base):
    name = request.POST["blog"]
    # ruleid: openctem.python.path.request-data-in-path
    path = os.path.join(base, name)
    # ok: openctem.python.path.request-data-in-path
    safe = os.path.join(base, os.path.basename(request.GET["doc"]))
    return path, safe
