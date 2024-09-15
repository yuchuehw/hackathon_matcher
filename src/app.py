from flask import Flask, request, render_template, redirect, url_for, session, abort
from database import init_db, get_db, add_user, find_matches, username_exists, add_answer
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

@app.route('/')
def index():
    current_user = session.get('username')
    return render_template('index.html', current_user=current_user)

@app.route('/login')
def login():
    return redirect(url_for('register'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        hackathon = request.form.getlist('hackathon')
        technology_known = request.form.getlist('technologies_known')
        technology_learning = request.form.getlist('technologies_learning')
        question = request.form['question']

        db = get_db()

        # Check if username already exists
        if username_exists(db, username):
            return render_template('register.html', error="Username is already taken.")

        add_user(db, username, hackathon, technology_known, technology_learning,
                 question, "", "")
        session['username'] = username  # Store the current user in the session
        return redirect(url_for('profile', username=username))

    return render_template('register.html')

@app.route('/profile/<username>')
def profile(username):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

    if user is None:
        abort(404, description="User not found")

    return render_template('profile.html', user=user)

@app.route('/matches/<username>')
def matches(username):
    if not session.get('quizz'):
        return redirect(url_for("quizz"))
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

    if user is None:
        return render_template('error.html', message="User not found or not registered.")

    matches = find_matches(db, user['technology2'])
    return render_template('match.html', user=user, matches=matches)

@app.route('/quizz',methods=['GET', 'POST'])
@app.route('/quizz/<uid>', methods=['GET', 'POST'])
def quizz(uid=None):
    db = get_db()
    if uid is None:
        uid = random.randint(1,db.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1").fetchall()[0][0])
    user = db.execute('SELECT * FROM users WHERE id = ?', (uid,)).fetchone()
    if not user:
        return redirect(url_for('quizz'))
    if request.method == "POST":
        if 'username' not in session or session['username'] is None:
            return render_template("quizz.html",user=uid,error="please log in/register first")
        else:
            session['quizz'] = 1
            answer = request.form.get('answer')
            userid = user[0]
            add_answer(db,userid,uid,answer)
        return redirect(url_for('matches',username=session['username']))
    return render_template('quizz.html',user=user)

@app.route('/request')
def request():
    return render_template('request.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', message="Page not found."), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
