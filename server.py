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

def logState(value):
   # Append-adds at last
  file1 = open("state-history", "a")  # append mode
  ct = datetime.datetime.now()
  time_str =str(ct) 
  file1.write(time_str+" state: "+value+ " \n")
  file1.close()

def logTemp(value):
   # Append-adds at last
  file1 = open("temp-history", "a")  # append mode
  ct = datetime.datetime.now()
  time_str =str(ct) 
  file1.write(time_str+" temp: "+value+ " \n")
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
    # read token
    if (request.headers.get('Authorization')!=fread("token.key").strip()):
      return("Invalid token!");
    temperature = request.json['temp']
    logTemp(temperature)
    fwrite("temp.txt",temperature)
    return fread("tstatus.txt")

# API thermostat
@api.route('/status', methods=['GET'])
def get_status():
  return fread("tstatus.txt")

# API thermostat
@api.route('/on', methods=['GET'])
def get_on():
  # read token
  if (request.headers.get('Authorization')!=fread("token.key").strip()):
    return("Invalid token!");  
  fwrite("tstatus.txt","on")
  logState("on")
  return render_template('index.html', ischecked="checked" )

# API thermostat
@api.route('/off', methods=['GET'])
def get_off():
  # read token
  if (request.headers.get('Authorization')!=fread("token.key").strip()):
    return("Invalid token!");  
  fwrite("tstatus.txt","off")
  logState("off")
  return render_template('index.html',ischecked="")

if __name__ == '__main__':
    api.run(port=8088, host='0.0.0.0')
    
