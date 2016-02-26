import serial
import time
from termcolor import colored
from Responder import Responder


def run_serial_connection(responder: Responder, ser: serial):
    """Constantly monitors the serial connection and responds back
    :param responder:
    :param ser:
    """
    print(colored("connected to: " + ser.portstr, "green"))
    while True:
        try:
            read_text = ser.readline()
            request = read_text.decode("utf-8")
            print(colored("--Received:\n", "red"), end="")
            print(colored(request.replace("\n", "\n[Newline]"), "green"))

            response = responder.response_to(request)
            ser.write(response.encode())
            print(colored("--Responded:\n", "red"), end="")
            print(colored(response.replace("\n", "\n[Newline]"), "green"))
            time.sleep(.1)

        except ser.SerialTimeoutException:
            print("Data could not be read")
            time.sleep(1)
