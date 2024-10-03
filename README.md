# My Flask Project

This is a Flask application designed to control relay 1 and relay 2, which can be used for home automation or other control systems. The project is hosted on a Raspberry Pi 4 and can be used to trigger relays via a web interface.

## Features

- Control Relay 1 and Relay 2 via a web interface.
- Simple and responsive interface built with Flask.
- Easily deployable on Raspberry Pi 4 or other similar hardware.

## Requirements

To run this project, you will need:

- Python 3.x
- Flask
- Raspberry Pi (for hardware setup)
- Relay module connected to Raspberry Pi GPIO pins

## Installation

1. Clone the repository:
  git clone https://github.com/mnedev-cell/my_flask_project.git
  cd my_flask_project
   
2.Install dependencies:
  pip install -r requirements.txt
  
3.Run the Flask application:
  python app.py

Step 2: Start Flask Server at Boot on Raspberry Pi

1.Create a Systemd Service File: Open a terminal and create a new service file:
  sudo nano /etc/systemd/system/flaskapp.service

2.Add the Following Configuration: Replace /path/to/your/app (/home/pi/my_flask_project) and app.py with the actual path and name of your Flask application file.

  [Unit]
  Description=Flask Application
  After=network.target
  
  [Service]
  User=pi
  WorkingDirectory=/path/to/your/app
  ExecStart=/usr/bin/python3 app.py
  Restart=always
  
  [Install]
  WantedBy=multi-user.target
