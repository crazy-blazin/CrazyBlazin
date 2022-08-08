from flask import Flask, render_template, request
import threading
app = Flask(__name__)



# import qrcode

# img = qrcode.make("http://192.168.1.234:5000/someid")
# type(img)  # qrcode.image.pil.PilImage
# img.save("some_file.png")


@app.route("/")
def home():

    return "What are you doing here?"


@app.route("/<id>")
def hello_world(id):
    with open('whatwehave.txt', 'r') as f:
        database = eval(f.read())
    if id in database:
        name = database[id]
        return render_template("index.html", name=name, id=id)
    else:
        return render_template("nolonger.html")


@app.route("/thanks")
def thanks():
    return "Thanks for using our service"


@app.route("/oilchange", methods=["POST"])
def oilchange():
    oilvalue = str(request.form["oil"]).split(" ")[-1]
    name = request.form["name"]
    
    with open('whatwehave.txt', 'r') as f:
        database = eval(f.read())
    
    oilvalue = int(oilvalue)
    if oilvalue <= 0 or oilvalue > 5:
        return "Nice try hacker man.. :("
    for id in database:
        if name == database[id]:
            database.pop(id)
            with open('whatwehave.txt', 'w') as f:
                f.write(str(database))
                
            with open('users.txt', 'r') as f:
                users = eval(f.read())
                users[name] = oilvalue
            with open('users.txt', 'w') as f:
                f.write(str(users))
                return f"Oil diversion changed to {oilvalue}"
    return "Could not find user"


if __name__ == "__main__":
    app.run("0.0.0.0", 2000)
