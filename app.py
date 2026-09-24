from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sheets

app = Flask(__name__)
app.secret_key = "rcm_depot_secure_app_key_2026"

@app.route('/')
def home():
    # Agar user pehle se logged in hai, toh use seedha uske sahi page par bhej dein
    if 'user' in session:
        role = session.get('role', 'depot')
        if role == 'admin':
            return redirect(url_for('admin'))
        elif role == 'staff':
            return redirect(url_for('staff'))
        else:
            return redirect(url_for('depot'))
    return render_template('index.html')

# Frontend JavaScript se aane wali session request ko handle karne ke liye
@app.route('/login', methods=['POST'])
def login_session():
    try:
        data = request.get_json(silent=True) or {}
        username = data.get('username')
        
        if username:
            clean_user = str(username).strip()
            session['user'] = clean_user
            
            # Role decide karna jo frontend se match kare
            lower_user = clean_user.lower()
            if 'admin' in lower_user:
                session['role'] = 'admin'
            elif lower_user.startswith('emp') or lower_user.startswith('stf'):
                session['role'] = 'staff'
            else:
                session['role'] = 'depot'
                
            return jsonify({"success": True})
        return jsonify({"success": False})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/admin')
def admin():
    # Strict Security: Sirf aur sirf 'admin' role wale hi admin khol sakte hain, URL change karne par block ho jayega
    if session.get('role') != 'admin':
        return redirect(url_for('home'))
    return render_template('admin.html')

@app.route('/depot')
def depot():
    # Strict Security: Bina login ke ya agar staff/admin URL se aaye toh depot block ho jayega
    if 'user' not in session or session.get('role') != 'depot':
        return redirect(url_for('home'))
    return render_template('depot.html')

@app.route('/staff')
def staff():
    # Strict Security: Sirf staff role wale hi access kar sakte hain
    if 'user' not in session or session.get('role') != 'staff':
        return redirect(url_for('home'))
    return render_template('staff.html')

@app.route('/audit')
def audit():
    # Jaisa aapne kaha tha, audit bina login ke khul sakta hai
    return render_template('audit.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
