import os
import requests
import numpy as np
from datetime import datetime as dt


class OpenWeather:

    # Time of last weather update
    last = dt.fromtimestamp(0)
    # Cached data
    data = {}

    def __init__(self, key, lat, lon, units='imperial', freq=10):
        self.key  = key       # openweather api key
        self.lat  = lat       # latitude
        self.lon  = lon       # longitude
        self.freq = freq * 60 # refresh in seconds
        self.uri  = f"https://api.openweathermap.org/data/3.0/onecall?appid={key}&units={units}&lat={lat}&lon={lon}"

    def _update(self):
        # do not refresh if the update frequency has not elapsed
        if ((dt.now() - self.last).total_seconds() < self.freq):
            return False
        else:
            
            try:
                response = requests.get(OW_URI)
                assert response.status_code == 200
                self.data = response.json()

            except:
                self.data = {}
                return False
            
            else:
                self.last = dt.now()
                return True
    
    def current(self):
        self._update()
        return self.data['current']
    
    def precipitation(self):
        self._update()
        return np.array(
            [*map(lambda d: (d['dt'], d['precipitation']), self.data['minutely'])],
            dtype=np.float32 #[('time', np.int32), ('chance', np.float32)]
        )


