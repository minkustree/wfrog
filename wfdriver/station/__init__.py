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

from . import simulator
from . import wmrs200
from . import wmr928nx
from . import wmr200
from . import vantagepro
from . import vantagepro2
from . import wh1080
from . import wh3080
from . import ws23xx
from . import ws28xx
from . import auto

# YAML mappings and registration for auto-detect

class YamlAutoDetectStation(auto.AutoDetectStation, yaml.YAMLObject):
    yaml_tag = '!auto'

class YamlWMR200Station(wmr200.WMR200Station, yaml.YAMLObject):
    yaml_tag = '!wmr200'
auto.stations.append(wmr200)

class YamlWMRS200Station(wmrs200.WMRS200Station, yaml.YAMLObject):
    yaml_tag = '!wmrs200'
auto.stations.append(wmrs200)

class YamlWMR928NXStation(wmr928nx.WMR928NXStation, yaml.YAMLObject):
    yaml_tag = '!wmr928nx'
auto.stations.append(wmr928nx)

class YamlVantageProStation(vantagepro.VantageProStation, yaml.YAMLObject):
    yaml_tag = '!vantagepro'

class YamlVantageProStation(vantagepro2.VantageProStation, yaml.YAMLObject):
    yaml_tag = '!vantagepro2'

class YamlWH1080Station(wh1080.WH1080Station, yaml.YAMLObject):
    yaml_tag = '!wh1080'
    
class YamlWH3080Station(wh3080.WH3080Station, yaml.YAMLObject):
    yaml_tag = '!wh3080'

class YamlWS2300Station(ws23xx.WS2300Station, yaml.YAMLObject):
    yaml_tag = '!ws2300'    

class YamlWS28xxStation(ws28xx.WS28xxStation, yaml.YAMLObject):
    yaml_tag = '!ws28xx'
auto.stations.append(ws28xx)

class YamlRandomSimulator(simulator.RandomSimulator, yaml.YAMLObject):
    yaml_tag = '!random-simulator'
auto.stations.append(simulator)

