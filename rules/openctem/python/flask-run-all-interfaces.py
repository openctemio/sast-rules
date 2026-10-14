from flask import Flask
app = Flask(__name__)
# ruleid: openctem.python.flask.run-all-interfaces
app.run(host='0.0.0.0', port=8080)
# ok: openctem.python.flask.run-all-interfaces
app.run(host='127.0.0.1', port=8080)
