import os
import json
import lib.crypt as aes
import lib.speedruncom as spc
import TKinterModernThemes as tkmt
import requests as r
import tkinter as tk
import threading as t
import tkinter.font as tkFont
from tkinter import messagebox as mb
from PIL import ImageTk, Image
from lib.logging import *
from math import gcd

def get_dimensions(dimensions):
    height, width = dimensions
    factor = gcd(height, width)
    
    simplified_height = height // factor
    simplified_width = width // factor
    
    multiplier = 64 // simplified_height
    if 64 % simplified_height != 0:
        multiplier += 0.5
    
    new_height = round(simplified_width * multiplier)
    new_width = round(simplified_height * multiplier)
    
    return new_width, new_height

def download_png(url, save_path):
    response = r.get(url, stream=True)
    response.raise_for_status()
    
    with open(save_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

def resize_image(input_image_path, output_image_path, size):
    original_image = Image.open(input_image_path)
    resized_image = original_image.resize(size)
    resized_image.save(output_image_path)

def chunk_list(lst, chunk_size):
    return [lst[i:i+chunk_size] for i in range(0, len(lst), chunk_size)]

def getAccountData():
    with open("acc.dat", "r") as accFile:
        return json.load(accFile)

def clearFrame(frame):
    for widget in frame.winfo_children():
       widget.destroy()
    
def validatePassword(username, password):
    dat = getAccountData()
    username = username.lower()
        
    if dat.get(username):
        try:
            if aes.aes256(bytes.fromhex(dat[username]["test"]), password, False) == username.encode():
                return [True, aes.aes256(bytes.fromhex(dat[username]["key"]), password, False)]
            else:
                return [False, "passwd"]
        except ValueError:
            return [False, "passwd"]
        except:
            return [False, "error"]
    else:
        return [False, "uname"]

class NewApp(tkmt.ThemedTKinterFrame):
    def __init__(self):
        super().__init__("Speedrun Desktop - API Key", "sun-valley", "dark", False, True)
        
        self.keyVar = tk.StringVar(self.root, "")
        self.createElements()
        
        self.run()
    
    def auth(self, *args):
        NewAppEncr(self.keyVar.get())
        self.handleExit()
    
    def createElements(self):
        self.Text("Welcome to Speedrun Desktop", ("Segoe UI bold", 18))
        self.Text("To access the services, you need an account and an API Key.\nThese are both free and can be accessed by pressing the buttons below.")
        
        self.authButtons = self.addFrame("AuthButtons", pady=0)
        self.authButtons.AccentButton("API Key", os.system, (["start https://www.speedrun.com/settings/api"]))
        self.authButtons.Button("Login", os.system, (["start https://www.speedrun.com/auth/login"]), row=0, col=1)
        
        self.Text("Once you have got your API Key, paste it below.")
        self.Entry(self.keyVar, widgetkwargs={"show": "•"})
        
        self.AccentButton("Next Step", self.auth)
        
        self.Text("The API Key is encrypted with AES-256, and incredibly secure algorithm.\nYou will choose the passphrase for it next.", ("Segoe UI italic", 8))
    
class NewAppEncr(tkmt.ThemedTKinterFrame):
    def __init__(self, key):
        super().__init__("Speedrun Desktop - Encryption", "sun-valley", "dark", False, True)
        
        self.key = key
        self.uname = tk.StringVar(self.root, "")
        self.passwd = tk.StringVar(self.root, "")
        
        self.createElements()
        
        self.run()
    
    def createElements(self):
        self.Text("New Account", ("Segoe UI bold", 18))
        self.Text("You've given the app your API Key, now it's time to encrypt it.\nChoose a secure but memorable password and enter it below.")
        
        self.Entry(self.passwd, widgetkwargs={"show": "•"})
        
        self.Text("Please enter an account name below.")
        
        self.Entry(self.uname)
        
        self.Text("Once you have finished, create the user.")
        
        self.AccentButton("Create User", self.addUser)
        
        self.Text("The API Key is encrypted with AES-256, and incredibly secure algorithm.\nYou are choosing the passphrase for it.", ("Segoe UI italic", 8))
    
    def addUser(self):
        dat = getAccountData()
        self.uname.set(self.uname.get().lower())
        
        if dat.get(self.uname.get()):
            mb.showwarning("Speedrun Desktop - Name Taken", "The name " + self.uname.get() + " is already taken.\nPlease use a different one.")
        else:
            dat[self.uname.get()] = {
                "name": self.uname.get(),
                "key": aes.aes256(self.key.encode(), self.passwd.get(), True).hex(),
                "test": aes.aes256(self.uname.get().encode(), self.passwd.get(), True).hex()
            }
            
            with open("acc.dat", "w") as accFile:
                json.dump(dat, accFile)
            
            mb.showinfo("Speedrun Desktop - Account Created", "Added the user " + self.uname.get() + "\nPlease login.")
            self.handleExit()

class PasswordApp(tkmt.ThemedTKinterFrame):
    def __init__(self):
        super().__init__("Speedrun Desktop - Password", "sun-valley", "dark", False, True)
        
        self.uname = tk.StringVar(self.root, "")
        self.passwd = tk.StringVar(self.root, "")
        
        self.createElements()
        
        self.run()
    
    def createElements(self):
        self.Text("Welcome to Speedrun Desktop", ("Segoe UI bold", 18))
        self.Text("Please login.")
        
        self.Seperator()
        
        self.unameContainer = self.addFrame("UsernameContainer", pady=0)
        
        self.unameContainer.Text("Username:", pady=0)
        self.unameContainer.Entry(self.uname)
        
        self.passwdContainer = self.addFrame("PasswordContainer", pady=0)
        
        self.passwdContainer.Text("Password:", pady=0)
        self.passwdEntry = self.passwdContainer.Entry(self.passwd, widgetkwargs={"show": "•"})
        self.passwdToggle = self.passwdContainer.Button("Show", self.showPasswd, row=1, col=1)
        self.passwdEntry.bind("<Return>", self.login)
        
        self.Button("New Account", self.newAccount)
        self.AccentButton("Login", self.login)
    
    def showPasswd(self, *args):
        self.passwdEntry.config(show="")
        self.passwdToggle.config(text="Hide", command=self.hidePasswd)
    
    def hidePasswd(self, *args):
        self.passwdEntry.config(show="•")
        self.passwdToggle.config(text="Show", command=self.showPasswd)
    
    def login(self, *args):
        res = validatePassword(self.uname.get(), self.passwd.get())
        
        if res[0]:
            spc.init(res[1])
            mb.showinfo("Speedrun Desktop - Correct Information", "Loaded API Successfully!\nWelcome, " + self.uname.get())
            self.root.withdraw()
            self.uname.set("")
            self.passwd.set("")
            self.hidePasswd()
            UIApp()
            spc.destroy()
            self.root.deiconify()
        else:
            match res[1]:
                case "uname":
                    mb.showerror("Speedrun Desktop - Incorrect Information", "Incorrect Username.\nThe username handles spaces at the start and end of it.")
                case "passwd":
                    mb.showerror("Speedrun Desktop - Incorrect Information", "Incorrect Password.\nThe password is case-sensitive and handles spaces at the start, and end of it.")
                case "error":
                    mb.showerror("Speedrun Desktop - Error", "An error occurred whilst checking the username and password.\nThis likely not due to an incorrect password.")
    
    def newAccount(self):
        self.root.withdraw()
        NewApp()
        self.root.deiconify()

class GameApp(tkmt.ThemedTKinterFrame):
    global img
    def __init__(self, game):
        super().__init__("Speedrun Desktop - " + game.name, "sun-valley", "dark", False, True)
        
        self.game = game
        self.runs = {}
        self.createElements()
        
        self.run()
    def createElements(self):
        global img
        
        try:
            img = Image.open(f"{os.getenv("TEMP")}\\{self.game.data["abbreviation"]}_cvr.png")
            img = img.resize(get_dimensions((img.width, img.height)))
            img = ImageTk.PhotoImage(img)
        except:
            warn("Error grabbing image for " + self.game.name)
            img = Image.open("resources/cover.png")
            img = img.resize(get_dimensions((img.width, img.height)))
            img = ImageTk.PhotoImage(img)
            
        self.temp = self.addFrame("TitleAndImageFrame")
        
        ifr = self.temp.addFrame("ImageFrame", pady=0, padx=0).Label(None, widgetkwargs={"image": img}, pady=0, padx=0)
        ifr.config(image=img)
        ifr.image = img
        
        self.temp.Text(self.game.name, ("Segoe UI bold", 18), row=0, col=1)
        
        self.categories = self.Notebook("Categories")
        
        for cat in self.game.categories:
            temp = self.categories.addTab(cat.data["name"])
    
    def getRuns(self, cat, *args):
        self.runs[cat.data["name"]]

class UIApp(tkmt.ThemedTKinterFrame):
    global img
    def __init__(self):
        super().__init__("Speedrun Desktop", "sun-valley", "dark", False, True)
        
        self.searchTerm = tk.StringVar(self.root, "Search...")
        self.gamesList = []
        self.playersList = []
        self.me = spc.me()
        self.gamePage = 0
        self.underline = tkFont.Font(self.root, ("Segoe UI", 8))
        self.underline.configure(underline = True)
        
        self.createElements()
        
        self.run()

    def createElements(self):
        self.Text("Logged in as " + self.me.name, pady=0)
        self.Text("Welcome to Speedrun Desktop", ("Segoe UI bold", 18), pady=0)
        
        temp = self.addFrame("SearchBarFrame", padx=10, pady=10)
        
        temp.Entry(self.searchTerm).bind("<Return>", self.updateSearch)
        temp.AccentButton("GO", self.updateSearch, row=0, col=1)
        
        self.tabs = self.Notebook("HomeTabs")
        self.games = self.tabs.addTab("Games")
        self.players = self.tabs.addTab("Users")
        temp = self.tabs.addTab("Credits")
        
        temp.Text("Credits", ("Segoe UI", 18))
        temp.Seperator()
        
        with open("creds.json", "r") as creds:
            links = []
            for cred in json.load(creds):
                temp.Text(cred["name"], ("Segoe UI bold", 11), pady=5)
                temp.Text(cred["user"], pady=0)
                temp.Text(cred["link"], widgetkwargs={"cursor": "no"}, pady=0)
                temp.Seperator(pady=0)
    
    def changeGamePage(self, change, *args):
        temp = self.gamePage + change
        if temp > -1 and temp < len(self.gamesList) :
            self.gamePage = temp
            clearFrame(self.games.master)
            self.createGameElements()
    
    def createGameElements(self, *args):
        global img
        for gm in self.gamesList[self.gamePage]:
            try:
                img = Image.open(f"{os.getenv("TEMP")}\\{gm.data["abbreviation"]}_cvr.png")
                img = img.resize(get_dimensions((img.width, img.height)))
                img = ImageTk.PhotoImage(img)
            except:
                warn("Error grabbing image for " + gm.name)
                img = Image.open("resources/cover.png")
                img = img.resize(get_dimensions((img.width, img.height)))
                img = ImageTk.PhotoImage(img)
            self.temp = self.games.addFrame("GMFrame" + gm.name, pady=0)
            ifr = self.temp.addFrame("ImageFrame").Label(None, widgetkwargs={"image": img}, pady=0)
            ifr.config(image=img)
            ifr.image = img
            self.temp.Text(gm.name, ("Segoe UI bold", 18), row=0, col=1)
            temp = self.games.addFrame("GMFrame1" + gm.name, pady=0)
            temp.AccentButton("Attempt", print)
            temp.Button("More Info", self.openGameApp, args=([gm]), row=0, col=1)
            self.games.Seperator(pady=2)
        
        self.gamePageControl = self.games.addFrame("PageControl", pady=0)
        
        self.gamePageControl.Button("<", self.changeGamePage, ([-1]))
        self.gamePageControl.Text(f"{self.gamePage + 1} / {len(self.gamesList)}", row=0, col=1)
        self.gamePageControl.Button(">", self.changeGamePage, ([1]), row=0, col=2)
    
    def updateSearch(self, *args):
        gsThread = t.Thread(target=self.updateGameSearch, name="GameSearchThread", args=([self.searchTerm.get()]))
        psThread = t.Thread(target=self.updatePlayerSearch, name="PlayerSearchThread", args=([self.searchTerm.get()]))
        
        gsThread.start()
        psThread.start()
        
        clearFrame(self.games.master)
        clearFrame(self.players.master)
        
        gsThread.join()
        self.createGameElements()
        psThread.join()
            
        for pl in self.playersList[0:4]:
            self.players.Text(pl.name, ("Segoe UI bold", 18))
            self.players.Seperator()
    
    def updateGameSearch(self, term, *args):
        try:
            self.gamesList = chunk_list(spc.search(spc.dt.Game, term), 3)
            gsdThread = t.Thread(target=self.downloadGameCovers, name="DownloadCoverThread", args=([0]))
            gsd1Thread = t.Thread(target=self.downloadGameCovers, name="DownloadCoverThread1", args=([1]))
            gsdThread.start()
            gsd1Thread.start()
            gsdThread.join()
            gsd1Thread.join()
        except Exception as e:
            error("Exception {0}{1!r}".format(type(e).__name__, e.args))
    
    def downloadGameCovers(self, start=0, *args):
        for gmp in self.gamesList:
            for gm in gmp[start::2]:
                if not os.path.exists(f"{os.getenv("TEMP")}\\{gm.data["abbreviation"]}_cvr.png"):
                    download_png(gm.data["assets"]["cover-tiny"]["uri"], f"{os.getenv("TEMP")}\\{gm.data["abbreviation"]}_cvr.png")
    
    def updatePlayerSearch(self, term, *args):
        try:
            self.playersList = spc.search(spc.dt.User, term)
        except Exception as e:
            error("Exception {0}{1!r}".format(type(e).__name__, e.args))
        
    def openGameApp(self, game):
        GameApp(game)

if __name__ == "__main__":
    PasswordApp()