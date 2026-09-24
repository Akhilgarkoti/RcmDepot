from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from functools import wraps

app = Flask(__name__)
app.secret_key = "rcm_depot_secure_app_key"

# सामान्य लॉगिन चेक
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

# केवल Admin के लिए सुरक्षा चेक
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session.get('role') != 'admin':
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    # अगर यूजर पहले से लॉग इन है, तो उसे उसके रोल के अनुसार सही पेज पर भेजें
    if 'user' in session:
        role = session.get('role')
        if role == 'admin':
            return redirect(url_for('admin'))
        elif role == 'staff':
            return redirect(url_for('staff'))
        else:
            return redirect(url_for('depot'))
    return render_template('index.html')

# Frontend से लॉगिन होने के बाद यूजर और उसका रोल सेट करें
@app.route('/login', methods=['POST'])
def login_session():
    try:
        data = request.get_json(silent=True) or {}
        user_code = data.get('username')
        
        if user_code:
            clean_user = str(user_code).strip()
            session['user'] = clean_user
            
            # यहाँ तय करें कि यूजर का रोल क्या है (आप इसे अपनी शीट या डेटाबेस से भी मिला सकते हैं)
            if clean_user.lower() == 'admin' or 'admin' in clean_user.lower():
                session['role'] = 'admin'
            elif 'staff' in clean_user.lower():
                session['role'] = 'staff'
            else:
                session['role'] = 'depot'
                
            return jsonify({"success": True})
        return jsonify({"success": False})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

# Admin पेज - यहाँ सिर्फ Admin ही आ सकता है
@app.route('/admin')
@admin_required
def admin():
    return render_template('admin.html')

# Depot पेज - यहाँ Login यूजर आ सकता है
@app.route('/depot')
@login_required
def depot():
    # अगर कोई एडमिन डिपो पेज खोलना चाहे तो रोक भी सकते हैं या अनुमति दे सकते हैं
    return render_template('depot.html')

# Staff पेज - यहाँ Login यूजर आ सकता है
@app.route('/staff')
@login_required
def staff():
    return render_template('staff.html')

# Audit पेज - केवल Admin के लिए
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
