from flask import Flask, jsonify, request
from flask_cors import CORS
from SmartApi import SmartConnect
import pyotp

app = Flask(__name__)
CORS(app)  # Browser/App se CORS restrictions hatane ke liye

@app.route('/api/login', methods=['POST'])
def angel_login():
    data = request.json
    api_key = data.get('apiKey')
    client_code = data.get('clientCode')
    password = data.get('password') # MPIN
    totp_secret = data.get('totpSecret')

    if not all([api_key, client_code, password, totp_secret]):
        return jsonify({'status': False, 'message': 'Missing Credentials'}), 400

    try:
        # SmartAPI Session Generation
        smart_api = SmartConnect(api_key=api_key)
        totp = pyotp.TOTP(totp_secret).now()
        session_data = smart_api.generateSession(client_code, password, totp)
        
        if not session_data.get('status'):
            return jsonify({'status': False, 'message': session_data.get('message')}), 401

        return jsonify({
            'status': True,
            'message': 'Successfully connected to Angel One',
            'jwtToken': session_data['data']['jwtToken'],
            'feedToken': session_data['data']['feedToken']
        })

    except Exception as e:
        return jsonify({'status': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
