from flask import Flask, json, render_template
import os
import datetime


api = Flask(__name__)

def write_status(value):
  f = open("tstatus.txt", "w")
  f.write(value)
  f.close()

def log(value):
   # Append-adds at last
  file1 = open("history", "a")  # append mode
  ct = datetime.datetime.now()
  time_str =str(ct) 
  file1.write(time_str+" position:"+value+ " \n")
  file1.close()

@api.route('/', methods=['GET'])
def get_index():
  f = open("tstatus.txt", "r")
  status= f.read()
  return render_template('index.html', pos=status)

@api.route('/on', methods=['GET'])
def get_on():
  write_status("130")
  log("130")
  return render_template('index.html', pos="130")

@api.route('/off', methods=['GET'])
def get_off():
  write_status("90")
  log("90")
  os.environ['TSTATUS']="90"
  return render_template('index.html', pos="90")

if __name__ == '__main__':
    api.run(port=8088, host='0.0.0.0')
    
