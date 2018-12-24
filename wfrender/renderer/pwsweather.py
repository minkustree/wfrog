## Copyright 2010 Jordi Puigsegur <jordi.puigsegur@gmail.com>
##                derived from PyWeather by Patrick C. McGinty
##
##  This file is part of wfrog
##
##  wfrog is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import math
import logging
import sys
import time
import wfcommon.database
from wfcommon.formula.base import LastFormula
from wfcommon.formula.base import SumFormula
try:
    from wfrender.datasource.accumulator import AccumulatorDatasource
except ImportError as e:
    from datasource.accumulator import AccumulatorDatasource
from wfcommon.units import HPaToInHg
from wfcommon.units import CToF
from wfcommon.units import MmToIn
from wfcommon.units import MpsToMph

class PwsWeatherPublisher(object):
    """
    Render and publisher for pwsweather.com. It is a wrapper 
    around PyWeather, thus needs this package installed on your 
    system, version 0.9.1 or superior. (sudo easy_install weather)

    [ Properties ]

    id [string]:
        PWS station ID.

    password [string]:
        password.

    period [numeric]:
        The update period in seconds.

    storage: 
        The storage service.
    """

    id = None
    password = None
    publisher = None
    storage = None
    alive = False

    logger = logging.getLogger("renderer.pwsweather")

    def render(self, data={}, context={}):
        try:
            assert self.id is not None, "'pws.id' must be set"
            assert self.password is not None, "'pws.password' must be set"
            assert self.period is not None, "'pws.period' must be set"

            self.logger.info("Initializing PWS publisher (station %s)" % self.id)
            import weather.services
            self.publisher = weather.services.PwsWeather(self.id, self.password)

            self.alive = True

            accu = AccumulatorDatasource()
            accu.slice = 'day'
            accu.span = 1
            accu.storage = self.storage
            accu.formulas = {'current': {
                 'temp' : LastFormula('temp'),
                 'dew_point': LastFormula('dew_point'),
                 'hum' : LastFormula('hum'),
                 'pressure' : LastFormula('pressure'),
                 'wind' : LastFormula('wind'),
                 'wind_deg' : LastFormula('wind_dir'),
                 'gust' : LastFormula('wind_gust'),
                 'gust_deg' : LastFormula('wind_gust_dir'),
                 'rain_rate' : LastFormula('rain_rate'),
                 'rain_fall' : SumFormula('rain'), 
                 'utctime' : LastFormula('utctime') } }

            accu_month = AccumulatorDatasource()
            accu_month.slice = 'month'
            accu_month.span = 1
            accu_month.storage = self.storage
            accu_month.formulas = {'current': {'rain_fall' : SumFormula('rain') } }

            accu_year = AccumulatorDatasource()
            accu_year.slice = 'year'
            accu_year.span = 1
            accu_year.storage = self.storage
            accu_year.formulas = {'current': {'rain_fall' : SumFormula('rain') } }

            while self.alive:
                try:
                    data = accu.execute()['current']['series']
                    index = len(data['lbl'])-1
                    data_month= accu_month.execute()['current']['series']
                    index_month = len(data_month['lbl'])-1
                    data_year = accu_year.execute()['current']['series']
                    index_year = len(data_year['lbl'])-1

                    params = {
                        # <float> pressure: in inches of Hg
                        'pressure' : HPaToInHg(data['pressure'][index]),
                        # <float> dewpoint: in Fahrenheit
                        'dewpoint' : CToF(data['dew_point'][index]),
                        # <float> humidity: between 0.0 and 100.0 inclusive
                        'humidity' : data['hum'][index],
                        # <float> tempf: in Fahrenheit
                        'tempf' : CToF(data['temp'][index]),
                        # <float> rainin: inches/hour of rain
                        'rainin' : MmToIn(data['rain_rate'][index]),
                        # <float> rainday: total rainfall in day (localtime)
                        'rainday' : MmToIn(data['rain_fall'][index]),
                        # <float> rainmonth:  total rainfall for month (localtime)
                        'rainmonth' : MmToIn(data_month['rain_fall'][index_month]),
                        # <float> rainyear:   total rainfall for year (localtime)
                        'rainyear' : MmToIn(data_year['rain_fall'][index_year]),
                        # <string> dateutc: date "YYYY-MM-DD HH:MM:SS" in GMT timezone
                        'dateutc' : data['utctime'][index].strftime('%Y-%m-%d %H:%M:%S'),
                        # <float> windgust: in mph
                        'windgust' : MpsToMph(data['gust'][index]),
                        # <float> windspeed: in mph
                        'windspeed' : MpsToMph(data['wind'][index]),
                        # <float> winddir: in degrees, between 0.0 and 360.0
                        'winddir' : data['wind_deg'][index] }

                    # Do not send parameters that are null (None), but don't remove zeroes (0.0)
                    # from above only dateutc is a mandatory parameter.
                    params = dict([p_v for p_v in [(p,v) for p,v in params.items()] if p_v[1] is not None])
                    self.logger.info("Publishing PWS data: %s " % str(params))
                    self.publisher.set(**params)
                    response = self.publisher.publish()               
                    self.logger.info('Result PWS publisher: %s' % str(response))

                except Exception as e:
                    self.logger.exception(e)

                time.sleep(self.period)

        except Exception as e:
            self.logger.exception(e)
            raise

    def close(self):
        self.alive = False

