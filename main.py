# -*- coding: utf-8 -*-
import traceback

try:
    from app_main import DevApp
except Exception:
    err = traceback.format_exc()
    from kivy.app import App
    from kivy.uix.label import Label
    from kivy.uix.scrollview import ScrollView

    class DevApp(App):
        def build(self):
            sv = ScrollView()
            lbl = Label(text=err, size_hint_y=None, halign="left", valign="top", font_size="12sp")
            lbl.bind(width=lambda w, v: setattr(w, "text_size", (v, None)))
            lbl.bind(texture_size=lambda w, v: setattr(w, "height", v[1]))
            sv.add_widget(lbl)
            return sv

if __name__ == "__main__":
    DevApp().run()
