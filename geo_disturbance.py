import json
from random import normalvariate as normal
from json import loads as json_loads
from json import dumps as json_dumps

def getRandom_1(inf, sup):
    mu = (inf + sup) / 2
    sigma = (sup - inf) / 6
    res = .0
    while not (inf < res < sup):
        res = normal(mu, sigma)
    return res
def getRandom_2(mu, delta):
    return getRandom_1(mu - delta, mu + delta)

'''
decimal
places   degrees          distance
-------  -------          --------
0        1                111  km
1        0.1              11.1 km
2        0.01             1.11 km
3        0.001            111  m
4        0.0001           11.1 m
5        0.00001          1.11 m
6        0.000001         11.1 cm
7        0.0000001        1.11 cm
8        0.00000001       1.11 mm

https://qastack.cn/gis/8650/measuring-accuracy-of-latitude-and-longitude
'''

def getRandomPosition(position):
    lng = position['lng']
    lat = position['lat']
    accuracy_lng = round(lng, 4) # 10 米精度
    accuracy_lat = round(lat, 4) # 10 米精度
    R = getRandom_2(accuracy_lng, 0.000025) # 5米宿舍
    Q = getRandom_2(accuracy_lat, 0.000025) # 5米宿舍
    lng = round(R, 6) # 使用六个小数位
    lat = round(Q, 6) # 使用六个小数位
    position['Q'] = Q
    position['R'] = R
    position['lng'] = lng
    position['lat'] = lat
    return position

def reverseGeo(geo_api_info):
    res = json_dumps(geo_api_info, ensure_ascii=False)
    res = res.replace('", "','","')
    res = res.replace('": ','":')
    res = res.replace(', "',',"')
    res = res.replace('}, {','},{')
    return res

def geoDisturbance(geo_api_info):
    geo_api_info = json_loads(geo_api_info)
    pt = geo_api_info['position']
    pt = getRandomPosition(pt)
    geo_api_info['position'] = pt
    return reverseGeo(geo_api_info)

if __name__ == "__main__":
    test = '{"type":"complete","position":{"Q":31.195403583978656,"R":121.45039052277646,"lng":121.450391,"lat":31.195404},"location_type":"html5","message":"Get geolocation success.Convert Success.Get address success.","accuracy":15,"isConverted":true,"status":1,"addressComponent":{"citycode":"021","adcode":"310104","businessAreas":[{"name":"龙华","id":"310104","location":{"Q":31.173178,"R":121.447517,"lng":121.447517,"lat":31.173178}},{"name":"徐家汇","id":"310104","location":{"Q":31.193701,"R":121.439121,"lng":121.439121,"lat":31.193701}},{"name":"岳阳","id":"310104","location":{"Q":31.20492,"R":121.45215300000001,"lng":121.452153,"lat":31.20492}}],"neighborhoodType":"","neighborhood":"","building":"","buildingType":"","street":"东安路","streetNumber":"134号","country":"中国","province":"上海市","city":"","district":"徐汇区","township":"枫林路街道"},"formattedAddress":"上海市徐汇区枫林路街道复旦大学上海医学院枫林路校区西区二号书院楼","roads":[],"crosses":[],"pois":[],"info":"SUCCESS"}'
    geo_api_info = json_loads(test)
    print(reverseGeo(geo_api_info) == test)
    print(test)
    print(reverseGeo(geo_api_info))
    print(repr(geoDisturbance(test)))