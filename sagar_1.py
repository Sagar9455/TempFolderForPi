[Unit]
Description=My Startup Script
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/your_script.py
WorkingDirectory=/home/pi
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
