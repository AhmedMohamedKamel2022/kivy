from kivy.app import App
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.metrics import dp

from kivy.uix.screenmanager import (
    ScreenManager,
    Screen,
    SlideTransition
)

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.behaviors import ButtonBehavior

from kivy.graphics import (
    Color,
    Rectangle,
    RoundedRectangle,
)

from kivy.clock import Clock

from datetime import datetime

import requests
LabelBase.register(
    name="Arabic",
    fn_regular="Tahoma Gras 700.ttf",
)

import arabic_reshaper
from bidi.algorithm import get_display

def ar(text):
    if not text:
        return ""
    return get_display(arabic_reshaper.reshape(str(text)))


# ===========================
# APP SETTINGS
# ===========================

Window.clearcolor = (0.95,0.97,0.99,1)

Window.title = "Cyclic Resinline System"
BASE_URL = "http://192.168.1.13:5000"



# ===========================
# COLORS
# ===========================

PRIMARY = (0.09,0.32,0.60,1)

SUCCESS = (0.18,0.63,0.29,1)

DANGER = (0.84,0.18,0.15,1)

BACKGROUND = (0.95,0.97,0.99,1)

WHITE = (1,1,1,1)

TEXT = (0.18,0.22,0.30,1)



# ===========================
# FORMAT DATE
# ===========================

def format_date(value):

    if not value:
        return ""

    try:

        value=value.replace("T"," ")

        dt=datetime.fromisoformat(value)

        return dt.strftime("%Y-%m-%d %H:%M")

    except:

        return str(value)



# ===========================
# FORMAT DURATION
# ===========================

def format_duration(duration,start,end):

    if duration:

        return str(duration)

    if not start or not end:

        return ""

    try:

        start=start.replace("T"," ")

        end=end.replace("T"," ")

        s=datetime.fromisoformat(start)

        e=datetime.fromisoformat(end)

        diff=e-s

        hours=int(diff.total_seconds()/3600)

        minutes=int((diff.total_seconds()%3600)/60)

        return f"{hours}h {minutes}m"

    except:

        return ""



# ===========================
# API
# ===========================

class API:


    @staticmethod
    def get_faults():

        return requests.get(
            f"{BASE_URL}/faults"
        ).json()


    @staticmethod
    def get_machines():

        return requests.get(
            f"{BASE_URL}/machines"
        ).json()


    @staticmethod
    def add_fault(data):

        return requests.post(
            f"{BASE_URL}/faults",
            json=data
        )


    @staticmethod
    def close_fault(fault_id):

        return requests.put(
            f"{BASE_URL}/faults/{fault_id}/close"
        )
# ============================================
# BUTTON
# ============================================

class PrimaryButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)

        self.color = WHITE

        self.font_size = dp(15)

        self.bold = True

        with self.canvas.before:

            Color(*PRIMARY)

            self.bg = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[12]
            )

        self.bind(
            pos=self.update_bg,
            size=self.update_bg
        )

    def update_bg(self, *args):

        self.bg.pos = self.pos
        self.bg.size = self.size


# ============================================
# STATUS LABEL
# ============================================

class StatusLabel(Label):

    def __init__(self, status, **kwargs):
        super().__init__(**kwargs)

        self.bold = True

        self.font_size = dp(13)

        self.text = status

        if status == "Open":

            self.color = SUCCESS

        else:

            self.color = DANGER


# ============================================
# TABLE HEADER
# ============================================

