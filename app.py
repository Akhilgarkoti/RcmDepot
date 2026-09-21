from flask import Flask, render_template, redirect, url_for, session
from functools import wraps

app = Flask(__name__)
app.secret_key = "rcm_depot_secure_app_key"

# सुरक्षा के लिए डेकोरेटर (Login Protection Decorator)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # चेक करता है कि सेशन में यूजर लॉग्ड-इन है या नहीं
        if 'user' not in session:
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('index.html')

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
    session.clear()  # लॉगआउट होने पर सर्वर से पूरा सेशन साफ़ हो जाएगा
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
