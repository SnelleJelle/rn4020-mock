import threading
import serial
import Responder
from httpserver import run_server
from serialport import run_serial_connection


def http_worker(responder_instance: Responder, ser_instance: serial):
    run_server(responder_instance, ser_instance)


def serial_worker(responder_instance: Responder, ser_instance: serial):
    run_serial_connection(responder_instance, ser_instance)


ser = serial.Serial(
    port="COM1",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    stopbits=serial.STOPBITS_ONE,
    rtscts=True)

responder = Responder.Responder()

threading.Thread(target=serial_worker, args=[responder, ser]).start()
threading.Thread(target=http_worker, args=[responder, ser]).start()
