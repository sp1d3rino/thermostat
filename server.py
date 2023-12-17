from flask import Flask, json, render_template, request
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


def log(value):
   # Append-adds at last
  file1 = open("history", "a")  # append mode
  ct = datetime.datetime.now()
  time_str =str(ct) 
  file1.write(time_str+" state: "+value+ " \n")
  file1.close()

# frontend
@api.route('/', methods=['GET'])
def get_index():
  if (read_status()=="on"):
    status="checked"
  else:
    status=""
  return render_template('index.html', ischecked=status)


# APIs


# API temperature
@api.route('/guide', methods=["POST"])
def set_temp():
    temp = request.json['temp']
    return "200"

# API thermostat
@api.route('/status', methods=['GET'])
def get_status():
  return read_status()

# API thermostat
@api.route('/on', methods=['GET'])
def get_on():
  write_status("on")
  log("on")
  return render_template('index.html', ischecked="checked" )

# API thermostat
@api.route('/off', methods=['GET'])
def get_off():
  write_status("off")
  log("off")
  return render_template('index.html',ischecked="")

if __name__ == '__main__':
    api.run(port=8088, host='0.0.0.0')
    
