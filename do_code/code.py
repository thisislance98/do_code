import urllib
import requests
import json

base_url = 'http://127.0.0.1:8000/'

def fix(code,exception_str):
    params = {'code': code, 'exception_str': exception_str}
    encoded_params = urllib.parse.urlencode(params)
    url = base_url + 'fix?' + encoded_params
    response = requests.request("GET", url, headers={}, data={})
    return response.text

def do(action,param=None):

    params = {'action': action, 'param': param}
    encoded_params = urllib.parse.urlencode(params)


    url = base_url + 'test?' + encoded_params
    # url = "https://fastapi-test-chris.herokuapp.com/test?" + encoded_params

    response = requests.request("GET", url, headers={}, data={})
    response_obj = json.loads(response.text)
    print(response.text)
    function_str = response_obj['code']
    obj = compile(function_str,action,'exec')


    try:
        obj = compile(function_str, action, 'exec')
        print("executing:")
        print(function_str)

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




a = do('print out ten random characters')
print(a)