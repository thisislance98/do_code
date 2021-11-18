import urllib
import requests
import json
import pickledb

# base_url = 'http://127.0.0.1:8000/'

headers = {
    'x-rapidapi-host': "docode.p.rapidapi.com",
}

base_url = "https://docode.p.rapidapi.com/"
db = pickledb.load('data.db', False)

def init(api_key):

    db.set('api_key', api_key)


def fix(code,exception_str):
    params = {'code': code, 'exception_str': exception_str}
    url = base_url + 'fix'

    api_key = db.get('api_key')
    if not api_key:
        print("You need to pass an api_key paramater. You can get this at RapidAPI")
        return

    headers['x-rapidapi-key'] = api_key #"8f5e5e4805msh1fed7957d21a974p12184ajsn7f872e170ee7"


    response = requests.request("GET", url, headers=headers, params=params)
    return response.text

def do(action,param=None,api_key=None):

    if api_key != None:
        db.set('api_key',api_key)
        db.dump()

    api_key = db.get('api_key')
    if not api_key:
        print("You need to pass an api_key paramater. You can get this at RapidAPI")
        return

    params = {'action': action, 'param': param}

    api_key = db.get('api_key')
    headers['x-rapidapi-key'] = api_key #"8f5e5e4805msh1fed7957d21a974p12184ajsn7f872e170ee7"
    url = base_url + 'do'

    # url = "https://fastapi-test-chris.herokuapp.com/test?" + encoded_params

    response = requests.request("GET", url, headers=headers, params=params)
    response_obj = json.loads(response.text)
    print(response.text)
    function_str = response_obj['code']
    obj = compile(function_str,action,'exec')


    try:
        obj = compile(function_str, action, 'exec')
        exec(obj)
        if param != None:
            return eval(response_obj['function_name'] + '(param)')
        else:
            return eval(response_obj['function_name'] + '()')
    except Exception as e:
        print(function_str)
        print('Trying to fix exception: ' + str(e))

        fixed_code = fix(function_str, str(e))
        print('\n\nfixed code')
        print(fixed_code)
        try:
            obj = compile(fixed_code, action, 'exec')
            exec(obj)

            if param != None:
                return eval(response_obj['function_name'] + '(param)')
            else:
                return eval(response_obj['function_name'] + '()')

        except Exception as e:
            print("could not fix code")
            print(e)




a = do('print out ten random characters') #,api_key="8f5e5e4805msh1fed7957d21a974p12184ajsn7f872e170ee7")
print(a)

# import requests
#
# url = "https://docode.p.rapidapi.com/test"
#
# querystring = {"action":"create a text file with some text in it", "param": "test.txt"}
#
# headers = {
#     'x-rapidapi-host': "docode.p.rapidapi.com",
#     'x-rapidapi-key': "8f5e5e4805msh1fed7957d21a974p12184ajsn7f872e170ee7"
#     }

# response = requests.request("GET", url, headers=headers, params=querystring)
#
# print(response.text)