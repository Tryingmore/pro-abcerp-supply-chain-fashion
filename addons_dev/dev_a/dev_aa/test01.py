import request

ip_address = request.httprequest.environ['REMOTE_ADDR']
print(ip_address)