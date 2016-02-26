import flask
import logging
import serial
from termcolor import colored
from Responder import Responder

app = flask.Flask(__name__)

http_logging = False

responder = None

ser = None


@app.route("/")
def default() -> str:
    return '<html style="text-align: center; background-color: black; color: white; font-size: large;">' \
           '<head></head></body>' \
           "<h1><u>This is not the page you are looking for</u></h1>" \
           "<h2>Try:</h2>" \
           "<p>/characteristic/read/&lt;uuid&gt</p>" \
           "<p>/characteristic/write/&lt;uuid&gt/&lt;value&gt</p>" \
           "<p>/connect</p>" \
           "<p>/disconnect</p>" \
           "</ br></ br></ br>" \
           '<img src=' \
           '"http://2.bp.blogspot.com/_vRVJN4kcBZs/Suw2vq5JBQI/AAAAAAAAK0Q/p5v5VwFo3_E/s400/Pooped_A_Little.jpg">' \
           "</body></html>"


@app.errorhandler(404)
def page_not_found(e) -> str:
    return "404"


@app.route("/connect")
def connect() -> str:
    response = responder.connect_client()
    ser.write(response.encode())
    print(response, end="")
    return response


@app.route("/disconnect")
def disconnect() -> str:
    response = responder.disconnect_client()
    ser.write(response.encode())
    print(response, end="")
    return response


@app.route("/characteristic/read/<uuid>")
def characteristics_read(uuid: str) -> str:
    return responder.read(uuid)


@app.route("/characteristic/write/<uuid>/<value>")
def characteristics_write(uuid: str, value: str) -> str:
    response = responder.write(uuid, value)
    response_command = responder.generate_write_command(uuid, value)
    ser.write(response_command.encode())
    return response


def resp(response: str) -> str:
    """Encodes the response as html file.
    Content is placed between <pre> tags
    :param response: """
    return flask.Response(response, mimetype="text/plain")


def run_server(responder_instance: Responder, ser_instance: serial):
    """Starts the webservice for client app HTTP requests
    :param responder_instance:
    :param ser_instance:
    """
    global responder
    responder = responder_instance

    global ser
    ser = ser_instance

    if not http_logging:
        log = logging.getLogger("werkzeug")
        log.setLevel(logging.ERROR)

    print(colored("http server starting", "red"))
    app.run(host="0.0.0.0", debug=False, port=6666)
