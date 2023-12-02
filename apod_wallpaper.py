import os
import sys
import requests
import ctypes
import time
import subprocess

from datetime import datetime, timedelta


def download_apod():
    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')

    # Build the URL for today's APOD
    url = f'https://apod.nasa.gov/apod/ap{today[2:]}.html'

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the image URL from the HTML response
        image_url = 'https://apod.nasa.gov/apod/' + \
            response.text.split('<a href="image')[1].split('">')[0]

        # Download the image
        response = requests.get(image_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Save the image to disk
            with open('apod.jpg', 'wb') as f:
                f.write(response.content)

            # Set the wallpaper
            SPI_SETDESKWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER, 0, os.path.abspath('apod.jpg'), 0)


def install_service():
    # Get the path to the Python executable
    python_exe = sys.executable

    # Get the path to the script
    script_path = os.path.abspath(__file__)

    # Build the command to install the service
    command = f'sc create "APOD Wallpaper" binPath= "{python_exe} {script_path}" start= auto'

    # Run the command
    subprocess.run(command, shell=True)


if __name__ == '__main__':
    # Download today's APOD
    download_apod()

    # Install the service
    install_service()
