import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

style_provider = Gtk.CssProvider()
style_provider.load_from_data(b"""
button {
    background-color: black;
    background: black;
    box-shadow: none;
    border-radius: 0;
    border: 0;
    padding: 0px;
    margin: 0px;
    color: white;
    font-family: 'Fira Code', monospace;
    font-size: 8px;
}

button:hover {
    background: white;
    background-color: white;
    color: black;
}
window {
    background: black;
    background-color: black;
}
""")

Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(),
    style_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

