# -*- coding: utf-8 -*-

import string
import hashlib


class BaseUAccount(object):
    """
    UCloud UAccount 账户管理的基类，主要包括不同操作的公共方法
    """
    def __init__(self, public_key, private_key):
        """
        初始化 BaseUAccount 对象

        @param public_key: string类型， 账户API公私钥的公钥
        @param private_key: string类型，账户API公私钥的私钥
        @return None，如果为非法的公私钥则抛出ValueError异常
        """
        self.__checkkey(public_key, private_key)
        self.__public_key = public_key
        self.__private_key = private_key


    def __checkkey(self, public_key, private_key):
        if not (public_key and private_key) or not isinstance(public_key, str) or not isinstance(private_key, str):
            raise ValueError('invalid API keys')

    def getPublicKey(self):
        return self.__public_key


    def signature(self, params):
        """
        根据签名算法计算签名
        https://docs.ucloud.cn/api/summary/signature

        @param params: dict类型, 请求参数
        @return string类型，本次文件下载的下载签名
        """

        items = list(params.items())
        items.sort()

        params_data = ""
        for key, value in items:
            params_data = params_data + str(key) + str(value)
        params_data = params_data + self.__private_key
    
        #use sha1 to encode keys
        hash_new = hashlib.sha1()
        hash_new.update(params_data.encode(encoding="utf-8"))
        hash_value = hash_new.hexdigest()
        return hash_value