class TableHeader(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 4

        self.size_hint_y = None

        self.height = dp(60)

        with self.canvas.before:

            Color(*PRIMARY)

            self.bg = Rectangle(
                pos=self.pos,
                size=self.size
            )

        self.bind(
            pos=self.update_bg,
            size=self.update_bg
        )

        headers = [

            "ID",

            "Machine",

            "Fault",

            "Status"

        ]

        for h in headers:

            self.add_widget(

                Label(

                    text=f"[b]{h}[/b]",

                    markup=True,

                    color=WHITE,
                    size_hint_x=0.15

                )

            )

    def update_bg(self, *args):

        self.bg.pos = self.pos

        self.bg.size = self.size


# ============================================
# TABLE ROW
# ============================================

class TableRow(ButtonBehavior, GridLayout):

    def __init__(self, row, callback=None, **kwargs):
        super().__init__(**kwargs)

        self.row = row

        self.callback = callback

        self.cols = 4

        self.height = dp(60)

        self.size_hint_y = None

        with self.canvas.before:

            Color(1, 1, 1, 1)

            self.bg = Rectangle(
                pos=self.pos,
                size=self.size
            )

        self.bind(
            pos=self.update_bg,
            size=self.update_bg
        )

        self.add_widget(

            Label(

                text=str(row["FaultID"]),

                color=TEXT,
                size_hint_x=0.15

            )

        )

        self.add_widget(

            Label(

                text=ar(row["MachineName"]),

                color=TEXT,
                font_name="Arabic",
                size_hint_x=0.35

            )

        )

        self.add_widget(

            Label(

                text=ar(row["FaultName"]),

                color=TEXT,
                font_name="Arabic",
                size_hint_x=0.35
                           

            )

        )

        self.add_widget(

            StatusLabel(

                row["Status"],
                size_hint_x=0.15

            )

        )

    def update_bg(self, *args):

        self.bg.pos = self.pos

        self.bg.size = self.size

    def on_press(self):

        with self.canvas.before:

            Color(0.90, 0.95, 1, 1)

            self.bg = Rectangle(
                pos=self.pos,
                size=self.size
            )

        if self.callback:

            self.callback(self.row)
            
# ============================================
# FAULT LIST SCREEN
# ============================================

class FaultListScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        # ========= Title =========

        title = Label(
            text="Cyclic Resinline System",
            font_size=dp(26),
            bold=True,
            size_hint_y=None,
            height=50,
            color=PRIMARY
        )

        root.add_widget(title)

        # ========= Add Button =========

        add_btn = PrimaryButton(
            text="Add Fault",
            size_hint_y=None,
            height=50
        )

        add_btn.bind(on_press=self.go_add)

        root.add_widget(add_btn)

        # ========= Header =========

        root.add_widget(TableHeader())

        # ========= Table =========

        self.table = GridLayout(
            cols=1,
            spacing=1,
            size_hint_y=None
        )

        self.table.bind(
            minimum_height=self.table.setter("height")
        )

        scroll = ScrollView()

        scroll.add_widget(self.table)

        root.add_widget(scroll)

        self.add_widget(root)

    # ==================================

    def on_pre_enter(self):

        self.load_faults()

    # ==================================

    def go_add(self, instance):

        self.manager.transition = SlideTransition(
            direction="left"
        )

        self.manager.current = "add"

    # ==================================

    def load_faults(self):

        self.table.clear_widgets()

        try:

            faults = API.get_faults()

            for row in faults:

                self.table.add_widget(

                    TableRow(

                        row,

                        callback=self.show_details

                    )

                )

        except Exception as e:

            self.table.add_widget(

                Label(

                    text=str(e),

                    color=DANGER

                )

            )

    # ==================================

    def show_details(self, row):

    # ================= BACKGROUND CARD =================
        layout = BoxLayout(
            orientation="vertical",
            spacing=12,
            padding=20,
            size_hint_y=None
        )

        layout.bind(minimum_height=layout.setter("height"))

        # خلفية كارد بيضاء + حواف ناعمة
        with layout.canvas.before:
            Color(1, 1, 1, 1)  # أبيض نضيف
            self.card_bg = RoundedRectangle(
                pos=layout.pos,
                size=layout.size,
                radius=[15]
            )

        def update_bg(*args):
            self.card_bg.pos = layout.pos
            self.card_bg.size = layout.size

        layout.bind(pos=update_bg, size=update_bg)

        # ================= ITEM DESIGN =================
        def item(title, value):

            box = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=70,
                padding=8,
                spacing=5
            )

            # ===== BORDER =====
            with box.canvas.before:
                Color(0.95, 0.95, 0.95, 1)  # خلفية خفيفة
                rect = RoundedRectangle(
                    pos=box.pos,
                    size=box.size,
                    radius=[10]
                )

            def update_rect(*args):
                rect.pos = box.pos
                rect.size = box.size

            box.bind(pos=update_rect, size=update_rect)

            # ===== TITLE =====
            box.add_widget(
                Label(
                    text=ar(f"{title}:"),
                    bold=True,
                    color=(0.2, 0.2, 0.2, 1),
                    size_hint_y=None,
                    height=25,
                    halign="left"
                )
            )

            # ===== VALUE =====
            box.add_widget(
                Label(
                    text=ar(value),
                    font_name="Arabic",
                    color=(0.1, 0.1, 0.1, 1),
                    size_hint_y=None,
                    height=25,
                    halign="left"
                )
            )

            layout.add_widget(box)
        # ================= DATA =================

        item("Fault ID", row["FaultID"])
        item("Machine", row["MachineName"])
        item("Fault", row["FaultName"])
        item("Description", row["Description"])
        item("Start Time", format_date(row["StartTime"]))
        item("End Time", format_date(row["EndTime"]))

        item(
            "Duration",
            format_duration(
                row["Duration"],
                row["StartTime"],
                row["EndTime"]
            )
        )

        item("Status", row["Status"])

        # ================= CLOSE BUTTON =================
        if row["Status"] == "Open":

            close_btn = PrimaryButton(
                text="Close Fault",
                size_hint_y=None,
                height=45
            )

            def close_fault(instance):
                API.close_fault(row["FaultID"])
                popup.dismiss()
                self.load_faults()

            close_btn.bind(on_press=close_fault)
            layout.add_widget(close_btn)

        # ================= BACK BUTTON =================
        back_btn = Button(
            text="Back",
            size_hint_y=None,
            height=45
        )

        def close_popup(instance):
            popup.dismiss()

        back_btn.bind(on_press=close_popup)
        layout.add_widget(back_btn)

        # ================= SCROLL =================
        scroll = ScrollView()
        scroll.add_widget(layout)

        # ================= POPUP =================
        popup = Popup(
            title="Fault Details",
            content=scroll,
            size_hint=(0.92, 0.92),
            background_color=(0, 0, 0, 0)  # يخليه أنضف بصريًا
        )

        popup.open()
        
