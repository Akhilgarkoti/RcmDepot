from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from functools import wraps
import sheets  # Aapki sheets.py file ka use karne ke liye

app = Flask(__name__)
app.secret_key = "rcm_depot_secure_app_key"

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

# Google Sheet se login verify karne wala route
@app.route('/login', methods=['POST'])
def login_session():
    try:
        data = request.get_json(silent=True) or {}
        user_code = data.get('username')
        
        if not user_code:
            return jsonify({"success": False, "message": "Username missing"})

        clean_user = str(user_code).strip()
        
        # Google Sheet se data fetch karein (Yahan apni worksheet ka naam dein, jaise 'Users' ya 'Login')
        sheet_response = sheets.get_depot_data("Users") # Agar worksheet ka naam kuch aur hai toh yahan badal lein
        
        found = False
        user_role = "depot" # Default role depot rahega

        if sheet_response.get("status") == "success":
            records = sheet_response.get("data", [])
            for row in records:
                # Sheet ke column name ke hisaab se check karein (jaise 'username' ya 'User')
                sheet_username = str(row.get('username') or row.get('User') or '').strip()
                
                if sheet_username.lower() == clean_user.lower():
                    found = True
                    # Agar sheet mein role ka column diya hua hai, toh wahan se role utha lein
                    r = str(row.get('role') or row.get('Role') or '').strip().lower()
                    if r:
                        user_role = r
                    break
        
        # Emergency ya default Admin check (agar sheet mein admin set na ho)
        if clean_user.lower() == 'admin':
            found = True
            user_role = 'admin'

        if found:
            session['user'] = clean_user
            session['role'] = user_role
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "Invalid Username"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

# Admin Page - Sirf Admin ke liye secure
@app.route('/admin')
@admin_required
def admin():
    return render_template('admin.html')

# Depot Page - Logged in users ke liye
@app.route('/depot')
@login_required
def depot():
    return render_template('depot.html')

# Staff Page - Logged in users ke liye
@app.route('/staff')
@login_required
def staff():
    return render_template('staff.html')

# Audit Page - Sirf Admin ke liye secure
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
