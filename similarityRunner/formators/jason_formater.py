import json

from interfaces.OutputFormaterInterface import OutputFormaterInterface


class JsonFormater(OutputFormaterInterface):

    def format(self, data: dict) -> json:
        jsondata = json.dumps(data, indent=4)
        return jsondata
