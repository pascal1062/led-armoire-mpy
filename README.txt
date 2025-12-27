esp32 to control under cabinet led dimming. Board is completely self controlled, time schedule and sunset calculations.

Wifi enable. IP address 192.168.0.20 

Data exchange with esp32 done through wifi on port 47902-UDP with node-red as a GUI for display and interaction with MQTT.

RTC time is done every hour through node-red (192.168.0.90)

webrepl is not enabled. ftp server instead.

FTP server is running on the esp32. Code edition is done with vscode and SFTP package.

Local-PC files are located in folder "/home/pascal/Documents/Projets/micropython/led-armoire"

1- Open vscode and connect to the esp32 with SFTP. You have access to all files
2- To edit python files, download desired file to local PC folder and edit as you want
3- Then upload edited files to the esp32. 
4- Reset the board to have "modified code" take effect. Use reset command with node-red


Sync to github

Local-PC folder "/home/pascal/Documents/Projets/micropython/led-armoire" has git enable
Keep all esp32 files same as local-PC files and sync to github "led-armoire-mpy" repo
