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
        data = request.get_json(silent=True) or request.form
        username = data.get('username')
        password = data.get('password')
        
        if username:
            clean_user = str(username).strip()
            session['user'] = clean_user
            
            # Yahan check kar rahe hain ki user admin hai ya depot user
            if clean_user.lower() == 'admin' or 'admin' in clean_user.lower():
                session['role'] = 'admin'
            else:
                session['role'] = 'depot'
            
            if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"success": True, "role": session['role']})
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
    # Security Check: Agar session mein role 'admin' nahi hai, toh admin page nahi khulega!
    if session.get('role') != 'admin':
        return redirect(url_for('home'))
    return render_template('admin.html')

@app.route('/depot')
def depot():
    # Security Check: Bina login ke depot page bhi nahi khulega
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template('depot.html')

@app.route('/staff')
def staff():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template('staff.html')

@app.route('/audit')
def audit():
    # Security Check: Sirf admin ke liye
    if session.get('role') != 'admin':
        return redirect(url_for('home'))
    return render_template('audit.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
