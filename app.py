from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from functools import wraps

app = Flask(__name__)
app.secret_key = "rcm_depot_secure_app_key"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('index.html')

# Yahan apna login validate karne ka route banayein (Jaise aapne pehle Google Apps Script ya DB se connect kiya ho)
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    user_code = data.get('username')
    # Yahan password/user check karne ke baad agar details sahi hain toh:
    session['user'] = user_code  # Yeh session set karna bahut zaroori hai
    return jsonify({"success": True})

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/depot')
@login_required
def depot():
    return render_template('depot.html')

@app.route('/staff')
@login_required
def staff():
    return render_template('staff.html')

@app.route('/audit')
@login_required
def audit():
    return render_template('audit.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
