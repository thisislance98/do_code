import requests
import json

from requests import api
import pickledb
import configparser

# base_url = 'http://127.0.0.1:8000/'

headers = {
    "x-rapidapi-host": "docode.p.rapidapi.com",
}

base_url = "https://docode.p.rapidapi.com/"
db = pickledb.load("data.db", False)


def init(api_key):

    db.set("api_key", api_key)
    
def _get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['rapidapi']['api']


def fix(code, exception_str):
    params = {"code": code, "exception_str": exception_str}
    url = base_url + "fix"

    api_key = db.get("api_key")
    
    if not api_key:
        api_key = _get_api_key()
        
    if not api_key:
        print("You need to pass an api_key paramater. You can get this at RapidAPI")
        return

    headers[
        "x-rapidapi-key"
    ] = api_key

    response = requests.request("GET", url, headers=headers, params=params)
    return response.text


def do(action, param=None, api_key=None):

    if api_key != None:
        db.set("api_key", api_key)
        db.dump()

    api_key = db.get("api_key")
    
    if not api_key:
        api_key = _get_api_key()
        
    if not api_key:
        print("You need to pass an api_key paramater. You can get this at RapidAPI")
        return

    params = {"action": action, "param": param}

    #api_key = db.get("api_key")
    headers[
        "x-rapidapi-key"
    ] = api_key
    url = base_url + "do"

    response = requests.request("GET", url, headers=headers, params=params)
    response_obj = json.loads(response.text)
    print(response.text)
    function_str = response_obj["code"]
    obj = compile(function_str, action, "exec")

    try:
        obj = compile(function_str, action, "exec")
        exec(obj, globals())
        if param != None:
            return eval(response_obj["function_name"] + "(param)")
        else:
            return eval(response_obj["function_name"] + "()")
    except Exception as e:
        print(function_str)
        print("Trying to fix exception: " + str(e))

        fixed_code = fix(function_str, str(e))
        print("\n\nfixed code")
        print(fixed_code)
        try:
            obj = compile(fixed_code, action, "exec")
            exec(obj)

            if param != None:
                return eval(response_obj["function_name"] + "(param)")
            else:
                return eval(response_obj["function_name"] + "()")

        except Exception as e:
            print("could not fix code")
            print(e)


a = do(
    "print out ten random characters"
)
print(a)
