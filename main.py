from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button






class CreateAccountWindow(Screen):
    username = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)


    def submit(self):
        if self.username.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password.text != "":
                db.add_user(self.email.text, self.password.text, self.username.text)


                self.reset()


                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()


    def login(self):
        self.reset()
        sm.current = "login"


    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.username.text = ""




class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)


    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            app = App.get_running_app()
            app.current_user_email = self.email.text  # Set current user's email
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()


    def createBtn(self):
        self.reset()
        sm.current = "create"


    def reset(self):
        self.email.text = ""
        self.password.text = ""




class MainWindow(Screen):
    n = ObjectProperty(None)
    email = ObjectProperty(None)
    created = ObjectProperty(None)


    def settings(self):
        print("Entering settings method")
        app = App.get_running_app()
        SettingsWindow.email = app.current_user_email  # Access current user's email
        self.reset()
        sm.current = "settings"


    def to_fridge(self):
        sm.current = "fridge"


    def reset(self):
        print("self.n:", self.n)


class FridgeWindow(Screen):
    n = ObjectProperty(None)
    items_label = ObjectProperty(None)
    item_input = ObjectProperty(None)
    input_visible = BooleanProperty(False)
    dropdown = DropDown()  # Initialize dropdown


    def on_enter(self, *args):
        app = App.get_running_app()
        items = db.get_fridge_items(app.current_user_email)
        if items:
            self.ids.items_label.text = "Items in Fridge: \n" + "\n".join(items)


    def add_item(self):
        if self.input_visible:
            new_item = self.ids.item_input.text.strip()  # Get the text entered by the user
            if new_item:
                db.add_item_to_fridge(App.get_running_app().current_user_email, new_item)
                self.ids.items_label.text += "\n" + new_item  # Append the new item to the label
            self.toggle_input()  # Hide the input field
        else:
            self.toggle_input()  # Show the input field


    def remove_item(self, item):
        removed = db.remove_item_from_fridge(App.get_running_app().current_user_email, item)
        if removed:
            self.update_items_label()  # Update items label after removing
        else:
            self.show_popup("Item not found in fridge.")
            print("Item not found in fridge.")


    def update_items_label(self):
        items = db.get_fridge_items(App.get_running_app().current_user_email)
        if items:
            self.ids.items_label.text = "Items in Fridge: \n" + "\n".join(items)




    def open_dropdown(self, button):
        self.dropdown.clear_widgets()  # Clear existing items in dropdown
        items = db.get_fridge_items(App.get_running_app().current_user_email)
        for item in items:
            if item:  # Check if item is not empty or None
                btn = Button(text=item, size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn: self.select_item(btn.text))
                self.dropdown.add_widget(btn)
        self.dropdown.open(button)
   


    def select_item(self, item):
        self.remove_item(item)


    def toggle_input(self):
        self.input_visible = not self.input_visible  # Toggle the visibility of the input field


    def show_popup(self, message):
        popup = Popup(title='Error', content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()






class SettingsWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)  


    def on_enter(self, *args):
        app = App.get_running_app()
        user_data = db.get_user(app.current_user_email)
        if user_data:
            password = user_data.get('password', '')
            name = user_data.get('name', '')
            created = user_data.get('date', '')  # Ensure 'date' field is retrieved
            self.ids.email.text = "Email: " + app.current_user_email
            self.ids.created.text = "Created On: " + created
            self.n.text = "Account Name: " + name
        else:
            print("User not found.")






    def logOut(self):
        sm.current = "login"
   
    def go_to_main(self, instance):
        sm.current = "main"




class WindowManager(ScreenManager):
    pass




def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid email or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()




def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))


    pop.open()




kv = Builder.load_file("my.kv")


sm = WindowManager()
db = DataBase("users.txt")


screens = [
    LoginWindow(name="login"),
    CreateAccountWindow(name="create"),
    MainWindow(name="main"),
    SettingsWindow(name="settings"),
    FridgeWindow(name="fridge")
]


for screen in screens:
    sm.add_widget(screen)


sm.current = "login"




class MyMainApp(App):
    def build(self):
        return sm




if __name__ == "__main__":
    MyMainApp().run()
