import os
import sys
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# সাপোর্ট করা প্রধান রিজিওনসমূহের তালিকা
SUPPORTED_REGIONS = {
    'BD': 'Bangladesh',
    'IN': 'India',
    'SG': 'Singapore',
    'MY': 'Malaysia',
    'ID': 'Indonesia',
    'PK': 'Pakistan',
    'MA': 'Middle East (MENA)',
    'BR': 'Brazil',
    'TH': 'Thailand',
    'VN': 'Vietnam'
}

def check_player_info(target_id, requested_region=None):
    if requested_region:
        regions_to_test = [requested_region.upper()]
    else:
        regions_to_test = ['BD', 'IN', 'SG', 'MA', 'PK', 'BR']

    for r_code in regions_to_test:
        if r_code not in SUPPORTED_REGIONS:
            continue
            
        print(f"🔍 Testing region {r_code} ({SUPPORTED_REGIONS[r_code]}) for UID: {target_id}...", flush=True)
        
        cookies = {
            '_ga': 'GA1.1.2123120599.1674510784',
            '_fbp': 'fb.1.1674510785537.363500115',
            '_ga_7JZFJ14B0B': 'GS1.1.1674510784.1.1.1674510789.0.0.0',
            'source': 'mb',
            'region': r_code,
            'language': 'en' if r_code != 'MA' else 'ar',
            'datadome': '6h5F5cx_GpbuNtAkftMpDjsbLcL3op_5W5Z-npxeT_qcEe_7pvil2EuJ6l~JlYDxEALeyvKTz3~LyC1opQgdP~7~UDJ0jYcP5p20IQlT3aBEIKDYLH~cqdfXnnR6FAL0',
            'session_key': 'efwfzwesi9ui8drux4pmqix4cosane0y',
        }

        headers = {
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Origin': 'https://shop2game.com',
            'Referer': 'https://shop2game.com/app/100067/idlogin',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi Note 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
            'accept': 'application/json',
            'content-type': 'application/json',
            'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'x-datadome-clientid': '6h5F5cx_GpbuNtAkftMpDjsbLcL3op_5W5Z-npxeT_qcEe_7pvil2EuJ6l~JlYDxEALeyvKTz3~LyC1opQgdP~7~UDJ0jYcP5p20IQlT3aBEIKDYLH~cqdfXnnR6FAL0',
        }

        json_data = {
            'app_id': 100067,
            'login_id': target_id,
            'app_server_id': 0,
        }

        try:
            res = requests.post(
                'https://shop2game.com/api/auth/player_id_login', 
                cookies=cookies, 
                headers=headers, 
                json=json_data,
                timeout=8
            )

            if res.status_code == 200 and res.json().get('nickname'):
                player_data = res.json()
                nickname = player_data.get('nickname', 'N/A')
                print(f"✅ Player found in region {r_code}! Nickname: {nickname}", flush=True)
                
                return {
                    "nickname": nickname,
                    "region_code": r_code,
                    "region_name": SUPPORTED_REGIONS[r_code]
                }
                
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error during request for region {r_code}: {str(e)}", flush=True)
            if requested_region:
                return {"error": str(e)}

    return {"error": "ID NOT FOUND IN SUPPORTED REGIONS"}

@app.route('/', methods=['GET'])
def home_region_info():
    uid = request.args.get('uid')
    region = request.args.get('region')
    
    if not uid:
        return jsonify({"error": "UID parameter is required"}), 400

    result = check_player_info(uid, region)
    if "error" in result:
        return jsonify(result), 404

    return jsonify(result)

@app.route('/xp-opu', methods=['GET'])
def get_region_info():
    uid = request.args.get('uid')
    region = request.args.get('region')
    
    if not uid:
        return jsonify({"error": "UID parameter is required"}), 400

    result = check_player_info(uid, region)
    if "error" in result:
        return jsonify(result), 404

    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Initializing Flask application on port: {port}...", flush=True)
    app.run(host="0.0.0.0", port=port)