# ============================================
# ADD FAULT SCREEN
# ============================================

class AddFaultScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=15
        )

        title = Label(
            text="Add New Fault",
            font_size=dp(24),
            bold=True,
            color=PRIMARY,
            size_hint_y=None,
            height=50
        )

        root.add_widget(title)

        # =============================

        self.machine = Spinner(
            text="Select Machine",
            size_hint_y=None,
            height=50
        )

        root.add_widget(self.machine)

        # =============================

        self.fault = TextInput(
            hint_text="Fault Name",
            multiline=False,
            size_hint_y=None,
            height=50,
            font_name="Arabic",
            font_size=dp(18)
        )

        root.add_widget(self.fault)

        # =============================

        self.description = TextInput(
            hint_text="Description",
            multiline=True,
            font_name="Arabic",
            font_size=dp(18)
        )

        root.add_widget(self.description)

        # =============================

        save = PrimaryButton(
            text="Save Fault",
            size_hint_y=None,
            height=50
        )

        save.bind(
            on_press=self.save_fault
        )

        root.add_widget(save)

        # =============================

        back = Button(
            text="Back",
            size_hint_y=None,
            height=45
        )

        back.bind(
            on_press=self.go_back
        )

        root.add_widget(back)

        self.add_widget(root)

    # =====================================

    def on_pre_enter(self):

        self.load_machines()

    # =====================================

    def load_machines(self):

        try:

            machines = API.get_machines()

            self.machine.values = [

                m["MachineName"]

                for m in machines

            ]

        except Exception as e:

            print(e)

    # =====================================

    def save_fault(self, instance):

        if self.machine.text == "Select Machine":

            return

        data = {

            "MachineName": self.machine.text,

            "FaultName": self.fault.text,

            "Description": self.description.text

        }

        try:

            r = API.add_fault(data)

            if r.status_code == 200:

                Popup(

                    title="Success",

                    content=Label(

                        text="Fault Added Successfully"

                    ),

                    size_hint=(0.7,0.3)

                ).open()

                self.machine.text = "Select Machine"

                self.fault.text = ""

                self.description.text = ""

                self.manager.get_screen(
                    "list"
                ).load_faults()

                self.manager.transition = SlideTransition(
                    direction="right"
                )

                self.manager.current = "list"

        except Exception as e:

            Popup(

                title="Error",

                content=Label(

                    text=str(e)

                ),

                size_hint=(0.8,0.4)

            ).open()

    # =====================================

    def go_back(self, instance):

        self.manager.transition = SlideTransition(
            direction="right"
        )

        self.manager.current = "list"
        
# ============================================
# APP
# ============================================

class FaultsApp(App):

    def build(self):
        Window.title = "Cyclic Resinline System"
        sm = ScreenManager()

        sm.add_widget(
            FaultListScreen(
                name="list"
            )
        )

        sm.add_widget(
            AddFaultScreen(
                name="add"
            )
        )

        return sm
    
class FaultDetailsScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.row = {}

        root = BoxLayout(
            orientation="vertical",
            spacing=15,
            padding=15
        )

        # ================= Title =================

        title = Label(
            text="Fault Details",
            font_size=dp(26),
            bold=True,
            size_hint_y=None,
            height=50,
            color=PRIMARY
        )

        root.add_widget(title)

        # ================= Scroll =================

        scroll = ScrollView()

        self.container = BoxLayout(
            orientation="vertical",
            spacing=12,
            size_hint_y=None,
            padding=(5,5)
        )

        self.container.bind(
            minimum_height=self.container.setter("height")
        )

        scroll.add_widget(self.container)

        root.add_widget(scroll)

        # ================= Buttons =================

        self.close_btn = PrimaryButton(
            text="Close Fault",
            size_hint_y=None,
            height=50
        )

        self.close_btn.bind(
            on_press=self.close_fault
        )

        root.add_widget(self.close_btn)

        back = Button(
            text="Back",
            size_hint_y=None,
            height=45
        )

        back.bind(
            on_press=self.go_back
        )

        root.add_widget(back)

        self.add_widget(root)
        
            
    


if __name__ == "__main__":
    FaultsApp().run()