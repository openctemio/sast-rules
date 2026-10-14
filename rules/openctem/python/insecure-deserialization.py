import pickle, yaml, base64

def load(blob, f):
    # ruleid: openctem.python.deserialization.unsafe-loader
    user = pickle.loads(base64.b64decode(blob))
    # ruleid: openctem.python.deserialization.unsafe-loader
    data = yaml.load(f, yaml.Loader)
    # ok: openctem.python.deserialization.unsafe-loader
    conf = yaml.safe_load(f)
    return user, data, conf
