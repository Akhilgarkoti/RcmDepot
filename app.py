from flask import Flask, render_template, request, session, redirect, url_for
from sheets import get_user_role_from_sheet # Assuming sheets.py mein role verify karne ka function hai

app = Flask(__name__)
# Vercel ya production ke liye ek secure secret key zaroori hai sessions ke liye
app.secret_key = 'rcm_depot_secure_random_secret_key_2026'

@app.route('/')
def index():
    # Agar user pehle se logged in hai toh uske role ke hisaab se redirect karein
    if 'logged_in' in session:
        role = session.get('role')
        if role == 'admin':
            return redirect(url_for('admin_page'))
        elif role == 'depot':
            return redirect(url_for('depot_page'))
        elif role == 'staff':
            return redirect(url_for('staff_page'))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Google Sheet ya database se user ka role check karein
    # Yeh function aapke sheets.py ke logic ke anusaar kaam karega
    user_role = get_user_role_from_sheet(username, password)
    
    if user_role:
        session['logged_in'] = True
        session['username'] = username
        session['role'] = user_role  # Role: 'admin', 'depot', ya 'staff'
        
        if user_role == 'admin':
            return redirect(url_for('admin_page'))
        elif user_role == 'depot':
            return redirect(url_for('depot_page'))
        elif user_role == 'staff':
            return redirect(url_for('staff_page'))
    
    return render_template('index.html', error="Invalid username or password")

@app.route('/admin')
def admin_page():
    # Security Check: Kewal 'admin' role wale hi access kar sakte hain
    if not session.get('logged_in') or session.get('role') != 'admin':
        return redirect(url_for('index'))
    return render_template('admin.html')

@app.route('/depot')
def depot_page():
    # Security Check: 'admin' ya 'depot' role wale access kar sakte hain
    if not session.get('logged_in') or session.get('role') not in ['admin', 'depot']:
        return redirect(url_for('index'))
    return render_template('depot.html')

@app.route('/staff')
def staff_page():
    # Security Check: 'admin' ya 'staff' role wale access kar sakte hain
    if not session.get('logged_in') or session.get('role') not in ['admin', 'staff']:
        return redirect(url_for('index'))
    return render_template('staff.html')

@app.route('/audit')
def audit_page():
    # Security Check: Kewal admin ke liye audit page
    if not session.get('logged_in') or session.get('role') != 'admin':
        return redirect(url_for('index'))
    return render_template('audit.html')

@app.route('/logout')
def logout():
    session.clear()  # Session clear karke logout kar dein
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
