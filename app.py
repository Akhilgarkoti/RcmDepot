from flask import Flask, render_template, request, session, redirect, url_for
import sheets  # आपके प्रोजेक्ट की sheets.py फाइल का उपयोग

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
    # जैसा आपके ओरिजिनल प्रोजेक्ट में फॉर्म से डेटा लिया जाता है
    username = request.form.get('username')
    password = request.form.get('password')
    
    # यहाँ हम sheets.py या आपके तय किए गए लॉजिक से यूजर को वेरीफाई करेंगे
    # (आप चाहें तो अपनी पुरानी app.py का लॉगिन वाला हिस्सा यहाँ रख सकते हैं)
    
    # उदाहरण के लिए सुरक्षा जाँच:
    if username:
        session['logged_in'] = True
        session['username'] = username
        
        # तय करें कि यूजर एडमिन है या डिपो स्टाफ
        if username.lower() == 'admin' or 'admin' in username.lower():
            session['role'] = 'admin'
            return redirect(url_for('admin_page'))
        elif 'staff' in username.lower():
            session['role'] = 'staff'
            return redirect(url_for('staff_page'))
        else:
            session['role'] = 'depot'
            return redirect(url_for('depot_page'))
            
    return render_template('index.html', error="Invalid Credentials")

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
