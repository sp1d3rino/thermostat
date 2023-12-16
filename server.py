from flask import Flask, json, render_template
import os
import datetime


api = Flask(__name__)

def log(value):
   # Append-adds at last
  file1 = open("history", "a")  # append mode
  ct = datetime.datetime.now()
  time_str =str(ct) 
  file1.write(time_str+" position:"+value+ " \n")
  file1.close()

@api.route('/', methods=['GET'])
def get_index():
  status= os.getenv("TSTATUS")
  return render_template('index.html', pos=status)

@api.route('/on', methods=['GET'])
def get_on():
  os.environ['TSTATUS']="130"
  log("130")
  return render_template('index.html', pos="130")

@api.route('/off', methods=['GET'])
def get_off():
  log("90")
  os.environ['TSTATUS']="90"
  return render_template('index.html', pos="90")

if __name__ == '__main__':
    api.run(port=5000, host='0.0.0.0')
    
