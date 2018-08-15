# -*- coding: utf-8 -*-

import requests
import re
from ucloud.ufile import config
from ucloud.logger import logger


API_URL = "https://api.ucloud.cn"
TIMEOUT = 60

# base error class
class UAccountError(Exception):
  pass

class ServerError(UAccountError):
  def __init__(self, statuscode, reason):
    self.statusCode = statuscode
    super(ServerError, self).__init__(reason)
  
class ClientError(UAccountError):
  def __init__(self, message):
    super(ClientError, self).__init__(message)

class APIError(UAccountError):
  """API error exception for UAccount SDK"""
  def __init__(self, retCode, message):
    message = 'UAccount API Error: RetCode=%d Message="%s"' %(retCode, message)
    self.code = retCode
    super(APIError, self).__init__(message)


def checkHttpAPIError(result):
	if result.status_code != 200:
		body = result.text
		raise ServerError(result.status_code, body)
	try:
		body = result.json()
	except Exception as e:
		raise ClientError("unkown error")
	if body["RetCode"] != 0:
		raise APIError(body["RetCode"], body.get(u"Message"))
	return body


def _post(data):
    """
    @param data: dict 类型，请求体
    @return jsonbody: 如果http状态码不为200 或者RetCode不为0，则抛出异常；否则返回dict类型，键值对类型分别为string, unicode string类型
    """
    response = requests.post(API_URL, data=data, timeout=TIMEOUT)
    jsonbody = checkHttpAPIError(response)
    return jsonbody


def _get(payload):
    """
    @param payload: dict 类型，请求参数
    @return jsonbody: 如果http状态码不为200 或者RetCode不为0，则抛出异常；否则返回dict类型，键值对类型分别为string, unicode string类型
    """
    response = requests.get(API_URL, params=payload, timeout=TIMEOUT)
    jsonbody = checkHttpAPIError(response)
    return jsonbody

