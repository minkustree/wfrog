#!/usr/bin/env python
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

''' Bootstrap script for running wfrog components from one place. '''

import sys
import os.path
import logging
import getpass

import wflogger.wflogger
import wfrender.wfrender
import wfcommon.customize
import wflogger.setup

def get_home_wfrog_dir():
    if sys.platform == 'win32':
        import winreg
        return winreg.ExpandEnvironmentStrings('%APPDATA%\\Wfrog\\')
    else:
        return os.path.expanduser("~"+getpass.getuser())+'/.wfrog/'



class ComponentManager():

    @classmethod
    def default_opt_parser(cls):
        import optparse
        opt_parser = optparse.OptionParser(conflict_handler='resolve')

        opt_parser.add_option("-B", "--backend", action="store_true", dest="backend", help="Starts the logger and the driver only.")
        opt_parser.add_option("-R", "--renderer", action="store_true", dest="renderer", help="Starts the renderer only.")
        opt_parser.add_option("-C", "--customize", action="store_true", dest="customize", help="Prepare the config files for customizing wfrog. Safe operation, it does not overwrite an existing custom config.")
        opt_parser.add_option("-S", "--setup", action="store_true", dest="setup", help="Define the settings interactively.")
        opt_parser.add_option('-w', '--cwd', action='store_true', dest='cwd', help='Use the current working directory for data instead of the default one.')
        opt_parser.add_option("-f", "--config", dest="config_file", help="Configuration file (in yaml)", metavar="CONFIG_FILE")
        opt_parser.add_option("-s", "--settings", dest="settings", help="Settings file (in yaml)", metavar="SETTINGS_FILE")
        opt_parser.add_option("-m", "--mute", action="store_true", dest="mute", help="Skip the setup of user settings. Do not issues any questions but fails if settings are missing.")

        return opt_parser

    def __init__(self, opt_parser=None):
        ''' Note: modifies opt_parser options '''
        if not opt_parser:
            opt_parser = ComponentManager.default_opt_parser()
        self.candidate_logger = wflogger.wflogger.Logger(opt_parser)
        self.candidate_renderer = wfrender.wfrender.RenderEngine(opt_parser)
        (self.options, _) = opt_parser.parse_args()
    
    def get_component(self):
        if self.options.renderer:
            return self.candidate_renderer 
        else:
            return self.candidate_logger

class SettingsAndConfigManager():
    SETTINGS_FILE = 'settings.yaml'
    GLOBAL_CONF_DIR = '/etc/wfrog'

    def __init__(self, wfrog_home=get_home_wfrog_dir(), 
                       wfrog_root=os.path.dirname(os.path.realpath(__file__)),
                       global_conf_dir=GLOBAL_CONF_DIR,
                       settings=None, config_file=None, backend=False, renderer=False):
        self.global_conf_dir = global_conf_dir
        self.wfrog_home = wfrog_home
        self.wfrog_root = wfrog_root

        # Broken out from options to remove dependency on parsed options structure
        self.settings = settings
        self.config_file = config_file
        self.backend = backend
        self.renderer = renderer

        self._init_settings()
        self._init_config()

    def _init_settings(self):
        self.settings_def = os.path.normpath(os.path.abspath(os.path.join(self.wfrog_root, 'wfcommon', 'config','settings-definition.yaml')))
        if self.settings:
            self.settings = os.path.abspath(self.settings)
        else:
            candidates = [ os.path.join(self.wfrog_home, self.SETTINGS_FILE),
                           os.path.join(self.global_conf_dir, self.SETTINGS_FILE),
                           os.path.join(os.curdir, self.SETTINGS_FILE) ]
            for candidate in candidates:
                if os.path.exists(candidate):
                    self.settings = candidate
                    break

    def _init_config(self):
        if not self.config_file:
            if self.backend:
                config_file = os.path.join('wflogger','config','wflogger.yaml')
            elif self.renderer:
                config_file = os.path.join('wfrender','config','wfrender.yaml')
            else:
                config_file = os.path.join('wflogger','config','wfrog.yaml')

        if os.path.exists(os.path.join(self.wfrog_home, config_file)):
            config_dir = self.wfrog_home
        elif os.path.exists(os.path.join(self.global_conf_dir, config_file)):
            config_dir = self.global_conf_dir
        elif os.path.exists(os.path.join(os.curdir, config_file)):
            config_dir = os.path.abspath(os.curdir)
        else:
            config_dir = self.wfrog_root

        self.config_file = os.path.join(config_dir, config_file)

    def get_config_file(self):
        return self.config_file

    def get_settings(self):
        return self.settings

    def setup_settings(self, user):
        if user == 'root':
            settings_file = os.path.join(self.global_conf_dir, self.SETTINGS_FILE)
        else:
            settings_file = os.path.join(self.wfrog_home, self.SETTINGS_FILE)
        self.settings = wflogger.setup.SetupClient().setup_settings(self.settings_def, self.settings, settings_file)

def main(wfrog_home=get_home_wfrog_dir(), 
         wfrog_root=os.path.dirname(os.path.realpath(__file__)) ):

    component_manager = ComponentManager()
    options = component_manager.options

    sac_manager = SettingsAndConfigManager(wfrog_home, wfrog_root, 
                    settings=options.settings, 
                    config_file=options.config_file, 
                    backend=options.backend, 
                    renderer=options.renderer)

    user = getpass.getuser()

    if not options.cwd and not user=='root':
        try:
            os.makedirs(sac_manager.wfrog_home)
        except:
            pass
        os.chdir(sac_manager.wfrog_home)

    if user == 'root':
        customize_dir = sac_manager.global_conf_dir
    else:
        customize_dir = sac_manager.wfrog_home
    
    if options.customize:
        wfcommon.customize.Customizer().customize(wfrog_root+'/', customize_dir, ['wfcommon', 'wfdriver', 'wflogger', 'wfrender'])
        sys.exit(0)

    if options.setup or sac_manager.get_settings() is None:
        if not options.mute:
            sac_manager.setup_settings(user)
            if options.setup:
                sys.exit(0)
            else:
                print("Now starting wfrog. Standard config serves on http://localhost:7680/.")

    component_manager.get_component().run(sac_manager.get_config_file(), sac_manager.get_settings())

if __name__=='__main__':
    main()