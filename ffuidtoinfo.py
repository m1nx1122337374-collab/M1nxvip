import os
import sys
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# থার্ড-পার্টি ওয়ার্কিং এপিআই
EXTERNAL_API = "https://jexarcodexplayer.vercel.app/ffinfo"

# অটো-ডিটেক্ট করার জন্য রিজিওনের প্রাইওরিটি লিস্ট (BD এবং IND প্রথমে রাখা হয়েছে)
REGIONS_TO_TRY = ['BD', 'IND', 'SG', 'BR', 'US', 'PK', 'ID', 'TH']

def fetch_player_auto(uid, requested_region=None):
    # ইউজার যদি ম্যানুয়ালি রিজিওন দিয়ে দেয় তবে শুধু সেটাই ট্রাই করবে
    if requested_region:
        testing_regions = [requested_region.upper()]
    else:
        # রিজিওন না দিলে অটোমেটিক লুপ চালিয়ে খুজে বের করবে
        testing_regions = REGIONS_TO_TRY

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    for region in testing_regions:
        params = {
            'uid': uid,
            'region': region
        }

        try:
            response = requests.get(EXTERNAL_API, params=params, headers=headers, timeout=8)
            
            if response.status_code == 200:
                data = response.json()
                
                # সফলভাবে প্লেয়ারের তথ্য পাওয়া গেলে সাথে সাথে রেসপন্স রিটার্ন করবে
                if data.get("status") == "success" and "account" in data:
                    account = data.get("account", {})
                    
                    return {
                        "status": "success",
                        "nickname": account.get("name", "N/A"),
                        "uid": account.get("uid", uid),
                        "detected_region": region,
                        "level": account.get("level", "N/A"),
                        "exp": account.get("exp", "N/A"),
                        "likes": account.get("likes", "N/A"),
                        "br_rank": account.get("br_rank", "N/A"),
                        "cs_rank": account.get("cs_rank", "N/A"),
                        "account_created": account.get("account_created", "N/A"),
                        "last_login": account.get("last_login", "N/A"),
                        "bio": account.get("bio", "N/A"),
                        "guild": data.get("guild", {}),
                        "raw_data": data
                    }, 200

        except requests.exceptions.RequestException:
            continue # কোনো রিজিওনে টাইমআউট বা এরর আসলে পরের রিজিওন চেক করবে

    return {"error": "Player UID not found in any supported region"}, 404

@app.route('/', methods=['GET'])
def home_region_info():
    uid = request.args.get('uid')
    region = request.args.get('region')
    
    if not uid:
        return jsonify({"error": "UID parameter is required"}), 400

    result, status_code = fetch_player_auto(uid, region)
    return jsonify(result), status_code

@app.route('/xp-opu', methods=['GET'])
def get_region_info():
    uid = request.args.get('uid')
    region = request.args.get('region')
    
    if not uid:
        return jsonify({"error": "UID parameter is required"}), 400

    result, status_code = fetch_player_auto(uid, region)
    return jsonify(result), status_code

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
