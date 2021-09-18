from django.http import JsonResponse

class HttpCode(object):
    ok = 200
    params_error = 400
    unauth = 401
    method_error = 405
    server_error = 500

def result(code=HttpCode.ok,message='',data=None,kwargs=None):
    json_dict = {'code':code,'message':message,'data':data}

    if kwargs and isinstance(kwargs,dict) and kwargs.keys():
        json_dict.update(kwargs)

    return JsonResponse(json_dict)

def ok():
    return result()

def params_error():
    return result(code=HttpCode.params_error, message='账号或密码错误')

def unauth():
    return result(code=HttpCode.unauth, message='您没有该权限')

def method_error():
    return result(code=HttpCode.method_error, message='请求方法错误[POST/GET]')

def server_error():
    return result(code=HttpCode.server_error, message='服务器错误')