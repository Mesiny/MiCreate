from api.api import *
import shutil
import speedtest
from flask import Flask,send_from_directory
import threading
import requests


if __name__ == '__main__':
    api = API()
    api.get_mac_address()
 
