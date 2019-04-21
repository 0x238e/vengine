from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

channel_layer = get_channel_layer()

# Create your views here.

def mockEventList(request):
  res = HttpResponse()
  res['Content-Type'] = 'application/json'
  res['Access-Control-Allow-Origin'] = 'http://v.noinfinity.top'
  res.content = '''
[{
  "type": "update",
  "event": {
    "id": "9a7590ad-8d13-40de-9b1b-1714d0f84328",
    "type": {
      "name": "超车",
      "level": "is-danger"
    },
    "from": "0xcdfead4dfadbc714ced0d4b1eddebbb4c18d99e4",
    "to": "0x02275aEdd72D6406D20A21De9837737dc8501dC2",
    "expire": 1555826003837,
    "price": 197,
    "userlevel": 6,
    "data": {
      "gps": ["-74.7014", "98.8020"]
    },
    "decider": "car",
    "status": "accept"
  }
}, {
  "type": "update",
  "event": {
    "id": "c8108bfa-df01-4736-9264-19d1ad937746",
    "type": {
      "name": "换道",
      "level": "is-warning"
    },
    "from": "0xbcf808ebb924b3a34563d054d5ed0b4b38d1b686",
    "to": "0x02275aEdd72D6406D20A21De9837737dc8501dC2",
    "expire": 1555826028641,
    "price": 306,
    "userlevel": 7,
    "data": {
      "gps": ["-35.0395", "-80.9195"]
    },
    "decider": "car",
    "status": "reject"
  }
}, {
  "type": "update",
  "event": {
    "id": "96df607b-e94c-47d4-b790-a2099be7ff8f",
    "type": {
      "name": "换道",
      "level": "is-warning"
    },
    "from": "0xdc9bc50a3d6fa25cf10453b3b7e2d09613c0b7db",
    "to": "0x02275aEdd72D6406D20A21De9837737dc8501dC2",
    "expire": 1555826029015,
    "price": 457,
    "userlevel": 0,
    "data": {
      "gps": ["-3.9431", "-87.3783"]
    },
    "decider": "car",
    "status": "reject"
  }
}]
'''
  return res

def eventList(request):
  if request.method == 'POST':
    datas = json.loads(request.body)
    for data in datas:
      if cache.get(data['event']['to']):
        async_to_sync(channel_layer.send)(cache.get(data['event']['to']), {
            "type": "vevent.send",
            "data": data,
        })
    return HttpResponse()