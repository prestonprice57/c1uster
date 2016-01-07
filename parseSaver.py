import os, sys
from parse_rest.connection import register, ParseBatcher
from parse_rest.datatypes import Object

application_id = "uxliXmbidhv6n7zhKAP2BG6mVJiFdpNkms4zaVMw"
rest_api_key = "SF5ZKAFt44znr3vPBqfYMcYLeioegKDsjStvHfFz"

register(application_id, rest_api_key)

first_object = Object()
class Customers(Object):
    pass

test_data = Customers.Query.all()