# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime
from functools import partial

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.utils import escape_markup

import content

Window.clearcolor = (0, 0, 0, 1)

KV = """
#:import dp kivy.metrics.dp

<Tile@Button>:
    background_normal: ''
    background_down: ''
    background_color: (0.12, 0.12, 0.12, 1)
    color: 1, 1, 1, 1
    bold: True
    font_size: '20sp'
    canvas.after:
        Color:
            rgba: (0.8, 0.05, 0.05, 1) if self.state == 'down' else (0.3, 0.3, 0.3, 1)
        Line:
            rounded_rectangle: self.x, self.y, self.width, self.height, dp(16)
            width: dp(1.5)

<BackButton@Button>:
    target: 'home'
    text: 'Назад'
    size_hint_y: None
    height: dp(50)
    background_normal: ''
    background_color: (0.15, 0.15, 0.15, 1)
    color: 1, 1, 1, 1
    on_release: app.go(self.target)

<Title@Label>:
    color: 0.8, 0.05, 0.05, 1
    bold: True
    font_size: '24sp'
    size_hint_y: None
    text_size: self.width, None
    height: self.texture_size[1] + dp(20)
    halign: 'center'

<Home>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(16)
        Title:
            text: 'ЛИЧНОЕ РАЗВИТИЕ'
        GridLayout:
            cols: 2
            spacing: dp(16)
            Tile:
                text: 'BRAIN'
                on_release: app.open_section('brain')
            Tile:
                text: 'AI'
                on_release: app.open_section('ai')
            Tile:
                text: 'STYLE'
                on_release: app.open_section('style')
            Tile:
                text: 'MEDICINE'
                on_release: app.open_section('medicine')
            Tile:
                text: 'ДНЕВНИК'
                on_release: app.go('diary')
            Tile:
                text: 'ПРОГРЕСС'
                on_release: app.go('progress')

<Section>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(16)
        spacing: dp(10)
        Title:
            text: root.title
        Label:
            text: root.subtitle
            color: 0.7, 0.7, 0.7, 1
            size_hint_y: None
            height: dp(30)
        ScrollView:
            BoxLayout:
                id: list
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(8)
        BackButton:

<Topic>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(16)
        spacing: dp(10)
        Title:
            text: root.title
            font_size: '20sp'
        ScrollView:
            Label:
                text: root.text
                color: 1, 1, 1, 1
                font_size: '16sp'
                size_hint_y: None
                height: self.texture_size[1] + dp(20)
                text_size: self.width, None
                halign: 'left'
                valign: 'top'
        Button:
            text: root.done_text
            size_hint_y: None
            height: dp(50)
            background_normal: ''
            background_color: (0.6, 0.05, 0.05, 1)
            on_release: root.toggle()
        BackButton:
            target: 'section'

<StyleQuiz>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(16)
        spacing: dp(8)
        Title:
            text: 'ПОДБОР СТИЛЯ ПОД МЕНЯ'
            font_size: '20sp'
        Spinner:
            id: build
            text: 'Телосложение'
            values: root.builds
            size_hint_y: None
            height: dp(44)
        Spinner:
            id: height
            text: 'Рост'
            values: root.heights
            size_hint_y: None
            height: dp(44)
        Spinner:
            id: contrast
            text: 'Цвет волос и кожи'
            values: root.contrasts
            size_hint_y: None
            height: dp(44)
        Spinner:
            id: setting
            text: 'Где носить'
            values: root.settings
            size_hint_y: None
            height: dp(44)
        Button:
            text: 'Подобрать'
            size_hint_y: None
            height: dp(48)
            background_normal: ''
            background_color: (0.6, 0.05, 0.05, 1)
            on_release: root.calc()
        ScrollView:
            Label:
                text: root.result
                color: 1, 1, 1, 1
                font_size: '15sp'
                size_hint_y: None
                height: self.texture_size[1] + dp(20)
                text_size: self.width, None
                halign: 'left'
                valign: 'top'
        BackButton:
            target: 'section'

<Progress>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(12)
        Title:
            text: 'ПРОГРЕСС'
        Label:
            text: root.text
            color: 1, 1, 1, 1
            font_size: '18sp'
            text_size: self.width, None
            halign: 'left'
            valign: 'top'
        BackButton:

<Diary>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(10)
        Title:
            text: 'ДНЕВНИК'
        TextInput:
            id: inp
            hint_text: 'Запиши мысль, событие, вывод дня...'
            size_hint_y: None
            height: dp(110)
            background_color: (0.12, 0.12, 0.12, 1)
            foreground_color: (1, 1, 1, 1)
            hint_text_color: (0.5, 0.5, 0.5, 1)
            cursor_color: (0.8, 0.05, 0.05, 1)
        Button:
            text: 'Сохранить запись'
            size_hint_y: None
            height: dp(50)
            background_normal: ''
            background_color: (0.6, 0.05, 0.05, 1)
            on_release: root.save()
        ScrollView:
            BoxLayout:
                id: box
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(10)
        BackButton:
"""

STYLE_QUIZ = "quiz"


class Home(Screen):
    pass


