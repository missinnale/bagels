import os
import datetime
from flask import Flask, render_template
app = Flask(__name__)


def openTmp():
    try:
        bagelTxt = open("./tmp/aretherebagels.txt", "r")
    except OSError:
        return False
    bagelInfo = bagelTxt.read()
    bagelTxt.close()
    bagelArray = bagelInfo.split(' ')
    if len(bagelArray) > 1:
        print("Someone messed with the account")
        return
    bagelArray = bagelArray[0].split("\n")
    bagels = bagelArray[0].lower()
    if bagels == "yes":
        return True
    return False


def deleteTmp():
    mtime = os.path.getmtime("./tmp/aretherebagels.txt")
    date = datetime.datetime.fromtimestamp(mtime)
    now = datetime.datetime.now()
    elapsedtime = now - date
    if elapsedtime.days > 0 or elapsedtime.seconds > 7200:
        os.remove("./tmp/aretherebagels.txt")


@app.route('/')
def bagels():
    aretherebagels = openTmp()
    deleteTmp()
    if aretherebagels:
        return render_template('bagels.html')
    else:
        return render_template('nobagels.html')

if __name__ == '__main__':
    app.run(debug=True)
