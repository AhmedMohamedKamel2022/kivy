from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Rectangle
import requests


# ================= BASE URL =================
BASE_URL = "http://192.168.1.13:5000"


# ================= COLORS =================
BG = (1, 1, 1, 1)
PRIMARY = (0.2, 0.6, 1, 1)


# ================= ROW =================
class TableRow(BoxLayout):

    def __init__(self, data, widths, color=(0.97, 0.97, 0.97, 1)):
        super().__init__()

        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = 45
        self.spacing = 2

        with self.canvas.before:
            Color(*color)
            self.bg = Rectangle()

        self.bind(pos=self.update_bg, size=self.update_bg)

        for i, v in enumerate(data):
            self.add_widget(
                Label(
                    text=str(v),
                    color=(0, 0, 0, 1),
                    size_hint_x=widths[i]
                )
            )

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size


# ================= LIST SCREEN =================
class FaultListScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10,
            size_hint=(1, 1)
        )

        # BACKGROUND
        with root.canvas.before:
            Color(*BG)
            self.bg = Rectangle()

        root.bind(pos=self.update_bg, size=self.update_bg)

        # TITLE
        root.add_widget(Label(
            text="Cyclic Resinline Faults",
            font_size=24,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=50
        ))

        # BUTTON
        btn = Button(
            text="Add Fault",
            size_hint_y=None,
            height=50,
            background_color=PRIMARY,
            color=(1, 1, 1, 1)
        )
        btn.bind(on_press=self.go_add)
        root.add_widget(btn)

        # TABLE WIDTHS
        self.widths = [0.1, 0.2, 0.2, 0.3, 0.2]

        # TABLE
        self.table = GridLayout(
            cols=1,
            size_hint_y=None,
            spacing=3,
            padding=5
        )

        self.table.bind(minimum_height=self.table.setter("height"))

        scroll = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            do_scroll_y=True
        )

        scroll.add_widget(self.table)

        # 🔥 FIX IMPORTANT: Force scroll to top
        scroll.scroll_y = 1

        # 🔥 FIX: Anchor layout to force top start
        container = AnchorLayout(anchor_y="top")
        container.add_widget(scroll)

        root.add_widget(container)

        self.add_widget(root)

    def update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size

    def on_pre_enter(self):
        self.load_data()

    def go_add(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "add"

    def load_data(self):

        self.table.clear_widgets()

        try:
            r = requests.get(f"{BASE_URL}/faults")
            data = r.json()

            for i, row in enumerate(data):

                color = (0.97, 0.97, 0.97, 1) if i % 2 == 0 else (1, 1, 1, 1)

                self.table.add_widget(
                    TableRow(
                        [
                            row.get("FaultID"),
                            row.get("MachineName"),
                            row.get("FaultName"),
                            row.get("Description"),
                            row.get("StartTime")
                        ],
                        self.widths,
                        color
                    )
                )

        except Exception as e:
            self.table.add_widget(
                TableRow(["ERROR", str(e), "", "", ""], self.widths)
            )


# ================= ADD SCREEN =================
class AddFaultScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10,
            size_hint=(1, 1)
        )

        with root.canvas.before:
            Color(*BG)
            self.bg = Rectangle()

        root.bind(pos=self.update_bg, size=self.update_bg)

        root.add_widget(Label(
            text="Add Fault",
            font_size=22,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=50
        ))

        self.machine = Spinner(
            text="Select Machine",
            size_hint_y=None,
            height=45,
            background_color=(0.95, 0.95, 0.95, 1)
        )

        self.fault = TextInput(
            hint_text="Fault Name",
            size_hint_y=None,
            height=45
        )

        self.desc = TextInput(
            hint_text="Description",
            size_hint_y=None,
            height=45
        )

        root.add_widget(self.machine)
        root.add_widget(self.fault)
        root.add_widget(self.desc)

        btn_add = Button(
            text="Save Fault",
            size_hint_y=None,
            height=50,
            background_color=PRIMARY,
            color=(1, 1, 1, 1)
        )
        btn_add.bind(on_press=self.add_fault)

        btn_back = Button(
            text="Back",
            size_hint_y=None,
            height=50
        )
        btn_back.bind(on_press=self.go_back)

        root.add_widget(btn_add)
        root.add_widget(btn_back)

        self.add_widget(root)

        self.load_machines()

    def update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size

    def load_machines(self):

        try:
            r = requests.get(f"{BASE_URL}/machines")
            data = r.json()

            self.machine.values = [m["MachineName"] for m in data]

        except Exception as e:
            print(e)

    def add_fault(self, instance):

        if self.machine.text == "Select Machine":
            return

        data = {
            "MachineName": self.machine.text,
            "FaultName": self.fault.text,
            "Description": self.desc.text
        }

        try:
            r = requests.post(f"{BASE_URL}/faults", json=data)

            if r.status_code == 200:

                Popup(
                    title="Success",
                    content=Label(text="Fault Added Successfully"),
                    size_hint=(0.6, 0.3)
                ).open()

                self.machine.text = "Select Machine"
                self.fault.text = ""
                self.desc.text = ""

                self.manager.transition = SlideTransition(direction="right")
                self.manager.current = "list"

        except Exception as e:
            print(e)

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "list"


# ================= APP =================
class FactoryApp(App):
    title = "Cyclic Resinline Faults"

    def build(self):

        sm = ScreenManager()

        sm.add_widget(FaultListScreen(name="list"))
        sm.add_widget(AddFaultScreen(name="add"))

        return sm


FactoryApp().run()