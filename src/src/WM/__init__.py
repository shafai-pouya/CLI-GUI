from Xlib import X, display, Xatom, protocol
import random

WINDOW_TYPE_TASKBAR = 1
WINDOW_TYPE_DOCK = 2
WINDOW_TYPE_NORMAL = 3
WINDOW_TYPE_DO_NOT_HANDLE = 4





def find_the_window_type(win):
    try:
        window_type_property = win.get_full_property(NET_WM_WINDOW_TYPE, Xatom.ATOM) or None
    except Exception as e:
        window_type_property = None
    try:
        window_name_property = win.get_full_property(NET_WM_NAME, 0) or None
    except Exception as e:
        window_name_property = None

    configs.log('I', f'found window named "{window_name_property and window_name_property.value}" with type: "{window_type_property and window_type_property.value}"')

    if window_name_property and b'SHP GUI CUSTOM TASKBAR' in window_name_property.value:
        return WINDOW_TYPE_TASKBAR
    if not window_type_property:
        configs.log('E', 'window type is empty!!!')
        return WINDOW_TYPE_NORMAL
    if window_type_property.value == NET_WM_WINDOW_TYPE_DOCK:
        return WINDOW_TYPE_DOCK
    return WINDOW_TYPE_NORMAL



class Configure:
    def do_configure(win, evt):
        w_type = find_the_window_type(win)
        
        configs.log('I', 'Configuring window')
        x, y, width, height, need_send_configure_event, need_configure_process = Configure.get_configure_values(evt, w_type)
        
        if need_configure_process:
            win.configure(x=x, y=y, width=width, height=height)
            
        if need_send_configure_event:
            Configure.send_configure_event(win, x, y, width, height, 0)
        
    def get_configure_values(evt, window_type):
        screen_width, screen_height = configs.screen.width_in_pixels, configs.screen.height_in_pixels
        if window_type == WINDOW_TYPE_TASKBAR:
                return 0, 0, 64, screen_height, True, True
        if window_type == WINDOW_TYPE_DOCK:
                return evt.x, evt.y, evt.width, evt.height, False, True
        if window_type == WINDOW_TYPE_NORMAL:
                return 64, 0, screen_width - 64, screen_height, True, True
        if window_type == WINDOW_TYPE_DO_NOT_HANDLE:
                return 0, 0, 0, 0, False, False
                
                
        x, y, width, height, need_send_configure_event, need_configure_process = get_configure_values(evt, window_type)
    
    def send_configure_event(win, x, y, width, height, border_width):
        event = protocol.event.ConfigureNotify(
            event=win,
            window=win,
            above_sibling=X.NONE,
            x=x,
            y=y,
            width=width,
            height=height,
            border_width=border_width,
            override=False,
            send_event=True
        )
    
        win.send_event(event, event_mask=0)
        configs.d.flush()


class Map:
    def do_map(win, evt):
        w_type = find_the_window_type(win)
        
        configs.log('I', 'Mapping window')
        win.map()
        
        configs.log('I', 'Configuring and mapping window')
        Configure.do_configure(win, evt)
        
        configs.log('I', 'Mapping window to taskbar')
        configs.taskbar.tsk.add_window_if_ok(win)

class Unmap:
    def do_unmap(win, evt):
        configs.log('I', 'Unmapping window')
        win.unmap()
        
        configs.log('I', 'Unmapping window from taskbar')
        configs.taskbar.tsk.remove_window(win)
        




def WMinit():
    # looking for events after this line
    configs.root.change_attributes(event_mask=X.SubstructureRedirectMask | X.SubstructureNotifyMask)
    

def WMmain():
    while True:
        # get an event
        event = configs.d.next_event()

        # handle map events
        if event.type == X.MapRequest:
            win = event.window
            Map.do_map(win, event)

        # handle configure events
        elif event.type == X.ConfigureRequest:
            win = event.window
            Configure.do_configure(win, event)

        # handle unmap events
        elif event.type == X.UnmapNotify:
            win = event.window
            Unmap.do_unmap(win, event)


