from flask import Flask, json, render_template
import os
import datetime


api = Flask(__name__)

def write_status(value):
  f = open("tstatus.txt", "w")
  f.write(value)
  f.close()

def read_status():
  f = open("tstatus.txt", "r")
  status= f.read()
  return status

def updateButton():
  status=read_status()
  if status==90:
    return "images/button_off.png"
  else:
    return "images/button_on.png"

def log(value):
   # Append-adds at last
  file1 = open("history", "a")  # append mode
  ct = datetime.datetime.now()
  time_str =str(ct) 
  file1.write(time_str+" position:"+value+ " \n")
  file1.close()

# frontend
@api.route('/', methods=['GET'])
def get_index():
  status=read_status()
  icon_path="./images/button_off.png"
  return render_template('index.html', pos=status, button_image=icon_path)


# APIs

@api.route('/status', methods=['GET'])
def get_status():
  return read_status()


@api.route('/on', methods=['GET'])
def get_on():
  write_status("130")
  log("130")
  icon_path=updateButton()
  return render_template('index.html', pos="130", button_image=icon_path)

@api.route('/off', methods=['GET'])
def get_off():
  write_status("90")
  log("90")
  icon_path=updateButton()
  return render_template('index.html', pos="90", button_image=icon_path)

if __name__ == '__main__':
    api.run(port=8088, host='0.0.0.0')
    
