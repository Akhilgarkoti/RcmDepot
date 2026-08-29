from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = "rcm_depot_secure_live_key"

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz1cdsjmQpRCr33ruM-6XLHfkkLoqA_mpV6CZ1hcQITB2LemAXGtuV0aqcHxpRRc7xc-A/exec"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    role = data.get('role')
    username = data.get('username')
    password = data.get('password')

    try:
        session_req = requests.Session()
        res = session_req.get(
            GOOGLE_SCRIPT_URL,
            params={"action": "login", "role": role, "username": username, "password": password},
            allow_redirects=True,
            timeout=20
        )
        
        result = res.json()
        if result.get("success"):
            session['user'] = result.get('username')
            session['role'] = role
            session['name'] = result.get('name')
            return jsonify({"success": True, "redirect": f"/{role}"})
        else:
            return jsonify({"success": False, "message": result.get("message", "Invalid credentials")}), 401
    except Exception as e:
        return jsonify({"success": False, "message": "Connection error: " + str(e)}), 500

@app.route('/api/data', methods=['GET'])
def get_sheet_data():
    sheet_name = request.args.get('sheet', 'Depot Master')
    try:
        session_req = requests.Session()
        res = session_req.get(
            GOOGLE_SCRIPT_URL,
            params={"action": "getData", "sheet": sheet_name},
            allow_redirects=True,
            timeout=20
        )
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/depot')
def depot():
    return render_template('admin.html')

@app.route('/staff')
def staff():
    return render_template('admin.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
