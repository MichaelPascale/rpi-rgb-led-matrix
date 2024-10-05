import math
import requests as rq
from datetime import datetime as dt
from datetime import timezone as tz

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

stops = {}
trains = []
now = dt.now(tz.utc)

for station in stations:
  print(station)
  data = rq.get('https://api-v3.mbta.com/predictions?filter[stop]=%s&include=stop' % station)
  
  assert data.status_code == 200
  data = data.json()


  def get_stop(s):
    assert s['type'] == 'stop'
    a = s['attributes']
    print(a['name'])
    return s['id'], a['name'], a['platform_name']
    
  stops.update({s[0]: s[1:] for s in map(get_stop, data['included'])})
  
  for prediction in data['data']:
    assert prediction['type'] == 'prediction'
    
    time = dt(1970, 1, 1, tzinfo=tz.utc)
    if prediction['attributes']['arrival_time'] is not None:
      time = dt.fromisoformat(prediction['attributes']['arrival_time'])
    
    train = {
      'route': prediction['relationships']['route']['data']['id'],
      'status': prediction['attributes']['status'],
      'time': time,
      'arrives': math.floor((now - time).total_seconds() / 60),
      # 'departs': dt.fromisoformat(prediction['attributes']['departure_time']),
      'stop': prediction['relationships']['stop']['data']['id'],
      'station':  stops[prediction['relationships']['stop']['data']['id']][0],
      'platform': stops[prediction['relationships']['stop']['data']['id']][1]
    }
    
    trains.append(train)


