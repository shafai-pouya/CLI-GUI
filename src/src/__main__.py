import threading

from configs import Configs

# import other modules
import WM
import taskbar

configs = Configs(WM, taskbar)
WM.     configs = configs
taskbar.configs = configs

# initialize modules
WM.     WMinit()
taskbar.TBinit()


# main progress
WM_thread      = threading.Thread(target=WM.     WMmain)
taskbar_thread = threading.Thread(target=taskbar.TBmain)

WM_thread.     start()
taskbar_thread.start()

WM_thread.     join()
taskbar_thread.join()