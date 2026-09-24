from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sheets

app = Flask(__name__)
app.secret_key = "rcm_depot_secret_key"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        # Frontend se aane wale data ko handle karna
        data = request.get_json(silent=True) or request.form
        username = data.get('username')
        password = data.get('password')
        
        if username:
            session['user'] = str(username).strip()
            # Agar AJAX/JSON request hai toh JSON return karein, warna redirect
            if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"success": True})
            return redirect(url_for('depot'))
            
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"success": False, "message": "Invalid credentials"})
        return redirect(url_for('home'))
        
    except Exception as e:
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"success": False, "message": str(e)})
        return redirect(url_for('home'))

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/depot')
def depot():
    return render_template('depot.html')

@app.route('/staff')
def staff():
    return render_template('staff.html')

@app.route('/audit')
def audit():
    return render_template('audit.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
