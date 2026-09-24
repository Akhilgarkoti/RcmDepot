from flask import Flask, render_template, request, session, redirect, url_for
# sheets.py से आपके प्रोजेक्ट के अपने फंक्शन्स इम्पोर्ट करें (जैसे कि आपकी पुरानी app.py में थे)
# आमतौर पर sheets.py में डेटा वेरिफाई करने के लिए फंक्शन्स होते हैं

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
    
    # यहाँ आपके प्रोजेक्ट के अनुसार लॉगिन जाँच होती है। 
    # यदि आप Google Sheet से रोल और पासवर्ड मैच करते हैं, तो उसका उपयोग करें।
    # उदाहरण के लिए, मान लेते हैं कि रोल 'admin', 'depot', या 'staff' मिलता है:
    
    # (यदि आपकी sheets.py में कोई ऐसा फंक्शन है, तो आप यहाँ कॉल कर सकते हैं, 
    # जैसे: user_role = verify_user_in_sheets(username, password))
    
    # सुरक्षा के लिए सत्र (session) सेट करें:
    if username:  # इसे अपने sheet validation के साथ बदलें
        session['logged_in'] = True
        session['username'] = username
        
        # अगर यूजरनेम में admin है या शीट से role 'admin' मिला है
        if 'admin' in username.lower():
            session['role'] = 'admin'
            return redirect(url_for('admin_page'))
        elif 'staff' in username.lower():
            session['role'] = 'staff'
            return redirect(url_for('staff_page'))
        else:
            session['role'] = 'depot'
            return redirect(url_for('depot_page'))
            
    return render_template('index.html', error="Invalid Login")

@app.route('/admin')
def admin_page():
    # सबसे महत्वपूर्ण सुरक्षा जाँच: केवल 'admin' ही देख सकता है
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
    session.clear()  # सत्र साaf करें ताकि कोई डेटा न बचे
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
