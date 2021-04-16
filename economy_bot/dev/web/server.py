from flask import Flask, render_template
app = Flask(__name__)





class Database:
    def __init__(self):
        self.dbName = 'crazy_blazin_database.txt' 
    def read(self):
        with open(self.dbName, 'r') as f:
            return eval(f.read())

    def write(self, users):
        with open(self.dbName, 'w') as f:
            f.write(str(users))



@app.route("/")
def front():
   return render_template('frontpage.html', my_list=range(10))  # make a list and pass it to our template variable named my_list



if __name__ == "__main__":
    app.run(debug=True)