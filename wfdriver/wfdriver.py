#!/usr/bin/python

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

# Before loading other modules add wfrog directory to sys.path to be able to use wfcommon
import os.path
import sys
if __name__ == "__main__": sys.path.append(os.path.abspath(sys.path[0] + '/..'))

import station
import output
import wfcommon.generic
from output import stdio
import optparse
import logging
import wfcommon.log
import wfcommon.config
from threading import Thread
from Queue import Queue, Full
import event

def gen(type):
    return event.Event(type)

class Driver(object):

    logger = logging.getLogger('wfdriver')  ## get root logger so that all properties are transfered to all loggers

    # default values
    output = stdio.StdioOutput()
    queue_size = 10

    def __init__(self):
        
        # Prepare the configurer
        module_map = (
            ( "Stations" , station ),
            ( "Output" , output),
            ( "Generic Elements", wfcommon.generic)
        )
        configurer = wfcommon.config.Configurer("config/wfdriver.yaml", module_map)      

        # Initilize the option parser        
        opt_parser = optparse.OptionParser()
        configurer.add_options(opt_parser)
        wfcommon.log.add_options(opt_parser)

        # Parse the options and create object trees from configuration
        (options, args) = opt_parser.parse_args()
        (config, context) = configurer.configure(options)

        # Configure the log
        wfcommon.log.configure(options, config, context)

        # Initialize the driver from object trees
        self.station = config['station']

        if config.has_key('output'):
            self.output = config['output']
        if config.has_key('queue_size'):
            self.queue_size = config['queue_size']

        self.event_queue = Queue(self.queue_size)

    def enqueue_event(self,event):
        self.logger.debug('Queue size: '+str(self.event_queue.qsize()))
        try:
            self.event_queue.put(event, block=False)
        except Full:
            raise Exception('Consumer of events is dead or not consuming quickly enough')

    def output_loop(self):
        while True:
            event = self.event_queue.get(block=True)
            self.output.send_event(event)

    def run(self):

        # Start the logger thread
        logger_thread = Thread(target=self.output_loop)
        logger_thread.setDaemon(True)
        logger_thread.start()

        self.station.run(gen, self.enqueue_event)

if __name__ == "__main__":
    driver = Driver()
    driver.logger.debug("Started main()")
    driver.run()
    driver.logger.debug("Finished main()")