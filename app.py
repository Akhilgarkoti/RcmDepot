from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sheets

app = Flask(__name__)
app.secret_key = "rcm_depot_secure_app_key_2026"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login_session():
    try:
        data = request.get_json(silent=True) or {}
        username = data.get('username')
        
        if username:
            clean_user = str(username).strip()
            session['user'] = clean_user
            
            user_role = 'depot' # Default role
            
            # 1. Aapke Admin Master sheet ke columns ke mutabiq direct check
            try:
                admin_response = sheets.get_depot_data("Admin Master")
                if admin_response.get("status") == "success":
                    records = admin_response.get("data", [])
                    for row in records:
                        # Sheet ke saare possible admin keys check kar rahe hain
                        admin_id = str(row.get('Admin Login ID') or row.get('Admin Name') or '').strip()
                        if admin_id.lower() == clean_user.lower():
                            user_role = 'admin'
                            break
            except Exception as e:
                print("Admin Sheet Error:", e)
            
            # 2. Hardcoded fallback taaki agar sheet fetch na ho toh bhi admin login na ruke
            if clean_user.lower() in ['akhil', 'adm001', 'admin']:
                user_role = 'admin'
            elif clean_user.lower().startswith('emp') or clean_user.lower().startswith('stf'):
                user_role = 'staff'
            
            session['role'] = user_role
            return jsonify({"success": True, "role": user_role})
            
        return jsonify({"success": False})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/admin')
def admin():
    if session.get('role') != 'admin':
        return redirect(url_for('home'))
    return render_template('admin.html')

@app.route('/depot')
def depot():
    if 'user' not in session or session.get('role') != 'depot':
        return redirect(url_for('home'))
    return render_template('depot.html')

@app.route('/staff')
def staff():
    if 'user' not in session or session.get('role') != 'staff':
        return redirect(url_for('home'))
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
