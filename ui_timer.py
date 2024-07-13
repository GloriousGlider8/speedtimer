import lib.timing as tm
import threading as t
import json
import TKinterModernThemes as tkmt
from time import sleep as wait
from lib.logging import *
import os
import webbrowser as wb
from PIL import Image, ImageTk
import tkinter.font as tkFont
import glob
import tkinter as tk
from math import gcd

def get_dimensions1(dimensions):
    height, width = dimensions
    factor = gcd(height, width)
    
    simplified_height = height // factor
    simplified_width = width // factor
    
    multiplier = 64 // simplified_height
    if 64 % simplified_height != 0:
        multiplier += 2
    
    new_height = simplified_width * multiplier
    new_width = simplified_height * multiplier

    return new_width, new_height
    
def clearFrame(frame):
    for widget in frame.winfo_children():
       widget.destroy()

def get_dimensions(dimensions):
    height, width = dimensions
    
    new_height = height // 4
    new_width = width // 4 // 2
    
    return new_width, new_height

def compare_times(time1, time2):
    if time1["h"] > time2["h"]:
        return ">"
    elif time1["h"] < time2["h"]:
        return "<"
    
    if time1["m"] > time2["m"]:
        return ">"
    elif time1["m"] < time2["m"]:
        return "<"
    
    if time1["s"] > time2["s"]:
        return ">"
    elif time1["s"] < time2["s"]:
        return "<"
    
    if time1["ms"] > time2["ms"]:
        return ">"
    elif time1["ms"] < time2["ms"]:
        return "<"
    
    return "="

def convert_ms(milliseconds):
    milliseconds = abs(milliseconds)  # Work with absolute value for calculations

    # Calculate total seconds
    total_seconds = milliseconds // 1000
    # Calculate remaining milliseconds
    remaining_ms = milliseconds % 1000

    # Calculate total minutes
    total_minutes = total_seconds // 60
    # Calculate remaining seconds
    seconds = total_seconds % 60

    # Calculate total hours
    hours = total_minutes // 60
    # Calculate remaining minutes
    minutes = total_minutes % 60

    return hours, minutes, seconds, remaining_ms

def format_time(time_dict):
    return f"{time_dict["h"]:02}:{time_dict["m"]:02}:{time_dict["s"]:02}.{time_dict["ms"]:03}"

def dict_to_milliseconds(time_dict):
    hours = time_dict.get("h", 0)
    minutes = time_dict.get("m", 0)
    seconds = time_dict.get("s", 0)
    milliseconds = time_dict.get("ms", 0)

    total_milliseconds = (
        hours * 3600000 +  # 1 hour = 3600000 milliseconds
        minutes * 60000 +  # 1 minute = 60000 milliseconds
        seconds * 1000 +   # 1 second = 1000 milliseconds
        milliseconds       # milliseconds
    )

    return total_milliseconds

def time_difference(time1, time2):
    if time1["h"] - time2["h"] > 0:
        return "x Obsolete"
    
    t1ms = dict_to_milliseconds(time1)
    t2ms = dict_to_milliseconds(time2)
    
    diff = t1ms - t2ms
    
    sign = "±"
    
    if diff > 0:
        sign = "+"
    elif diff < 0:
        sign = "-"
    
    h, m, s, ms = convert_ms(diff)
    
    result = f"{sign}{m:02}:{s:02}.{ms:03}"
    
    return result

