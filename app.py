from flask import Flask, jsonify

app = Flask(__name__)

# बेसिक टेस्ट रूट
@app.route('/')
def home():
    return jsonify({
        "status": "success",
        "message": "RCM Depot System Backend Running Successfully!"
    })

if __name__ == '__main__':
    app.run(debug=True)
