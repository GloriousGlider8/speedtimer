import srcomapi as src
from srcomapi import datatypes as dt
import sys
from lib.logging import *

api = None

def init(api_key):
    global api
    api = src.SpeedrunCom(api_key, user_agent="GloriousGlider8/SpeedrunClientUI:v0.0.1;python/python:v" + sys.version.split(" ")[0])
    info("Initialized API with key <API_KEY> and agent GloriousGlider8/SpeedrunClientUI:v0.0.1;python/python:v" + sys.version.split(" ")[0])

def destroy():
    global api
    api = None
    info("Destroyed API, key <API_KEY> forgotten.")

def search(type, name):
    log("Searching for " + name + " with key <API_KEY>")
    return api.search(type, {"name": name})

def get(endpoint):
    log("Getting endpoint " + endpoint + " with key <API_KEY>")
    return api.get(endpoint)

def me():
    log("Getting self with key <API_KEY>")
    return dt.User(api, api.get("profile"))