from Xlib import display
import inspect

import yaml
try:
    yaml_loader = yaml.CLoader
except:
    yaml_loader = yaml.Loader

# import constants
from constants import LOG_FILE_ADDRESS, APP_ADDRESS, CFG_FILE_ADDRESS

module = None # Using as a type

class Configs:
    '''
    This class contains all configs for the GUI sush as:
    * WM and taskbar modules
    * Application program address
    * Log file object
    * X properties (display, screen, etc)
    '''
    def __init__(self, WM:module, taskbar:module):
        # storing modules
        self.WM = WM
        self.taskbar = taskbar
        
        # storing constants
        self.APP_ADDRESS = APP_ADDRESS
        self.LOG_FILE_ADDRESS = LOG_FILE_ADDRESS
        self.CFG_FILE_ADDRESS = CFG_FILE_ADDRESS
        
        # storing log file
        open(LOG_FILE_ADDRESS, 'w').close()
        self.log_file = open(LOG_FILE_ADDRESS, 'a')
        
        # load config file
        self.load_cfg()
        
        # storing X properties
        self.d = display.Display()
        self.screen = self.d.screen()
        self.root = self.screen.root
        
        self.ATOMS = Atoms(self.d)

    def load_cfg(self):
        # load config content
        with open(CFG_FILE_ADDRESS, 'r') as yaml_file:
            self.cfg_file_dictionary = yaml.load(yaml_file.read(), yaml_loader)
            
        # check for being all values setted
        if 'launcher-buttons' not in self.cfg_file_dictionary:
            self.log('E', 'unable to find launcher-buttons in "cfg.yaml" file')
            print('****************************** Exiting with code 1 ******************************', file=self.log_file, flush=True)
            exit(1)
        
        # load launcher buttons
        self.launcher_buttons = self.cfg_file_dictionary['launcher-buttons']
    
    def log(self, log_type, log_message):
        # Get log path
        log_path = ''
        inspect_path = inspect.stack()
        for inspect_point in reversed(inspect_path):
            if inspect_point.function in self.log_path_functions:
                log_path += self.log_path_functions[inspect_point.function]
        
        # Log the message
        print(f'[{log_type}]{log_path}  {log_message}', file=self.log_file, flush=True)
    
    log_path_functions = {
        'WMinit': '[WMinit]',
        'TBinit': '[taskbarinit]',
        'WMmain': '[WMmain]',
        'TBmain': '[taskbarmain]',
        'load_cfg': '[cfg.yaml loading]',
        'add_launcher_buttons': '[Taskbar.add_launcher_buttons]',
        'find_all_windows_and_map': '[Taskbar.find_all_windows_and_map]',
        'do_configure': '[Configure.do_configure]',
        'find_the_window_type': '[find_the_window_type]',
        'do_map': '[Map.do_map]',
        'do_unmap': '[Unmap.do_unmap]',
        'find_the_window_type': '[find_the_window_type]'
    }

class Atoms:
    '''
    This class contains Atoms that is needed by application
    '''
    def __init__(self, d):
        self.NET_WM_WINDOW_TYPE        = d.intern_atom('_NET_WM_WINDOW_TYPE')
        self.NET_WM_WINDOW_TYPE_DOCK   = d.intern_atom('_NET_WM_WINDOW_TYPE_DOCK')
        self.NET_WM_WINDOW_TYPE_NORMAL = d.intern_atom('_NET_WM_WINDOW_TYPE_NORMAL')
        self.NET_WM_NAME               = d.intern_atom("_NET_WM_NAME")
        self.NET_WM_STATE_SKIP_TASKBAR = d.intern_atom('_NET_WM_STATE_SKIP_TASKBAR')
        self.NET_WM_STATE              = d.intern_atom('_NET_WM_STATE')
        self.NET_ACTIVE_WINDOW         = d.intern_atom('_NET_ACTIVE_WINDOW')
        self.UTF8_STRING               = d.intern_atom('UTF8_STRING')
    