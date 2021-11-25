import os
from flask import Flask
#from main import  algo
app = Flask(__name__)
port = int(os.environ.get('PORT', 5000))
@app.route('/')
def homePg():
    return 'Home Page checkRoutineUpdate'

@app.route('/checkRoutineUpdate', methods=["GET"])
def updateDatabase():
    algo()
    return 'Result is returned'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
