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

import csvfile
import firebird
import mysql
import sqlite3
import simulator

# YAML mappings

class YamlCsvStorage(csvfile.CsvStorage, yaml.YAMLObject):
    yaml_tag = u'!csv'

class YamlFirebirdStorage(firebird.FirebirdStorage, yaml.YAMLObject):
    yaml_tag = u'!firebird'

class YamlMysqlStorage(mysql.MysqlStorage, yaml.YAMLObject):
    yaml_tag = u'!mysql'

class YamlSqlite3Storage(sqlite3.Sqlite3Storage, yaml.YAMLObject):
    yaml_tag = u'!sqlite3'

class YamlSimulatorStorage(simulator.SimulatorStorage, yaml.YAMLObject):
    yaml_tag = u'!simulator-storage'
