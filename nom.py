from flask import Flask, render_template
app = Flask(__name__)

def openTmp():
    bagelTxt = open("./tmp/aretherebagels.txt", "r")
    bagelInfo = bagelTxt.read()
    bagelArray = bagelInfo.split(' ')
    if len(bagelArray) > 1:
        print("Someone messed with the account")
        return
    bagelArray = bagelArray[0].split("\n")
    bagels = bagelArray[0].lower()
    print(bagels)
    if bagels == "yes":
        aretherebagels = True
    elif bagels == "no":
        aretherebagels = False
    else:
        aretherebagels = None
    return aretherebagels

@app.route('/')
def bagels():
    aretherebagels = openTmp()
    print(aretherebagels)
    if aretherebagels:
        return render_template('bagels.html')
    else:
        return render_template('nobagels.html')

if __name__ == '__main__':
    app.run(debug=True)
