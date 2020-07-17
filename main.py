# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 16:09:21 2020

@author: VK
"""

import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation 
from hoverable import HoverBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from datetime import datetime
import json
import glob
from pathlib import Path
import random
Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"
        
    def login(self,uname,pword):
        with open("users.json") as file:
            users=json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text = "wrong username or paswword"
            
class RootWidget(ScreenManager):
    pass

class ImageButton(ButtonBehavior, HoverBehavior, Image ):
    pass

class SignUpScreen(Screen):
    def add_user(self,uname,pword):
        with open("users.json") as file:
            users=json.load(file)
        users[uname] = {'username':uname,'password':pword,
                        'created':datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
        
        with open("users.json", 'w') as file:
            json.dump(users,file)
        self.manager.current = "sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def goto_login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "Login_screen"
         
class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "Login_screen"
    def get_quotes(self,feel):
        feel = feel.lower()
        available_feelings = glob.glob("Quotes/*txt")
        available_feelings = [Path(filename).stem for filename in 
                              available_feelings]
        if feel in available_feelings:
            with open(f"Quotes/{feel}.txt", encoding="utf8") as file:
                quotes = file.readlines() 
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling!"
class MainApp(App):
    def build(self):
        return RootWidget() 
    
if __name__ == '__main__':
    app = MainApp()
    app.run()
    