from flask import Flask, render_template, url_for
app = Flask(__name__)





class Database:
    def __init__(self):
        self.dbName = '../crazy_blazin_database.txt' 
    def read(self):
        with open(self.dbName, 'r') as f:
            return eval(f.read())

    def write(self, users):
        with open(self.dbName, 'w') as f:
            f.write(str(users))


db = Database()


@app.route("/")
def front():
    users = db.read()
    temp_dict = {}
    for user in users:
        temp_dict[user] = users[user]['Coins']
        # print(users[user]['Coins'])
    sorted_users = sorted(temp_dict.items(),  key=lambda x: x[1], reverse=True)

    for user in users:
        if 'Timer' not in users[user]:
            users[user]['Timer'] = 0
    #users -> key, users[key] -> {'Coins' : 499, .....}

    return render_template('frontpage.html', users = sorted_users, users_all = users)  # make a list and pass it to our template variable named my_list


@app.route("/commands")
def coms():
    
    return render_template('commands.html')  # make a list and pass it to our template variable named my_list


if __name__ == "__main__":
    app.run(debug=True)