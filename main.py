##

from flask import *
import sqlite3

app = Flask(__name__, template_folder="frontend", static_folder="frontend")
app.config['SECRET_KEY'] = '123456789'

def get_db_connection():
    conn = sqlite3.connect('data/users.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_users_sorted_by_score():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return sorted(users, key = lambda d: d["high_score"], reverse=True)


def add_user(user: list):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (user[0],))
    data = cursor.fetchone()
    if data is None:
        conn.execute('INSERT INTO users (email, name_) VALUES (?, ?)',
                         tuple(user))
        conn.commit()
        cursor.execute("SELECT id FROM users WHERE email = ?", (user[0],))
        data = cursor.fetchone()
    session["id"] = data[0]
    conn.close()
    print(session["id"])


def set_score(score: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT high_score FROM users WHERE id = ?", (session["id"],))
    last_score = cursor.fetchone()[0]
    if int(last_score) < score:
        conn.execute('UPDATE users SET high_score = ?'
                         ' WHERE id = ?',
                         (score, session["id"]))
    conn.commit()
    conn.close()


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/lb", methods=["post", "get"])
def leaderboard():
    #sorted(list_to_be_sorted, key=lambda d: d['name']) 
    return render_template("leaderboard.html", users=get_users_sorted_by_score()[:10], devs=["robertproducts", "MixVKusa", "TasFoster", "VladPopush"])


@app.route("/auth", methods=["post", "get"])
def auth():
    if request.method == "GET":
        return render_template("auth.html")
    else:
        email = request.form.get("email")
        name = request.form.get("name")
        
        add_user([email, name])
        print(session.get("id"))
        return redirect("/game")


@app.route("/game")
def game():
    return render_template("game.html")


if __name__ == "__main__":
    app.run(debug=True)