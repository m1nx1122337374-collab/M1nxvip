import os
import sys
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

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
        
        # ফ্রেশ এবং ডায়নামিক হেডারের ব্যবস্থা
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Origin': 'https://shop2game.com',
            'Referer': f'https://shop2game.com/app/100067/idlogin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'content-type': 'application/json',
        }

        json_data = {
            'app_id': 100067,
            'login_id': target_id,
            'app_server_id': 0,
        }

        try:
            # কুকিজের ঝামেলা এড়াতে সেশন রিকোয়েস্ট ব্যবহার করা ভালো
            session = requests.Session()
            res = session.post(
                'https://shop2game.com/api/auth/player_id_login', 
                headers=headers, 
                json=json_data,
                timeout=10
            )

            print(f"Response Code: {res.status_code}, Body: {res.text}", flush=True)

            if res.status_code == 200:
                data = res.json()
                if data.get('nickname'):
                    nickname = data.get('nickname', 'N/A')
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
    app.run(host="0.0.0.0", port=port)
