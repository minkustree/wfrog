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

from . import csvfile
from . import firebird
from . import mysql
from . import sqlite3
from . import simulator

# YAML mappings

class YamlCsvStorage(csvfile.CsvStorage, yaml.YAMLObject):
    yaml_tag = '!csv'

class YamlFirebirdStorage(firebird.FirebirdStorage, yaml.YAMLObject):
    yaml_tag = '!firebird'

class YamlMysqlStorage(mysql.MysqlStorage, yaml.YAMLObject):
    yaml_tag = '!mysql'

class YamlSqlite3Storage(sqlite3.Sqlite3Storage, yaml.YAMLObject):
    yaml_tag = '!sqlite3'

class YamlSimulatorStorage(simulator.SimulatorStorage, yaml.YAMLObject):
    yaml_tag = '!simulator-storage'
