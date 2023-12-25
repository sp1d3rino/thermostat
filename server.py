from flask import Flask, json, render_template, request
import os
import datetime
import subprocess

HTTP_OK = "200";

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

def saveAvgTemp(ctemp):
  f = open("tempavg", "r")
  row= f.read()
  line= row.split() 
  sum = float(line[0])
  count = float(line[1])  
  sum = sum + float(ctemp)
  count = count +1
  avg = sum / count
  
  file1 = open("tempavg", "w")  # append mode
  file1.write("{:.2f}".format(sum) +" "+"{:.2f}".format(count)+" "+ "{:.2f}".format(avg))
  file1.close()



# frontend 
# returns the index.html webpage
@api.route('/', methods=['GET'])
def get_index():
  if (fread("tstatus.txt")=="on"):
    status="checked"
  else:
    status=""
  return render_template('index.html', ischecked=status,temp=fread("temp.txt"))


# APIs


# API temperature
# this API is used by ESP8266 to send temperature and 
# receive last thermostat status saved on the server 
@api.route('/temp', methods=["POST"])
def set_temp():
    # read token
    if (request.headers.get('Authorization')!=fread("token.key").strip()):
      return("Invalid token!");
    temperature = request.json['temp']
    logTemp(temperature)
    fwrite("temp.txt",temperature)
    saveAvgTemp(temperature)
    return fread("tstatus.txt")

# API thermostat
# for any endpoints that want to know 
# what is the latest saved state
@api.route('/status', methods=['GET'])
def get_status():
  return fread("tstatus.txt")


# API thermostat
# to set ON therm status on server
@api.route('/on', methods=['GET'])
def get_on():
  # read token
  if (request.headers.get('Authorization')!=fread("token.key").strip()):
    return("Invalid token!");  
  fwrite("tstatus.txt","on")
  logState("on")
  #return render_template('index.html', ischecked="checked" )
  return HTTP_OK;

# API thermostat
# to set OFF therm status on server
@api.route('/off', methods=['GET'])
def get_off():
  # read token
  if (request.headers.get('Authorization')!=fread("token.key").strip()):
    return("Invalid token!");  
  fwrite("tstatus.txt","off")
  logState("off")
  #return render_template('index.html',ischecked="")
  return HTTP_OK;

# API thermostat
# to get temp (e.g. called by mobile app)
@api.route('/temp', methods=['GET'])
def get_temp():
  return fread("temp.txt")

# API thermostat
# to get min temp (e.g. called by mobile app)
@api.route('/lowertemp', methods=['GET'])
def get_lower_temp():
  process = subprocess.Popen(['./scripts/getmin.sh'], stdout=subprocess.PIPE)
  stdout = process.communicate()[0]
  return stdout

# API thermostat
# to get max temp (e.g. called by mobile app)
@api.route('/highertemp', methods=['GET'])
def get_higher_temp():
  process = subprocess.Popen(['./scripts/getmax.sh'], stdout=subprocess.PIPE)
  stdout = process.communicate()[0]
  return stdout

# API thermostat
# to get mean temp (e.g. called by mobile app)
@api.route('/avgtemp', methods=['GET'])
def get_avg_temp():
  process = subprocess.Popen(['./scripts/getavg.sh'], stdout=subprocess.PIPE)
  stdout = process.communicate()[0]
  return stdout


# API thermostat
# to get all stastitics from one service (e.g. called by mobile app)
@api.route('/statistics', methods=['GET'])
def get_all_statistics_temp():
  return str(get_lower_temp())+" "+str(get_higher_temp())+" "+str(get_avg_temp())

if __name__ == '__main__':    
   #api.run(port=8088, host='0.0.0.0', ssl_context=('./certificates/server.crt', './certificates/server.key'))
   api.run(port=8088, host='0.0.0.0')
    
