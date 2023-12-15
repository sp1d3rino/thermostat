from flask import Flask, json, render_template

companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]

api = Flask(__name__)

@api.route('/', methods=['GET'])
def get_companies():
  return render_template('index.html')

@api.route('/companies', methods=['GET'])
def get_companies():
  return json.dumps(companies)

if __name__ == '__main__':
    api.run(port=5000, host='0.0.0.0')
    
