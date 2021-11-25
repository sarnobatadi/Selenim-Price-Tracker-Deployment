from flask import Flask
app = Flask(__name__)

@app.route('/')
def homePg():
    return 'Home Page checkRoutineUpdate'

@app.route('/checkRoutineUpdate', methods=["GET"])
def updateDatabase():

    return 'Result is returned'

if __name__ == "__main__":
    app.run()
