from rest_framework.response import Response
from rest_framework import utils
import json, os, copy, re
# 继承自一个文件
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
# 注意写完之后要在setings里面进行注册 在MIDDLEARE里面注册使用
class myMiddle(MiddlewareMixin):

    def process_request(self,request):
        print('===============================================下面是新的一条日志====================================================')
        print('拦截请求的地址：',request.path,'请求的方法：',request.method)
        print('====================================headers 头信息====================================================')
        for key in request.META:
            if key[:5] == 'HTTP_':
                print(key, request.META[key])
        # if request.body:
        #     print('====================================request body信息==================================================')
            # request_dic = json.loads(request.body, encoding='utf-8')
            # print(request_dic)

    def process_exception(self, request, exception):
        print('发生错误的请求地址', request.path, exception.__str__)
        return Response({"message": "出现了无法预料的view视图错误", "errorCode": 1, "data": {}})

    def process_response(self,request,response):
        # response_dic = json.loads(response.content,encoding='utf-8')
        print('====================================response 日志信息=================================================')
        if request.path is not '/' and not re.match(r'/swagger.*', request.path, re.I) and not re.match(r'/redoc/.*', request.path, re.I):
            if (type(response.content.decode('utf-8'))) == str:
                print(response.content.decode('utf-8'))
        return response


class JsondataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # print('测试')
        # print(response.data)
        # print(response.status_code)
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        print(type(response.data))
        print(type(response))
        if request.method == 'DELETE':
            pass
            print('删除数据测试')
            print(response.data)
            if response.status_code == 204:
                response.data = {"message": '删除成功', "errorCode": 0, "data": {}}
            else:
                if response.data.get('detail'):
                    data = {"message": response.data.get('detail'), "errorCode": 1, "data": {}}
                else:
                    data = {"message": 'error', "errorCode": 1, "data": response.data}
                response.data = data
            response._is_rendered = False
            response.render()
        else:
            if request.path is not '/' and not re.match(r'/swagger.*', request.path, re.I) and not re.match(r'/redoc/.*', request.path, re.I):
            # if type(response.data) == dict or utils.serializer_helpers.ReturnDict: # 兼容只有返回 dict 以及 ReturnDict 时才做处理  or utils.serializer_helpers.ReturnDict
                if response.status_code != 200:
                    if response.data.get('detail'):
                        data = {"message": response.data.get('detail'), "errorCode": 1, "data": {}}
                    else:
                        data = {"message": 'error', "errorCode": 1, "data": response.data}
                    response.data = data
                else:
                    if response.data.get('message'): # 兼容APIView返回data的设置
                        pass
                    elif response.data.get('count'): # 兼容分页返回data的设置
                        response.data['errorCode'] = 0
                        response.data['message'] = 'ok'
                    else:
                        data = {"message": 'ok', "errorCode": 0, "data": response.data}
                        response.data = data
                response._is_rendered = False
                response.render()
        return response