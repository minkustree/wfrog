import socket

import win32service
import win32serviceutil
import win32event
import servicemanager

class WFrogService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'wfrog'
    _svc_display_name_ = 'Weather Frog'
    _svc_description_ = 'Weather station data logging and reporting service'

    # TODO: Determine this path better
    _exe_name_ = 'D:\\Andy\\Documents\\Source\\wfrog\\env\\Scripts\\pythonservice.exe'

    @classmethod
    def handle_command_line(cls):
        ''' Call to ask the win32serviceutil framework to handle any command line
        arguments in sys.argv '''
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        ''' Called when the service is asked to stop '''
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STOPPING,
                              (self._svc_name_, ''))
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.stop()
        
    def SvcDoRun(self):
        ''' Called when the service is asked to start '''
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTING,
                              (self._svc_name_, ''))
        
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        
        self.main()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STOPPED,
                              (self._svc_name_, ''))

    def start(self):
        pass

    def stop(self):
        win32event.SetEvent(self.hWaitStop)

    def main(self):
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

        

if __name__=='__main__':
    WFrogService.handle_command_line()