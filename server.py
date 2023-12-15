from flask import Flask, json, render_template
import os


api = Flask(__name__)

@api.route('/', methods=['GET'])
def get_index():
  status= os.getenv("TSTATUS")
  return render_template('index.html', pos=status)

@api.route('/on', methods=['GET'])
def get_on():
  return render_template('index.html', pos="130")

@api.route('/off', methods=['GET'])
def get_off():
  return render_template('index.html', pos="90")

if __name__ == '__main__':
    api.run(port=5000, host='0.0.0.0')
    
