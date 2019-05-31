import requests
import json
import time
import hmac
import traceback

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context

# This is the 2.11 Requests cipher string, containing 3DES.
CIPHERS = (
    'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:'
    'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES:!aNULL:'
    '!eNULL:!MD5'
)


class DESAdapter(HTTPAdapter):
    """
    A TransportAdapter that re-enables 3DES support in Requests.
    """
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).proxy_manager_for(*args, **kwargs)


#r = s.get('https://some-3des-only-host.com/some-path')

class Client(object):

    def __init__(self, api_key, api_seceret_key):

        self.API_KEY = api_key
        self.API_SECRET_KEY = api_seceret_key
        self.SignatureMethod='HmacSHA256'
        self.SignatureVersion=2
        self.base_url = 'https://openapi.58ex.com'
        self.s =  requests.Session()
        
    def _getSign(self,params, timestamp):
        
        params = self._get_param(params,timestamp)
        bSecretKey = bytes(self.API_SECRET_KEY, encoding='utf8')
    
        sign = ''
        for key in sorted(params.keys()):
            value = str(params[key])
            sign += key + '=' + value + '&'
    
        bSign = bytes(sign[:-1], encoding='utf8')
    
        mySign = hmac.new(bSecretKey, bSign, digestmod='sha256').hexdigest()
        return mySign

    def _get_param(self,params,timestamp):
        
        params['AccessKeyId'] = self.API_KEY
        params['SignatureMethod'] = self.SignatureMethod
        params['SignatureVersion'] = self.SignatureVersion
        params['Timestamp'] = timestamp
        return params
        
    def _get_header(self,sign,timestamp):
        header = {'X-58COIN-APIKEY':self.API_KEY,
          'Timestamp':str(timestamp),
          'Signature':sign
        }
        return header
        
    def request_sign(self, method, request_path, params = {}):
        
        
        # url
        url = self.base_url + request_path
        self.s.mount(url, DESAdapter())
        
        timestamp = int(round(time.time() * 1000))
        sign = self._getSign(params,timestamp)
        header = self._get_header(sign, timestamp)

        # send request
        response = None
        #print("url:", url)
#        print("headers:", timestamp)
        #print("body:", body)
        try:
            if method == 'GET':
                response = self.s.get(url, headers=header,params =params).json()
            else :
                response = self.s.post(url, data=params, headers=header).json()
        except:
            print('Invalid Response: %s' % response.text)
            traceback.print_exc()
        return response
            
    def request_without_sign(self, request_path, params = {}):
        try:
            u = self.base_url + request_path
            re = requests.get(u,params = params).json()
        except:
            traceback.print_exc()
        return re

