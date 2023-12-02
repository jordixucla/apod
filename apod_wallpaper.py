import os
import requests
import ctypes
import time
import sys
import subprocess
import shutil
import winreg

def download_apod():
    url = "https://apod.nasa.gov/apod/"
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        start = html.find("<a href=\"image") + 9
        end = html.find(".jpg", start) + 4
        img_url = url + html[start:end]
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            with open("apod.jpg", "wb") as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)

def set_wallpaper():
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, os.path.abspath("apod.jpg"), 0)

def install_service():
    script_path = os.path.abspath(sys.argv[0])
    service_name = "APOD Wallpaper"
    service_display_name = "APOD Wallpaper Service"
    service_description = "Sets the Astronomy Picture of the Day as your Windows wallpaper every day."
    key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Services\\" + service_name)
    winreg.SetValueEx(key, "ImagePath", 0, winreg.REG_SZ, script_path)
    winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, service_display_name)
    winreg.SetValueEx(key, "Description", 0, winreg.REG_SZ, service_description)
    winreg.SetValueEx(key, "Start", 0, winreg.REG_DWORD, 2)
    winreg.CloseKey(key)
    subprocess.call(["sc", "start", service_name])

download_apod()
set_wallpaper()
# install_service()
