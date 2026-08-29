from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)
app.secret_key = "rcm_depot_secure_app_key"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/depot')
def depot():
    return render_template('depot.html')

@app.route('/staff')
def staff():
    return render_template('staff.html')

@app.route('/logout')
def logout():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