class Section(Screen):
    title = StringProperty("")
    subtitle = StringProperty("")
    key = StringProperty("")

    def on_pre_enter(self, *args):
        self.populate()

    def populate(self):
        app = App.get_running_app()
        lst = self.ids.list
        lst.clear_widgets()
        if not self.key:
            return
        topics = content.SECTIONS[self.key][2]
        progress = app.load_progress()
        for i, (name, _text) in enumerate(topics):
            done = progress.get("%s:%d" % (self.key, i))
            mark = "[x] " if done else "[ ] "
            lst.add_widget(self._button(mark + name, partial(app.open_topic, self.key, i)))
        if self.key == "style":
            lst.add_widget(self._button("Подбор стиля под меня", lambda *a: app.go("quiz")))

    @staticmethod
    def _button(text, handler):
        btn = Button(
            text=text,
            size_hint_y=None,
            height=dp(60),
            background_normal="",
            background_color=(0.12, 0.12, 0.12, 1),
            halign="left",
            valign="middle",
        )
        btn.bind(size=lambda w, v: setattr(w, "text_size", (v[0] - dp(24), v[1])))
        btn.bind(on_release=handler)
        return btn


class Topic(Screen):
    title = StringProperty("")
    text = StringProperty("")
    done_text = StringProperty("Отметить как пройденное")

    def toggle(self):
        app = App.get_running_app()
        app.toggle_done()
        self.refresh_button()

    def refresh_button(self):
        app = App.get_running_app()
        done = app.is_done()
        self.done_text = "Снять отметку" if done else "Отметить как пройденное"


class StyleQuiz(Screen):
    builds = content.STYLE_BUILDS
    heights = content.STYLE_HEIGHTS
    contrasts = content.STYLE_CONTRASTS
    settings = content.STYLE_SETTINGS
    result = StringProperty("Выбери параметры и нажми «Подобрать».")

    def calc(self):
        b, h = self.ids.build.text, self.ids.height.text
        c, s = self.ids.contrast.text, self.ids.setting.text
        if b not in self.builds or h not in self.heights or c not in self.contrasts or s not in self.settings:
            self.result = "Заполни все четыре поля."
            return
        self.result = content.build_style_advice(b, h, c, s)


class Progress(Screen):
    text = StringProperty("")

    def on_pre_enter(self, *args):
        progress = App.get_running_app().load_progress()
        lines = []
        for key, (name, _sub, topics) in content.SECTIONS.items():
            done = sum(1 for i in range(len(topics)) if progress.get("%s:%d" % (key, i)))
            lines.append("%s: %d из %d" % (name, done, len(topics)))
        entries = len(App.get_running_app().load_diary())
        lines.append("")
        lines.append("Записей в дневнике: %d" % entries)
        self.text = "\n".join(lines)


class Diary(Screen):
    def on_pre_enter(self, *args):
        self.refresh()

    def refresh(self):
        box = self.ids.box
        box.clear_widgets()
        for e in reversed(App.get_running_app().load_diary()):
            lbl = Label(
                text="[color=cc0d0d]%s[/color]\n%s" % (e["date"], escape_markup(e["text"])),
                markup=True,
                size_hint_y=None,
                halign="left",
                valign="top",
            )
            lbl.bind(width=lambda w, v: setattr(w, "text_size", (v, None)))
            lbl.bind(texture_size=lambda w, v: setattr(w, "height", v[1] + dp(12)))
            box.add_widget(lbl)

    def save(self):
        text = self.ids.inp.text.strip()
        if text:
            App.get_running_app().add_entry(text)
            self.ids.inp.text = ""
            self.refresh()


class DevApp(App):
    current_key = ""
    current_idx = 0

    def build(self):
        Builder.load_string(KV)
        self.sm = ScreenManager(transition=NoTransition())
        self.sm.add_widget(Home(name="home"))
        self.sm.add_widget(Section(name="section"))
        self.sm.add_widget(Topic(name="topic"))
        self.sm.add_widget(StyleQuiz(name="quiz"))
        self.sm.add_widget(Progress(name="progress"))
        self.sm.add_widget(Diary(name="diary"))
        return self.sm

    # ----- навигация -----
    def go(self, name):
        if name == "section" and self.sm.current == "quiz":
            pass
        self.sm.current = name

    def open_section(self, key):
        title, subtitle, _topics = content.SECTIONS[key]
        sec = self.sm.get_screen("section")
        sec.key = key
        sec.title = title
        sec.subtitle = subtitle
        self.current_key = key
        self.sm.current = "section"

    def open_topic(self, key, idx, *args):
        name, text = content.SECTIONS[key][2][idx]
        self.current_key, self.current_idx = key, idx
        topic = self.sm.get_screen("topic")
        topic.title = name
        topic.text = text
        topic.refresh_button()
        self.sm.current = "topic"

    # ----- данные -----
    @property
    def diary_path(self):
        return os.path.join(self.user_data_dir, "diary.json")

    @property
    def progress_path(self):
        return os.path.join(self.user_data_dir, "progress.json")

    def _load(self, path, default):
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except (OSError, ValueError):
            return default

    def _save(self, path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    def load_diary(self):
        return self._load(self.diary_path, [])

    def add_entry(self, text):
        entries = self.load_diary()
        entries.append({"date": datetime.now().strftime("%d.%m.%Y %H:%M"), "text": text})
        self._save(self.diary_path, entries)

    def load_progress(self):
        return self._load(self.progress_path, {})

    def is_done(self):
        return bool(self.load_progress().get("%s:%d" % (self.current_key, self.current_idx)))

    def toggle_done(self):
        progress = self.load_progress()
        k = "%s:%d" % (self.current_key, self.current_idx)
        if progress.get(k):
            progress.pop(k)
        else:
            progress[k] = True
        self._save(self.progress_path, progress)


if __name__ == "__main__":
    DevApp().run()
