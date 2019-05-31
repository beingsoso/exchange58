from exchanges58.exchanges58.client import Client


class DeliveryContract(Client):
    
    # https://github.com/58COIN/open-api-docs/wiki/Regular-API-Reference
    
    
    def __init__(self, api_key, api_seceret_key):
        Client.__init__(self, api_key, api_seceret_key)

    
    def get_contract_list(self):
        u = '/v1/regular/contract/list'
        return self.request_without_sign(u)
       
    def get_coin_asset(self, contractId):
        u = '/v1/regular/account/asset'
        p = {'contractId':contractId}
        return self.request_sign('GET',u,p)
    
    
    def get_wallet(self):
        u = '/v1/regular/account/wallet'
        return self.request_sign('GET',u)
    
    def transfer2sub(self, contractId,amount):
        u = '/v1/regular/account/transfer'
        p = {'contractId':contractId,
          'action':1,
          'amount':amount
          }
        return self.request_sign('POST',u,p)
    
    
