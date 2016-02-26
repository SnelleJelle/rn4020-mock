import re
from termcolor import colored


class Responder:
    def __init__(self):
        self.__version = "V1.3 Python Mock"
        self.__message_aok = "AOK"
        self.__message_err = "ERR"
        self.__echo = False
        self.__message_echo_on = "Echo on"
        self.__message_echo_off = "Echo off"
        self.__connected = False
        self.__message_connection_start = "Connected"
        self.__message_connection_end = "Connection End"
        self.__responses = ""

        # Characteristics can hold 20 hexadecimal values(meaning 40 bytes).
        # They are never empty, always filled with 0's.
        default_value = "0000000000000000000000000000000000000000"
        self.__characteristics = {"00000000000000000000000000000001": default_value,
                                  "00000000000000000000000000000002": default_value,
                                  "00000000000000000000000000000003": default_value,
                                  "00000000000000000000000000000004": default_value,
                                  "00000000000000000000000000000005": default_value,
                                  "00000000000000000000000000000006": default_value,
                                  "00000000000000000000000000000007": default_value,
                                  "00000000000000000000000000000008": default_value,
                                  "00000000000000000000000000000009": default_value,
                                  "00000000000000000000000000000010": default_value}

        self.__handles = {"00000000000000000000000000000001": "0018",
                          "00000000000000000000000000000002": "001A",
                          "00000000000000000000000000000003": "001C",
                          "00000000000000000000000000000004": "001E",
                          "00000000000000000000000000000005": "0020",
                          "00000000000000000000000000000006": "0022",
                          "00000000000000000000000000000007": "0024",
                          "00000000000000000000000000000008": "0026",
                          "00000000000000000000000000000009": "0028",
                          "00000000000000000000000000000010": "002A"}

    def response_to(self, request: str) -> str:
        """Generate the appropriate response according to the RN4020 Microchip module.
        :param request: the complete command string
        """
        response = ""
        if self.__echo:
            response += request
        response += self.generate_response(request.rstrip()) + "\n"
        return response

    def generate_response(self, request: str) -> str:
        if request == "v":
            response = self.__version
        elif request == "+":
            response = self.__toggle_echo()
        elif re.match("^SUW,[0-9]{32},[0-9a-fA-F]{1,40}$", request):
            response = self.__suw(request)
        elif re.match("^SUR,[0-9]{32}$", request):
            response = self.__sur(request)

        # TODO: Tommy, feel free to implement these methods as desired
        # These codes are functional on the module but are useless here.
        # They will return AOK.
        elif re.match("^PC,[0-9]+,[0-9a-zA-Z]+,[0-9a-zA-Z]+$", request):
            response = self.__message_aok
        elif re.match("^PS,[0-9]{32}$", request):
            response = self.__message_aok
        elif request == "SS,C0000001":
            response = self.__message_aok
        elif request == "PZ":
            response = self.__message_aok
        elif re.match("^R,[1-2]$", request):
            response = self.__message_aok
        elif request == "SR":
            response = self.__message_aok
        else:
            response = self.__message_err
        return response

    def __suw(self, command: str) -> str:
        """Write value to characteristic"""
        split = command.split(",")
        uuid = split[1]
        value = split[2]
        self.__characteristics[uuid] = value

        return self.write(uuid, value, color="red")

    def __sur(self, command: str) -> str:
        """Read value from characteristic"""
        uuid = command.split(",")[1]

        return self.read(uuid, color="green")

    def write(self, uuid: str, value: str, color="blue") -> str:
        self.__characteristics[uuid] = value

        if self.__characteristics[uuid] == value:
            print(colored("\t-> Wrote " + value + " to " + uuid, color))
            return self.__message_aok
        else:
            print(colored("\t No such characteristic: " + uuid + " exists", color))
            return self.__message_err

    def read(self, uuid: str, color="blue") -> str:
        value = self.__characteristics[uuid]

        if value is None:
            print(colored("\t No such characteristic: " + uuid + " exists", color))
            return self.__message_err
        else:
            return value

    def generate_write_command(self, uuid: str, value: str) -> str:
        handle = self.__handles[uuid]
        command = "WV,{},{}. \n".format(handle, value)
        return command

    def __toggle_echo(self) -> str:
        """Toggles whether or not to append the request to the response"""
        self.__echo = not self.__echo
        if self.__echo:
            response = self.__message_echo_on
        else:
            response = self.__message_echo_off
        print(colored("\t-> Toggled " + response, "green"))
        return response

    def connect_client(self) -> str:
        """Clients can announce their connection via http.
         It will be broadcast on the serial port"""
        self.__connected = True
        response = self.__message_connection_start
        return response + "\n"

    def disconnect_client(self) -> str:
        """Clients can announce their disconnection via http.
         It will be broadcast on the serial port"""
        self.__connected = False
        response = self.__message_connection_end
        return response + "\n"
