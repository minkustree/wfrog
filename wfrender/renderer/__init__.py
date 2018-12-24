## Copyright 2009 Laurent Bovet <laurent.bovet@windmaster.ch>
##                Jordi Puigsegur <jordi.puigsegur@gmail.com>
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

import yaml

from . import chart
from . import data
from . import datatable
from . import file
from . import staticfile
from . import ftp
from . import http
from . import scheduler
from . import template
from . import value
from . import meteoclimatic
from . import wunderground
from . import pwsweather
from . import wettercom
from . import sticker
from . import openweathermap
from . import metofficewow


# YAML mappings

class YamlGoogleChartRenderer(chart.GoogleChartRenderer, yaml.YAMLObject):
    yaml_tag = '!chart'

class YamlGoogleWindRadarChartRenderer(chart.GoogleChartWindRadarRenderer, yaml.YAMLObject):
    yaml_tag = '!windradar'

class YamlDataRenderer(data.DataRenderer, yaml.YAMLObject):
    yaml_tag = '!data'

class YamlDataRenderer(datatable.DataTableRenderer, yaml.YAMLObject):
    yaml_tag = '!datatable'

class YamlFileRenderer(file.FileRenderer, yaml.YAMLObject):
    yaml_tag = '!file'

class YamlStaticFileRenderer(staticfile.StaticFileRenderer, yaml.YAMLObject):
    yaml_tag = '!staticfile'

class YamlFtpRenderer(ftp.FtpRenderer, yaml.YAMLObject):
    yaml_tag = '!ftp'

class YamlHttpRenderer(http.HttpRenderer, yaml.YAMLObject):
    yaml_tag = '!http'

class YamlSchedulerRenderer(scheduler.SchedulerRenderer, yaml.YAMLObject):
    yaml_tag = '!scheduler'

class YamlTemplateRenderer(template.TemplateRenderer, yaml.YAMLObject):
    yaml_tag = '!template'

class YamlValueRenderer(value.ValueRenderer, yaml.YAMLObject):
    yaml_tag = '!value'

class YamlMeteoclimaticRenderer(meteoclimatic.MeteoclimaticRenderer, yaml.YAMLObject):
    yaml_tag = '!meteoclimatic'

class YamlWundergroundRenderer(wunderground.WeatherUndergroundPublisher, yaml.YAMLObject):
    yaml_tag = '!wunderground'

class PwsWeatherRenderer(pwsweather.PwsWeatherPublisher, yaml.YAMLObject):
    yaml_tag = '!pwsweather'

class WetterComRenderer(wettercom.WetterComPublisher, yaml.YAMLObject):
    yaml_tag = '!wettercom'

class StickerRenderer(sticker.StickerRenderer, yaml.YAMLObject):
    yaml_tag = '!sticker'

class OpenWeatherMapPublisher(openweathermap.OpenWeatherMapPublisher, yaml.YAMLObject):
    yaml_tag = '!openweathermap'

class MetOfficeWowPublisher(metofficewow.MetOfficeWowPublisher, yaml.YAMLObject):
    yaml_tag = '!metofficewow'

