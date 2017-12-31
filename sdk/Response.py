#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# description:
# author:jack
# create_time: 2017/12/30

"""
处理完后构建返回数据
"""
import json
import re
from sdk.card.TextCard import TextCard


class Response(object):

    def __init__(self, request, session, nlu):
        '''

        :param request:
        :param session:
        :param nlu:
        '''
        self.request = request
        self.session = session
        self.nlu = nlu
        self.sourceType = self.request.getBotId()
        self.shouldEndSession = False
        self.needDetermine = False
        self.expectSpeech = False
        self.fallBack = False

    def setShouldEndSession(self, val):
        '''
        设置对话结束
        :param val:
        :return:
        '''
        if(val == True):
            self.shouldEndSession = True
        else:
            self.shouldEndSession = False

    def defaultResult(self):

        return {
            'status': 0,
            'msg': ''
        }

    def build(self, data):
        '''
        构造response 返回结果
        :param data:
        data = {
            'card': card,
            'directives': directives,
            'outputSpeech': string,
            'reprompt': string
        }
        :return:
        '''
        #TODO
        if(self.nlu and self.nlu.hasAsked()):
            self.shouldEndSession = False

        if('directives' in data.keys()):
            data['directives'] = data.get('directives')
        else:
            data['directives'] = []

        if('card' in data.keys()):
            data['card'] = data.get('card')
        else:
            data['card'] = None

        if('outputSpeech' in data.keys()):
            data['outputSpeech'] = data.get('outputSpeech')
        else:
            data['outputSpeech'] = None

        #
        if ('resource' in data.keys()):
            data['resource'] = data.get('resource')
        else:
            data['resource'] = None

        if ('reprompt' in data.keys()):
            data['reprompt'] = data.get('reprompt')
        else:
            data['reprompt'] = None


        if ('directives' in data.keys()):
            directives = data.get('directives')
        else:
            directives = []

        #TODO

        if(self.nlu):
            arr = self.nlu.toDirective()
            if(arr):
                directives = arr

        if(not data['outputSpeech'] and data['card'] and isinstance(data['card'], TextCard)):
            data['outputSpeech'] = data['card'].getContentData()

        if(self.nlu):
            if(self.nlu.toUpdateIntent()):
                context = self.nlu.toUpdateIntent()
            else:
                context = {}
        else:
            context = {}

        ret = {
            "version": "2.0",
            "context": context,
            "session": self.session.toResponse(),
            "response": {
                "directives":  directives,
                "shouldEndSession": self.shouldEndSession,
                "card": data['card'].getData(),
                "resource": data['resource'],
                "outputSpeech": self.formatSpeech(data['outputSpeech']),
                "reprompt": self.formatSpeech(data['reprompt'])
            }
        }

        if(self.needDetermine):
            ret['response']['needDetermine'] = self.needDetermine

        if(self.expectSpeech):
            ret['response']['expectSpeech'] = self.expectSpeech

        if(self.fallBack):
            ret['response']['fallBack'] = self.fallBack


        print('=====data = %s' % json.dumps(ret))
        return ret


    def formatSpeech(self, mix):
        '''
        通过正则 判断是纯文本还是ssml
        :param mix:
        :return:
        '''
        if(not mix or mix == 'null' or mix == ''):
            return None

        result = {}
        if(re.search(r'<speak>', mix)):
            result = {
                "type": "SSML",
                "ssml": mix
            }
        else:
            result = {
                "type": "PlainText",
                "text": mix
            }
        return result


    def illegalRequest(self):

        return {
            'status': 1,
            'msg': '非法请求'
        }

    def setNeedDetermine(self):

        self.needDetermine = True

    def setExpectSpeech(self, expectSpeech):
        '''
        通过控制expectSpeech来控制麦克风开关
        :param expectSpeech:
        :return:
        '''

        self.expectSpeech = expectSpeech

    def setFallBack(self):
        '''
        表示本次返回的结果为兜底结果
        :return:
        '''

        self.fallBack = True

if __name__ == '__main__':
    pass