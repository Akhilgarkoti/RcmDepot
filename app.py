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
        
        if username:
            clean_user = str(username).strip()
            session['user'] = clean_user
            
            # Yahan apne admin ya staff ka exact username set karein
            # Jaise agar aapka admin username 'admin' ya kuch aur hai:
            if clean_user.lower() == 'admin':  # Apne admin ID yahan match karein
                session['role'] = 'admin'
            elif 'staff' in clean_user.lower():  # Agar staff id me 'staff' aata hai
                session['role'] = 'staff'
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
    # Sirf aur sirf Admin hi access kar sakta hai
    if session.get('role') != 'admin':
        return redirect(url_for('home'))
    return render_template('admin.html')

@app.route('/depot')
def depot():
    # Bina login ke depot nahi khulega, aur agar role match nahi hai toh block
    if 'user' not in session or session.get('role') == 'staff':
        return redirect(url_for('home'))
    return render_template('depot.html')

@app.route('/staff')
def staff():
    # Sirf Staff ya Admin hi staff page dekh sakta hai
    if 'user' not in session or session.get('role') not in ['staff', 'admin']:
        return redirect(url_for('home'))
    return render_template('staff.html')

@app.route('/audit')
def audit():
    # Audit bina login ke khul sakta hai (jaisa aapne bataya tha)
    return render_template('audit.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
