from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sheets

app = Flask(__name__)
app.secret_key = "rcm_depot_secure_app_key_2026"

@app.route('/')
def home():
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
            
            user_role = 'depot' # Default role
            
            # 1. Google Sheet ke "Admin Master" se check karna ki kya ye admin hai[cite: 3]
            try:
                admin_response = sheets.get_depot_data("Admin Master")
                if admin_response.get("status") == "success":
                    records = admin_response.get("data", [])
                    for row in records:
                        admin_id = str(row.get('Admin Login ID') or row.get('Admin Login') or '').strip()
                        if admin_id.lower() == clean_user.lower():
                            user_role = 'admin'
                            break
            except Exception as e:
                print("Admin Sheet Error:", e)
            
            # 2. Agar sheet mein nahi mila, toh fallback logic check karein
            lower_user = clean_user.lower()
            if user_role != 'admin':
                if 'admin' in lower_user:
                    user_role = 'admin'
                elif lower_user.startswith('emp') or lower_user.startswith('stf'):
                    user_role = 'staff'
                else:
                    user_role = 'depot'
            
            session['role'] = user_role
            return jsonify({"success": True, "role": user_role})
            
        return jsonify({"success": False})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/admin')
def admin():
    # Strict Security: Sirf aur sirf 'admin' role wale hi admin khol sakte hain[cite: 1]
    if session.get('role') != 'admin':
        return redirect(url_for('home'))
    return render_template('admin.html')

@app.route('/depot')
def depot():
    # Strict Security: Bina login ke ya galat role hone par home par bhej dega[cite: 1]
    if 'user' not in session or session.get('role') != 'depot':
        return redirect(url_for('home'))
    return render_template('depot.html')

@app.route('/staff')
def staff():
    # Strict Security: Sirf staff role wale hi access kar sakte hain[cite: 1]
    if 'user' not in session or session.get('role') != 'staff':
        return redirect(url_for('home'))
    return render_template('staff.html')

@app.route('/audit')
def audit():
    # Audit bina login ke khul sakta hai
    return render_template('audit.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
