import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk

import os

from Xlib import X, display, Xatom, protocol, XK

d = display.Display()
screen = d.screen()
root = screen.root



from . import appearance


class Taskbar(Gtk.Window):
    def __init__(self):
        super().__init__(title="SHP GUI CUSTOM TASKBAR")

        # list of mapped windows
        self.windows = {}

        # set few attributes for application
        self.connect("destroy", Gtk.main_quit)
        self.set_decorated(False)  # No borders/title bar
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_keep_above(True)

        # make base box for all the taskbar
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 0)
        self.add(vbox)
        self.vbox = vbox

        # make top box for taskbar
        topbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 0)
        self.topbox = topbox
        topbox.set_valign(Gtk.Align.START)
        vbox.pack_start(topbox, True, True, 0)

        # make bottom box for taskbar
        bottombox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 0)
        bottombox.set_valign(Gtk.Align.END)
        self.bottombox = bottombox
        vbox.pack_end(bottombox, True, True, 0)

        # add Exit GUI button
        self.add_button("Exit GUI", bottombox.pack_end, self.exit_gui)

        # add restart taskbar button
        self.add_button("restart taskbar", bottombox.pack_end, lambda button: self.restart_taskbar())
        
        # add launcher buttons
        self.add_launcher_buttons()

        # show window
        self.show_all()
        vbox.queue_draw()
        
        # restore data that was on the taskbar after restarting that
        self.find_all_windows_and_map(root)

    def add_button(self, label_text, map_function_for_box, click_event):
        # make label
        label_object = Gtk.Label(label=label_text)
        label_object.set_line_wrap(True)
        label_object.set_max_width_chars(8)
        label_object.set_justify(Gtk.Justification.CENTER)

        # make button
        button_object = Gtk.Button()
        button_object.add(label_object)
        button_object.connect('clicked', click_event)
        button_object.set_size_request(64, -1)

        # map button
        map_function_for_box(button_object, False, False, 0)
    
    def add_launcher_buttons(self):
        try:
            for button_id, button_details in configs.launcher_buttons.items():
                try:
                    button_command = button_details['command']
                    button_text    = button_details['text']
                    self.add_button(button_text, self.topbox.pack_start, lambda button: os.system(button_command))
                    configs.log('I', f'Added new launcher button to taskbar (id: "{button_id}", text: "{button_text}", command: "{button_command}")')
                except Exception as e:
                    configs.log('E', f'An exception raised while itering in launcher button (id: "{button_id}" and details: "{repr(button_details)}"): {e}')
        except Exception as e:
            configs.log('E', f'An exception raised while itering in launcher buttons: {e}')
    

    def find_all_windows_and_map(self, win):
        try:
            windows = win.query_tree().children
        except Exception as e:
            configs.log('E', f'an error when getting children of something: {e}')
            return
        for window in windows:
            try:
                attrs = window.get_attributes()
                if attrs.map_state != 2:
                    continue
            except:
                continue
            self.add_window_if_ok(window)
            self.find_all_windows_and_map(window)
    
    def add_window_if_ok(self, win):
        if not self.has_skip_taskbar(win):
            self.add_window(win)
            configs.log('I', 'Mapped a window to taskbar')
        else:
            configs.log('I', 'Unmappable window to map to the taskbar because of taskbar skipping option from window')
    
    def has_skip_taskbar(self, window):
        prop = window.get_property(configs.ATOMS.NET_WM_STATE, Xatom.ATOM, 0, 1024)
    
        if not prop:
            return False
    
        return configs.ATOMS.NET_WM_STATE_SKIP_TASKBAR in prop.value
    
    
    def get_window_title(self, window):
    
        title = window.get_property(configs.ATOMS.NET_WM_NAME, configs.ATOMS.UTF8_STRING, 0, 1024)
        if title:
            return title.value.decode('utf-8')
    
        # Fallback: try WM_NAME (legacy, non-UTF8)
        wm_name = window.get_property(Xatom.WM_NAME, Xatom.STRING, 0, 1024)
        if wm_name:
            return wm_name.value.decode('utf-8')
    
        return None
    
    def active_window(self, window):
        window.configure(stack_mode=X.Above)
    
        # Set input focus
        window.set_input_focus(X.RevertToParent, X.CurrentTime)
    
        # Send _NET_ACTIVE_WINDOW client message
        event = protocol.event.ClientMessage(
            window = root,
            client_type = configs.ATOMS.NET_ACTIVE_WINDOW,
            data = (32, [1, X.CurrentTime, window.id, 0, 0])
        )
    
        root.send_event(event, event_mask=X.SubstructureRedirectMask | X.SubstructureNotifyMask)
        d.flush()

    

    def exit_gui(self, button):
        os.system("pkill x")

    def add_window(self, win):
        if win.id in self.windows:
            return

        title = self.get_window_title(win)

        self.add_button(title, self.topbox.pack_start, lambda button: active_window(win))

        # self.show_all()
        # self.hbox.queue_draw()

        # self.move(0, 0)
    def remove_window(self, win):
        if win.id not in self.windows:
            return

        win, button = self.windows[win.id]

        self.topbox.remove(button)
    
    def restart_taskbar(self):
        global tsk
        Gtk.main_quit()
        tsk.unmap()
        tsk = Taskbar()
        Gtk.main()

def TBinit():
    global tsk
    tsk = Taskbar()

def TBmain():
    while True:
        Gtk.main()
        configs.log('E', 'Umm, Gtk quited the main. I think got a bug. Restarting it..')