class TimerUI(tkmt.ThemedTKinterFrame):
    global img
    global pImg
    def __init__(self, target):
        super().__init__("Speedrun Desktop - Stopwatch", "sun-valley", "dark", False, True)
        
        self.root.resizable(False, False)
        
        with open(target, "r") as jsFile:
            self.target = json.load(jsFile)

        self.textColor = "#ffffff"
        if self.mode == "light":
            self.textColor = "#000000"
        self.sepColor = "#2e2e2e"
        if self.mode == "light":
            self.sepColor = "#747474"
        self.segment = 0
        self.pos = 1
        self.timer = tm.Stopwatch()
        self.update = True
        self.underline = tkFont.Font(self.root, ("Segoe UI", 8))
        self.underline.configure(underline = True)
        self.createElements()
        
        self.updThread = t.Thread(target=self.updateThread)
        self.pauseUpdThread = t.Thread(target=self.pauseUpdateThread)
        self.updThread.start()
        self.pauseUpdThread.start()
        
        self.run()
        self.update = False
    
    def createElements(self):
        global img
        global pImg
        try:
            pImg = Image.open("resources/pos1.png")
            pImg = pImg.resize(get_dimensions((pImg.width, pImg.height)))
            pImg = ImageTk.PhotoImage(pImg)
        except:
            warn("Error grabbing image for resources/pos1.png")
            pImg = Image.open("resources/question.png")
            pImg = pImg.resize(get_dimensions((pImg.width, pImg.height)))
            pImg = ImageTk.PhotoImage(pImg)
        
        self.posFrm = self.addFrame("PositionContentFrame", pady=10, padx=5)
        self.posImg = self.posFrm.Label(None, widgetkwargs={"image": pImg}, pady=0, padx=0)
        self.posImg.config(image=pImg)
        self.posImg.image = pImg
        
        temp = self.posFrm.addFrame("1stPositionMarker", padx=0, pady=0)
        temp.Text(f"1st - {self.target["leaderboard"][0]["name"]}", widgetkwargs={"foreground": "#b38b3f"}, pady=0, padx=0)
        temp1 = temp.Text("Video Link", self.underline, widgetkwargs={"foreground": "#b38b3f", "cursor": "hand2"}, pady=0, padx=0)
        if self.target["leaderboard"][0]["link"]:
            temp1.bind("<Button-1>", lambda e: wb.open(self.target["leaderboard"][0]["link"]))
        else:
            temp1.config(foreground="#6f727b", cursor="no")
        temp.Text(format_time(self.target["leaderboard"][0]["time"]), ("Digital-7 mono", 18), widgetkwargs={"foreground": "#b38b3f"}, pady=0, padx=0)
        
        temp = self.posFrm.addFrame("2ndPositionMarker", padx=0, pady=0)
        temp.Text(f"2nd - {self.target["leaderboard"][1]["name"]}", widgetkwargs={"foreground": "#96967b"}, pady=0, padx=0)
        temp1 = temp.Text("Video Link", self.underline, widgetkwargs={"foreground": "#96967b", "cursor": "hand2"}, pady=0, padx=0)
        if self.target["leaderboard"][1]["link"]:
            temp1.bind("<Button-1>", lambda e: wb.open(self.target["leaderboard"][1]["link"]))
        else:
            temp1.config(foreground="#6f727b", cursor="no")
        temp.Text(format_time(self.target["leaderboard"][1]["time"]), ("Digital-7 mono", 18), widgetkwargs={"foreground": "#96967b"}, pady=0, padx=0)
        
        temp = self.posFrm.addFrame("3rdPositionMarker", padx=0, pady=0)
        temp.Text(f"3rd - {self.target["leaderboard"][2]["name"]}", widgetkwargs={"foreground": "#c66741"}, pady=0, padx=0)
        temp1 = temp.Text("Video Link", self.underline, widgetkwargs={"foreground": "#c66741", "cursor": "hand2"}, pady=0, padx=0)
        if self.target["leaderboard"][2]["link"]:
            temp1.bind("<Button-1>", lambda e: wb.open(self.target["leaderboard"][2]["link"]))
        else:
            temp1.config(foreground="#6f727b", cursor="no")
        temp.Text(format_time(self.target["leaderboard"][2]["time"]), ("Digital-7 mono", 18), widgetkwargs={"foreground": "#c66741"}, pady=0, padx=0)
        
        self.sep1 = self.Text("", row=0, col=1, widgetkwargs={"foreground": self.sepColor})
        
        self.timerFrm = self.addFrame("TimerContentFrame", row=0, col=2, pady=10, padx=5)
        try:
            img = Image.open(f"{os.getenv("TEMP")}/{self.target["id"]}_cvr.png")
            img = img.resize(get_dimensions((img.width, img.height)))
            img = ImageTk.PhotoImage(img)
        except:
            warn(f"Error grabbing image for {os.getenv("TEMP")}/{self.target["id"]}_cvr.png")
            img = Image.open("resources/cover.png")
            img = img.resize(get_dimensions((img.width, img.height)))
            img = ImageTk.PhotoImage(img)
            
        self.coverImg = self.timerFrm.Label(None, widgetkwargs={"image": img}, pady=0, padx=0)
        self.coverImg.config(image=img)
        self.coverImg.image = img
        
        self.timerFrm.Text(self.target["name"], pady=0)
        self.timerFrm.Text(self.target["category"], ("Segoe UI bold", 12), pady=0)
        self.segmentText = self.timerFrm.Text(self.target["segments"][self.segment]["name"], ("Segoe UI bold", 16), pady=0)
        self.timerText = self.timerFrm.Text("00:00:00.000\n±00:00.000", widgetkwargs={"foreground": "#00aaff"}, fontargs=("Digital-7 mono", 18))
        self.nextSegButton = self.timerFrm.AccentButton("Next Segment", self.nextSegment)
        self.timerFrm.Button("Start", self.timer.start)
        self.timerFrm.Button("Pause", self.timer.pause)
        self.timerFrm.Button("Restart", self.restartRun)
        
        self.sep2 = self.Text("", row=0, col=3, widgetkwargs={"foreground": self.sepColor})
        
        self.segmentFrm = self.addFrame("SegmentContentFrame", row=0, col=4, pady=10, padx=5)
        for seg in self.target["segments"]:
            temp = self.segmentFrm.addFrame("SegmentFrame" + seg["name"], padx=0, pady=0)
            temp.Text(seg["name"])
        
        self.root.after(100, self.setSeparators)
    
    def setSeparators(self):
        self.sep1.config(text=("|\n" * ((self.root.winfo_height() // 13) - 8)).strip())
        self.sep2.config(text=("|\n" * ((self.root.winfo_height() // 13) - 8)).strip())
    
    def restartRun(self):
        self.nextSegButton.config(text="Next Segment", command=self.nextSegment)
        self.segment = 0
        self.segmentText.config(text=self.target["segments"][self.segment]["name"], foreground=self.textColor)
        self.timer.reset()
    
    def rerunRun(self):
        self.update = True
        self.updThread = t.Thread(target=self.updateThread)
        self.pauseUpdThread = t.Thread(target=self.pauseUpdateThread)
        self.updThread.start()
        self.pauseUpdThread.start()
        self.restartRun()
    
    def finishRun(self):
        t.Thread(target=self.finishRunThread).start()
    
    def finishRunThread(self):
        self.timer.pause()
        self.update = False
        self.segmentText.config(text="Hang on...", foreground="#ffcd00")
        self.updThread.join()
        self.pauseUpdThread.join()
        self.segmentText.config(text="Finish!", foreground="#ffff0e")
        match self.pos:
            case 1:
                temp = "#b38b3f"
            case 2:
                temp = "#96967b"
            case 3:
                temp = "#c66741"
            case 4:
                temp = "#b2cf6f"
            case _:
                temp = "#925bf5"
        self.timerText.config(text=self.timer.get_string_time(), foreground=temp)
        self.nextSegButton.config(text="Rerun", command=self.rerunRun)
    
    def nextSegment(self):
        self.segment += 1
        self.segmentText.config(text=self.target["segments"][self.segment]["name"])
        if self.segment + 1 >= len(self.target["segments"]):
            self.nextSegButton.config(text="Finish Run", command=self.finishRun)
    
    def setPos(self, position):
        global pImg
        try:
            pImg = Image.open(f"resources/pos{position}.png")
            pImg = pImg.resize(get_dimensions((pImg.width, pImg.height)))
            pImg = ImageTk.PhotoImage(pImg)
        except:
            warn(f"Error grabbing image for resources/pos{position}.png")
            pImg = Image.open("resources/question.png")
            pImg = pImg.resize(get_dimensions((pImg.width, pImg.height)))
            pImg = ImageTk.PhotoImage(pImg)
        
        self.pos = position
            
        self.posImg.config(image=pImg)
        self.posImg.image = pImg
    def updateThread(self):
        while self.update:
            wait(0.04)
            time = self.timer.get_dict_time()
            self.timerText.config(text=self.timer.get_string_time() + "\n" + time_difference(time, self.target["segments"][self.segment]["target"]))
            
            if self.timer.running:
                match compare_times(time, self.target["segments"][self.segment]["target"]):
                    case "=":
                        self.timerText.config(foreground="#ff945f")
                    case ">":
                        self.timerText.config(foreground="#ff5f5f")
                    case "<":
                        self.timerText.config(foreground="#94ff5f")
                
                match compare_times(time, self.target["leaderboard"][0]["time"]):
                    case "<":
                        if self.pos != 1:
                            self.setPos(1)
                    case "=":
                        if self.pos != 1:
                            self.setPos(1)
                    case ">":
                        if compare_times(time, self.target["leaderboard"][1]["time"]) == ">":
                            if compare_times(time, self.target["leaderboard"][2]["time"]) == ">":
                                if self.pos != 4:
                                    self.setPos(4)
                            else:
                                if self.pos != 3:
                                    self.setPos(3)
                        else:
                            if self.pos != 2:
                                self.setPos(2)
    
    def pauseUpdateThread(self):
        while self.update:
            wait(0.04)
            if not self.timer.running:
                time = self.timer.get_dict_time()
                if time["h"] == 0 and time["m"] == 0 and time["s"] == 0 and time["ms"] == 0:
                    self.timerText.config(foreground="#00aaff")
                else:
                    match compare_times(time, self.target["segments"][self.segment]["target"]):
                        case "=":
                            self.timerText.config(foreground="#ff945f")
                        case ">":
                            self.timerText.config(foreground="#ff5f5f")
                        case "<":
                            self.timerText.config(foreground="#94ff5f")
                if self.timer.running:
                    continue
                wait(1)
                if self.timer.running:
                    continue
                if time["h"] == 0 and time["m"] == 0 and time["s"] == 0 and time["ms"] == 0:
                    self.timerText.config(foreground="#00699d")
                else:
                    match compare_times(time, self.target["segments"][self.segment]["target"]):
                        case "=":
                            self.timerText.config(foreground="#9d5a3a")
                        case ">":
                            self.timerText.config(foreground="#9d3a3a")
                        case "<":
                            self.timerText.config(foreground="#5b9d3a")
                if self.timer.running:
                    continue
                wait(1)

class TargetChooseUI(tkmt.ThemedTKinterFrame):
    global img
    def __init__(self, name="NULL"):
        super().__init__("Speedrun Desktop - Choose Target", "sun-valley", "dark", False, True)
        
        self.name = name
        self.query = tk.StringVar(self.root, "")
        self.createElements()
        self.updateSearch()
        self.query.set("Search...")
        
        self.run()
    
    def createElements(self):
        self.Text("Welcome, " + self.name, ("Segoe UI bold", 18))
        self.Text("Please choose a target.")
        
        self.Seperator()
        
        temp = self.addFrame("QueryContentFrame", pady=0, padx=0)
        temp.Entry(self.query)
        temp.AccentButton("GO", self.updateSearch, row=0, col=1)
        
        self.targetFrame = self.addFrame("TargetContentFrame", pady=0, padx=0)

    def updateSearch(self):
        global img
        clearFrame(self.targetFrame.master)
        for targ in glob.glob("targets/*" + self.query.get() + "*.spdtarg")[0:5]:
            with open(targ, "r") as jsFile:
                dat = json.load(jsFile)
                
                try:
                    img = Image.open(f"{os.getenv("TEMP")}/{dat["id"]}_cvr.png")
                    img = img.resize(get_dimensions1((img.width, img.height)))
                    img = ImageTk.PhotoImage(img)
                except:
                    warn(f"Error grabbing image for {os.getenv("TEMP")}/{dat["id"]}_cvr.png")
                    img = Image.open("resources/cover.png")
                    img = img.resize(get_dimensions1((img.width, img.height)))
                    img = ImageTk.PhotoImage(img)
                
                temp = self.targetFrame.addFrame("TargetContent" + dat["id"] + "Frame", pady=0, padx=0)
                
                temp1 = temp.addFrame("ImageContentFrame", pady=0, padx=0)
                
                temp2 = temp1.Text(None, widgetkwargs={"image": img}, pady=0, padx=0)
                temp2.config(image=img)
                temp2.image = img
                
                temp1 = temp1.addFrame("TextContentFrame", row=0, col=1, pady=0, padx=0)
                
                temp1.Text(dat["name"], ("Segoe UI bold", 14))
                temp1.Text(dat["category"] + " - " + dat["date"], ("Segoe UI italic", 10))
                
                temp2 = temp1.addFrame("PlacementContentFrame", pady=0, padx=0)
                
                temp2.Text(dat["leaderboard"][0]["name"], widgetkwargs={"foreground": "#b38b3f"}, padx=0)
                temp2.Text(dat["leaderboard"][1]["name"], widgetkwargs={"foreground": "#96967b"}, row=0, col=1, padx=0)
                temp2.Text(dat["leaderboard"][2]["name"], widgetkwargs={"foreground": "#c66741"}, row=0, col=2, padx=0)
                
                temp2 = temp1.addFrame("PBContentFrame", pady=0, padx=0)
                
                temp2.Text("Personal Best: ", widgetkwargs={"foreground": "#925bf5"})
                temp2.Text(format_time(dat["pb"]) if dat["pb"] else "00:00:00.000", ("Digital-7 mono", 15), row=0, col=1, widgetkwargs={"foreground": "#ffff0e"})
                
                temp2 = temp1.addFrame("ActionContentFrame", pady=0, padx=0)
                
                temp2.AccentButton("Attempt WR", self.attemptRun, args=([targ]))
                temp2.Button("Attempt PB", print, row=0, col=1)
                
                temp.Seperator()
    def attemptRun(self, run, *args):
        self.root.withdraw()
        TimerUI(run)
        self.root.deiconify()

if __name__ == "__main__":
    TargetChooseUI("DEVELOPER")