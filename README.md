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

## Installation Service Flask

Start Flask Server at Boot on Raspberry Pi

- Create a Systemd Service File: Open a terminal and create a new service file:
  sudo nano /etc/systemd/system/flaskapp.service
  
  Add the Following Configuration: 

      [Unit]
      Description=Flask Application
      After=network.target
      
      [Service]
      User=pi
      WorkingDirectory=/path/to/your/app   #  Replace /path/to/your/app (/home/pi/my_flask_project
      ExecStart=/usr/bin/python3 app.py    #  Replace app.py /home/pi/my_flask_project/app.py
      Restart=always
      StandardOutput=journal
      StandardError=journal
      SyslogIdentifier=flaskapp_service

      
      [Install]
      WantedBy=multi-user.target

 - Reload systemd daemon to recognize the new service
 - ```shell
 sudo systemctl daemon-reload
```

- Start the service flaskapp
  sudo systemctl start flaskapp
  
- check status flaskapp
  sudo systemctl status flaskapp

- enable service flaskapp
  sudo systemctl enable flaskapp

- disable service flaskapp
   sudo systemctl disable flaskapp
  
- stop the service flaskapp
   sudo systemctl stop flaskapp
  
- Restart the service
  sudo systemctl restart flaskapp


