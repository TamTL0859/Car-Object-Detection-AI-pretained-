@echo off

start cmd /K python "C:\Users\XXXXX\Documents\Projects\Python\ComputerVisionProject\ComputerVision\Backend\main.py"
:: edit XXXXX to your path if you want to use the start script
start cmd /K python -m http.server 8001 --directory "C:\Users\XXXXX\Documents\Projects\Python\ComputerVisionProject\ComputerVision\Frontend"

start http://127.0.0.1:8001/index.html
