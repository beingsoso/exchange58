# -*- coding: utf-8 -*-
from exchanges58.exchange58.delivery_ontract import DeliveryContract
#%%
key	= 'xxx'
secret ='xxx'

api = DeliveryContract(key,secret)
#%%
wallet = api.get_wallet()
asset = api.get_coin_asset(2001)
#re = api.transfer2sub(2001,wallet['data']['balance'])
#%%
asset = api.get_coin_asset(2001)