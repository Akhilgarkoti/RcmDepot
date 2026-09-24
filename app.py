from flask import Flask, render_template, request, session, redirect, url_for
import sheets  # आपके द्वारा दी गई sheets.py फ़ाइल

app = Flask(__name__)
# Vercel पर सत्र (sessions) सुरक्षित रखने के लिए secret_key ज़रूरी है
app.secret_key = 'rcm_depot_secure_session_key_vercel'

@app.route('/')
def index():
    # अगर यूजर पहले से लॉग इन है, तो उसे उसके रोल के अनुसार सही पेज पर भेजें
    if session.get('logged_in'):
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
    
    if not username or not password:
        return render_template('index.html', error="कृपया यूजरनेम और पासवर्ड दर्ज करें।")
    
    # 1. पहले एडमिन या स्पेशल यूजर के लिए डायरेक्ट चेक (यदि आप रखना चाहें)
    if username.strip().lower() == 'admin' and password == 'admin123': # अपनी जरूरत के मुताबिक एडमिन पासवर्ड सेट करें
        session['logged_in'] = True
        session['username'] = username
        session['role'] = 'admin'
        return redirect(url_for('admin_page'))

    # 2. Google Sheet से डेटा फेच करके लॉगिन वेरीफाई करना
    # मान लीजिए आपकी शीट में "Users" या "Depot" नाम की worksheet है जहाँ यूजरनेम/पासवर्ड सेव हैं
    sheet_response = sheets.get_depot_data("Users") # अपनी सही Worksheet का नाम यहाँ लिखें (जैसे 'Login', 'Users' आदि)
    
    if sheet_response.get("status") == "success":
        users_data = sheet_response.get("data", [])
        
        for user in users_data:
            # मान लेते हैं शीट में कॉलम के नाम 'username', 'password', और 'role' हैं
            if str(user.get('username')).strip() == username.strip() and str(user.get('password')).strip() == password.strip():
                session['logged_in'] = True
                session['username'] = username
                user_role = str(user.get('role', 'depot')).strip().lower()
                session['role'] = user_role
                
                if user_role == 'admin':
                    return redirect(url_for('admin_page'))
                elif user_role == 'staff':
                    return redirect(url_for('staff_page'))
                else:
                    return redirect(url_for('depot_page'))
                    
    # अगर लॉगिन फेल हो जाता है
    return render_template('index.html', error="गलत यूजरनेम या पासवर्ड!")

@app.route('/admin')
def admin_page():
    # सुरक्षा जाँच: केवल 'admin' ही देख सकता है
    if not session.get('logged_in') or session.get('role') != 'admin':
        return redirect(url_for('index'))
    return render_template('admin.html')

@app.route('/depot')
def depot_page():
    # सुरक्षा जाँच: 'admin' या 'depot' वाले ही देख सकते हैं
    if not session.get('logged_in') or session.get('role') not in ['admin', 'depot']:
        return redirect(url_for('index'))
    return render_template('depot.html')

@app.route('/staff')
def staff_page():
    # सुरक्षा जाँच: 'admin' या 'staff' वाले ही देख सकते हैं
    if not session.get('logged_in') or session.get('role') not in ['admin', 'staff']:
        return redirect(url_for('index'))
    return render_template('staff.html')

@app.route('/audit')
def audit_page():
    # केवल एडमिन के लिए
    if not session.get('logged_in') or session.get('role') != 'admin':
        return redirect(url_for('index'))
    return render_template('audit.html')

@app.route('/logout')
def logout():
    session.clear()  # सत्र साफ़ करें ताकि डेटा सुरक्षित रहे
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
