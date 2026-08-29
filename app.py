from flask import Flask, render_template, request, jsonify
from sheets import get_depot_data

app = Flask(__name__)

# लॉगिन / होम पेज
@app.route('/')
def home():
    return render_template('index.html')

# एडमिन डैशबोर्ड
@app.route('/admin')
def admin():
    return render_template('admin.html')

# डिपो डैशबोर्ड
@app.route('/depot')
def depot():
    return render_template('admin.html')  # अभी के लिए एडमिन व्यू रेंडर करेगा

# स्टाफ डैशबोर्ड
@app.route('/staff')
def staff():
    return render_template('admin.html')

# Google Sheets से डेटा फेच करने का API रूट
@app.route('/api/depot-data', methods=['GET'])
def fetch_data():
    sheet_name = request.args.get('sheet', 'Sheet1')
    result = get_depot_data(sheet_name)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
