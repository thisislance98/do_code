import os
import sys
import json
import requests
import configparser


class DoCode:
    # @classmethod
    def set_key(self, api_key):
        self.api_key = api_key
        print("Key set!")

    def __init__(self, api_key=None):
        self.config = configparser.ConfigParser()
        self.secret = configparser.ConfigParser()
        project_root = os.path.dirname(os.path.realpath(__file__))
        self.config.read(os.path.join(project_root, "config.ini"))
        self.secret.read(os.path.join(project_root, "secret.ini"))

        self.api_key = api_key
        if "rapidapi" in self.secret:
            self.api_key = self.secret["rapidapi"]["api"]
            #print(self.api_key)
        if "rapidapi" in self.config:
            self.headers = {}
            self.headers["x-rapidapi-host"] = self.config["rapidapi"]["header_host"]
            self.base_url = self.config["rapidapi"]["base_url"]
            self.headers["x-rapidapi-key"] = self.api_key
            self.api_page = self.config["rapidapi"]["api_page"]
        else:
            print("[INFO] Config file not found")

    def do(self, action, param=None):
        if not self.api_key:
            print(
                f"You need to pass an api_key paramater. You can get this at RapidAPI ({self.api_page})"
            )
            return

        params = {"action": action, "param": param}
        url = self.base_url + "do"

        response = requests.request("GET", url, headers=self.headers, params=params)
        response_obj = json.loads(response.text)
        print(response.text, "\n")
        function_str = response_obj["code"]

        try:
            obj = compile(function_str, action, "exec")
            exec(obj, globals())
            if param != None:
                return eval(response_obj["function_name"] + "(param)")
            else:
                return eval(response_obj["function_name"] + "()")
        except Exception as ex:
            print(ex)
