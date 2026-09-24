from flask import Flask, render_template, redirect, url_for, session, request
from functools import wraps
import sheets

app = Flask(__name__)
app.secret_key = "rcm_depot_secure_app_key_2026"

# 1. Normal Login Check Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

# 2. Strict Admin Only Decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session.get('role') != 'admin':
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    # Agar user pehle se logged in hai toh uske role ke mutabiq sahi page par bhej dein
    if 'user' in session:
        role = session.get('role')
        if role == 'admin':
            return redirect(url_for('admin'))
        elif role == 'staff':
            return redirect(url_for('staff'))
        else:
            return redirect(url_for('depot'))
    return render_template('index.html')

# Standard Form Login Route
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    
    if not username:
        return redirect(url_for('home'))

    clean_user = str(username).strip()
    user_role = "depot"
    found = False

    try:
        # Google Sheet se verify karna
        sheet_response = sheets.get_depot_data("Users") # Agar worksheet ka naam kuch aur hai toh yahan badal lein
        if sheet_response.get("status") == "success":
            records = sheet_response.get("data", [])
            for row in records:
                sheet_username = str(row.get('username') or row.get('User') or '').strip()
                if sheet_username.lower() == clean_user.lower():
                    found = True
                    r = str(row.get('role') or row.get('Role') or '').strip().lower()
                    if r:
                        user_role = r
                    break
    except Exception as e:
        print("Sheet Error:", e)

    # Emergency Admin fallback
    if clean_user.lower() == 'admin':
        found = True
        user_role = 'admin'

    if found:
        session['user'] = clean_user
        session['role'] = user_role
        
        if user_role == 'admin':
            return redirect(url_for('admin'))
        elif user_role == 'staff':
            return redirect(url_for('staff'))
        else:
            return redirect(url_for('depot'))
    else:
        # Agar galat username ho toh wapas home par bhej dein
        return redirect(url_for('home'))

@app.route('/admin')
@admin_required
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
@admin_required
def audit():
    return render_template('audit.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
