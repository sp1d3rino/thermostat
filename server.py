from flask import Flask, json, render_template, request
import os
import datetime


api = Flask(__name__)

def fwrite(filename,value):
  f = open(filename, "w")
  f.write(value)
  f.close()

def fread(filename):
  try:
    f = open(filename, "r")
    status= f.read()
    return status
  except IOError:
      return ''

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
  if (fread("tstatus.txt")=="on"):
    status="checked"
  else:
    status=""
  return render_template('index.html', ischecked=status,temp=fread("temp.txt"))


# APIs


# API temperature
@api.route('/temp', methods=["POST"])
def set_temp():
    temperature = request.json['temp']
    fwrite("temp.txt",temperature)
    return temperature

# API thermostat
@api.route('/status', methods=['GET'])
def get_status():
  return fread("tstatus.txt")

# API thermostat
@api.route('/on', methods=['GET'])
def get_on():
  fwrite("tstatus.txt","on")
  log("on")
  return render_template('index.html', ischecked="checked" )

# API thermostat
@api.route('/off', methods=['GET'])
def get_off():
  fwrite("tstatus.txt","off")
  log("off")
  return render_template('index.html',ischecked="")

if __name__ == '__main__':
    api.run(port=8088, host='0.0.0.0')
    
