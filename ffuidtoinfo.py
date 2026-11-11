import os
import sys
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# External working API endpoint
EXTERNAL_API = "https://jexarcodexplayer.vercel.app/ffinfo"
REGIONS_TO_TRY = ['BD', 'IND', 'SG', 'BR', 'US', 'PK', 'ID', 'TH']

def fetch_player_auto(uid, requested_region=None):
    if requested_region:
        testing_regions = [requested_region.upper()]
    else:
        testing_regions = REGIONS_TO_TRY

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    for region in testing_regions:
        params = {'uid': uid, 'region': region}
        try:
            response = requests.get(EXTERNAL_API, params=params, headers=headers, timeout=8)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success" and "account" in data:
                    account = data.get("account", {})
                    return {
                        "status": "success",
                        "brand": "M1NX VIP",
                        "developer": "M1NX GAMING VIP",
                        "telegram": "@M1NXGAMINGVIP",
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
                        "pet": data.get("pet", {}),
                        "credit": "Powered by M1NX VIP & Co."
                    }, 200
        except requests.exceptions.RequestException:
            continue

    return {"error": "Player UID not found in any supported region", "developer": "M1NX GAMING VIP"}, 404


# ====================== PREMIUM HOME PAGE (SVG ICONS ONLY) ======================
HOME_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>M1NX VIP - Free Fire UID Info API</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%230ea5e9' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M3 7l4 5 5-8 5 8 4-5v11H3z'/></svg>">
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: radial-gradient(circle at 20% 20%, #1e1b4b 0%, #0f172a 40%, #020617 100%);
        color: #f8fafc; min-height: 100vh; padding: 16px; line-height: 1.6;
        overflow-x: hidden;
    }
    body::before {
        content: ''; position: fixed; inset: 0;
        background-image:
            radial-gradient(2px 2px at 20% 30%, #38bdf8, transparent),
            radial-gradient(2px 2px at 60% 70%, #a78bfa, transparent),
            radial-gradient(1px 1px at 50% 50%, #f472b6, transparent),
            radial-gradient(2px 2px at 80% 10%, #38bdf8, transparent),
            radial-gradient(1px 1px at 90% 80%, #a78bfa, transparent);
        background-repeat: repeat; background-size: 300px 300px;
        opacity: 0.35; z-index: 0; pointer-events: none;
        animation: twinkle 6s ease-in-out infinite alternate;
    }
    @keyframes twinkle { from { opacity: 0.25; } to { opacity: 0.5; } }

    /* ========= SVG ICON SYSTEM ========= */
    .ico {
        width: 16px; height: 16px;
        stroke: currentColor; fill: none;
        stroke-width: 2; stroke-linecap: round; stroke-linejoin: round;
        display: inline-block; vertical-align: middle; flex-shrink: 0;
    }
    .ico-sm { width: 14px; height: 14px; }
    .ico-lg { width: 20px; height: 20px; }
    .ico-xl { width: 26px; height: 26px; }

    .container {
        max-width: 860px; margin: 0 auto; position: relative; z-index: 1;
        background: rgba(30, 41, 59, 0.75);
        backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 22px; padding: 26px 20px 30px;
        box-shadow: 0 25px 60px rgba(0,0,0,0.6), 0 0 40px rgba(56,189,248,0.08);
        animation: floatIn 0.6s cubic-bezier(.2,.8,.2,1);
    }
    @keyframes floatIn { from { opacity: 0; transform: translateY(24px); } to { opacity: 1; transform: none; } }

    .hero { text-align: center; margin-bottom: 22px; }
    .logo-badge {
        display: inline-flex; align-items: center; gap: 8px;
        background: linear-gradient(135deg, #0ea5e9, #6366f1, #a855f7);
        padding: 8px 16px; border-radius: 999px; font-size: 13px;
        font-weight: 700; letter-spacing: 0.5px; color: white;
        box-shadow: 0 6px 20px rgba(99,102,241,0.45);
        animation: pulse 2.5s ease-in-out infinite;
    }
    .logo-badge .ico { stroke: #fde047; filter: drop-shadow(0 0 6px rgba(253,224,71,0.6)); }
    @keyframes pulse {
        0%,100% { box-shadow: 0 6px 20px rgba(99,102,241,0.45); }
        50% { box-shadow: 0 6px 32px rgba(168,85,247,0.75); }
    }

    h1 {
        font-size: clamp(22px, 5vw, 32px); margin: 14px 0 6px;
        background: linear-gradient(90deg, #38bdf8, #a78bfa, #f472b6);
        -webkit-background-clip: text; background-clip: text; color: transparent;
        font-weight: 800; letter-spacing: -0.5px;
        display: inline-flex; align-items: center; gap: 10px; justify-content: center;
        flex-wrap: wrap;
    }
    h1 .ico { width: 28px; height: 28px; stroke: #f472b6; filter: drop-shadow(0 0 10px rgba(244,114,182,0.5)); }
    .subtitle { color: #94a3b8; font-size: 14px; max-width: 520px; margin: 0 auto; }

    .quick-icons { display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin-top: 16px; }
    .icon-chip {
        display: inline-flex; align-items: center; gap: 6px;
        background: rgba(51,65,85,0.65); border: 1px solid rgba(56,189,248,0.25);
        padding: 6px 12px; border-radius: 999px; font-size: 12px;
        color: #cbd5e1; font-weight: 600; transition: 0.25s;
    }
    .icon-chip:hover { background: rgba(56,189,248,0.18); transform: translateY(-2px); }
    .icon-chip .ico { stroke: #38bdf8; }

    .section-title {
        display: flex; align-items: center; gap: 8px;
        font-size: 16px; font-weight: 800; color: #e2e8f0;
        margin: 26px 0 12px; padding-bottom: 8px;
        border-bottom: 1px dashed rgba(56,189,248,0.25);
    }
    .section-title .ico { stroke: #38bdf8; width: 20px; height: 20px; }

    .uid-form {
        background: linear-gradient(145deg, rgba(15,23,42,0.9), rgba(30,41,59,0.85));
        border: 1px solid rgba(56,189,248,0.3);
        border-radius: 16px; padding: 18px;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
    }
    .input-wrap { position: relative; }
    .input-wrap .prefix {
        position: absolute; left: 14px; top: 50%; transform: translateY(-50%);
        pointer-events: none; display: inline-flex;
    }
    .input-wrap .prefix .ico { stroke: #38bdf8; width: 20px; height: 20px; }
    input[type="text"] {
        width: 100%; padding: 14px 14px 14px 46px;
        background: #0b1220; border: 2px solid #1e293b; border-radius: 12px;
        color: #f8fafc; font-size: 16px; font-weight: 600;
        outline: none; transition: 0.25s; font-family: inherit;
    }
    input:focus { border-color: #38bdf8; box-shadow: 0 0 0 4px rgba(56,189,248,0.15); }

    .btn-row { display: flex; gap: 10px; margin-top: 12px; flex-wrap: wrap; }
    .btn {
        flex: 1; min-width: 140px; padding: 13px 18px;
        border: none; border-radius: 12px; font-size: 15px;
        font-weight: 800; cursor: pointer; letter-spacing: 0.3px;
        transition: 0.25s; display: inline-flex; align-items: center;
        justify-content: center; gap: 8px; font-family: inherit;
    }
    .btn-primary {
        background: linear-gradient(135deg, #0ea5e9, #6366f1);
        color: white; box-shadow: 0 8px 22px rgba(14,165,233,0.45);
    }
    .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 12px 28px rgba(99,102,241,0.55); }
    .btn-primary:active { transform: scale(0.98); }
    .btn-primary:disabled { opacity: 0.6; cursor: wait; }
    .btn .ico { stroke: white; }

    #result {
        margin-top: 16px; display: none;
        background: linear-gradient(145deg, #0b1220, #111a2e);
        border: 1px solid rgba(74,222,128,0.35);
        border-radius: 16px; padding: 18px;
        animation: fadeUp 0.4s ease;
    }
    #result.error { border-color: rgba(248,113,113,0.5); }
    @keyframes fadeUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }

    .player-head { display: flex; align-items: center; gap: 14px; margin-bottom: 14px; }
    .avatar {
        width: 60px; height: 60px; border-radius: 50%;
        background: linear-gradient(135deg, #0ea5e9, #a855f7);
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 0 22px rgba(168,85,247,0.55); flex-shrink: 0;
    }
    .avatar .ico { width: 30px; height: 30px; stroke: white; }
    .player-name { font-size: 18px; font-weight: 800; color: #f1f5f9; }
    .player-region {
        font-size: 12px; color: #94a3b8; margin-top: 4px;
        display: inline-flex; align-items: center; gap: 5px;
    }
    .player-region .ico { stroke: #38bdf8; }
    .player-region .tag { background: #1e40af; color: #bfdbfe; padding: 2px 8px; border-radius: 6px; font-weight: 700; }

    .info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; }
    .info-item {
        background: rgba(30,41,59,0.7); padding: 10px 12px;
        border-radius: 10px; border-left: 3px solid #38bdf8;
    }
    .info-item .lbl {
        font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px;
        display: inline-flex; align-items: center; gap: 5px;
    }
    .info-item .lbl .ico { stroke: #38bdf8; width: 13px; height: 13px; }
    .info-item .val { font-size: 14px; font-weight: 700; color: #e2e8f0; margin-top: 4px; word-break: break-word; }

    .credit-line {
        margin-top: 14px; text-align: center; font-size: 12px;
        color: #64748b; padding-top: 12px; border-top: 1px dashed #1e293b;
        display: flex; align-items: center; justify-content: center; gap: 6px;
    }
    .credit-line .ico { stroke: #a78bfa; }

    .endpoint-pill {
        display: flex; align-items: center; gap: 10px;
        background: linear-gradient(145deg, #0b1220, #111a2e);
        border: 1px solid rgba(56,189,248,0.25);
        border-radius: 12px; padding: 12px 14px; margin-top: 10px;
        font-family: monospace; font-size: 13px; color: #38bdf8;
        word-break: break-all;
    }
    .endpoint-pill .pill-ico { flex-shrink: 0; display: inline-flex; }
    .endpoint-pill .pill-ico .ico { stroke: #38bdf8; width: 18px; height: 18px; }
    .endpoint-pill .pill-text { flex: 1; min-width: 0; }
    .endpoint-pill .copy-mini {
        margin-left: auto; flex-shrink: 0;
        background: rgba(56,189,248,0.15); color: #38bdf8;
        border: 1px solid rgba(56,189,248,0.3); border-radius: 8px;
        padding: 5px 10px; font-size: 11px; font-weight: 700;
        cursor: pointer; transition: 0.2s; font-family: inherit;
        display: inline-flex; align-items: center; gap: 4px;
    }
    .endpoint-pill .copy-mini .ico { stroke: #38bdf8; width: 12px; height: 12px; }
    .endpoint-pill .copy-mini:hover { background: rgba(56,189,248,0.3); }

    .code-box { position: relative; margin-top: 10px; }
    .code-header {
        display: flex; justify-content: space-between; align-items: center;
        background: #0b1220; padding: 8px 14px; border-radius: 12px 12px 0 0;
        border-bottom: 1px solid #1e293b; font-size: 12px; color: #94a3b8;
        gap: 10px; flex-wrap: wrap;
    }
    .code-header .dots { display: flex; gap: 5px; }
    .code-header .dots i { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
    .code-header .dots i:nth-child(1) { background: #ef4444; }
    .code-header .dots i:nth-child(2) { background: #f59e0b; }
    .code-header .dots i:nth-child(3) { background: #22c55e; }
    .code-header .file-name { display: inline-flex; align-items: center; gap: 5px; }
    .code-header .file-name .ico { stroke: #38bdf8; width: 13px; height: 13px; }
    .copy-btn {
        background: linear-gradient(135deg, #0ea5e9, #6366f1);
        color: white; border: none; padding: 6px 14px;
        border-radius: 8px; font-size: 12px; font-weight: 700;
        cursor: pointer; transition: 0.2s; display: inline-flex;
        align-items: center; gap: 5px; font-family: inherit;
    }
    .copy-btn .ico { stroke: white; width: 13px; height: 13px; }
    .copy-btn:hover { transform: scale(1.05); }
    .copy-btn.copied { background: linear-gradient(135deg, #22c55e, #16a34a); }
    pre {
        background: #020617; margin: 0; padding: 16px;
        border-radius: 0 0 12px 12px; overflow-x: auto;
        font-size: 12px; line-height: 1.65; color: #cbd5e1;
        font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
        border-left: 3px solid #38bdf8; white-space: pre;
        max-height: 380px;
    }
    pre::-webkit-scrollbar { height: 8px; width: 8px; }
    pre::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }

    .footer { text-align: center; margin-top: 28px; padding-top: 20px; border-top: 1px solid rgba(56,189,248,0.15); }
    .footer .heart-ico {
        display: inline-flex; vertical-align: middle; animation: beat 1.4s infinite;
        color: #f472b6;
    }
    .footer .heart-ico .ico { stroke: #f472b6; fill: rgba(244,114,182,0.3); width: 14px; height: 14px; }
    @keyframes beat { 0%,100%{transform:scale(1);} 50%{transform:scale(1.25);} }
    .footer .dev { font-size: 13px; color: #94a3b8; display: inline-flex; align-items: center; gap: 5px; justify-content: center; }
    .footer .dev b { color: #38bdf8; }
    .tg-link {
        display: inline-flex; align-items: center; gap: 7px;
        margin-top: 10px; background: linear-gradient(135deg, #0ea5e9, #6366f1);
        color: white; padding: 9px 18px; border-radius: 999px;
        text-decoration: none; font-weight: 700; font-size: 13px;
        box-shadow: 0 6px 18px rgba(14,165,233,0.4); transition: 0.25s;
    }
    .tg-link .ico { stroke: white; width: 14px; height: 14px; }
    .tg-link:hover { transform: translateY(-2px); box-shadow: 0 10px 24px rgba(99,102,241,0.55); }

    #toast {
        position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%) translateY(80px);
        background: linear-gradient(135deg, #22c55e, #16a34a); color: white;
        padding: 12px 22px; border-radius: 12px; font-weight: 700; font-size: 14px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.4); opacity: 0; transition: 0.35s;
        z-index: 999; pointer-events: none;
        display: flex; align-items: center; gap: 8px;
    }
    #toast .ico { stroke: white; width: 16px; height: 16px; }
    #toast.show { opacity: 1; transform: translateX(-50%) translateY(0); }
    #toast.error { background: linear-gradient(135deg, #ef4444, #dc2626); }
    #toast.warn { background: linear-gradient(135deg, #f59e0b, #d97706); }

    .spinner {
        width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3);
        border-top-color: white; border-radius: 50%;
        animation: spin 0.7s linear infinite; display: inline-block;
    }
    @keyframes spin { to { transform: rotate(360deg); } }

    @media (max-width: 480px) {
        .container { padding: 20px 14px 24px; border-radius: 18px; }
        .btn { font-size: 14px; padding: 12px 14px; }
        pre { font-size: 11px; padding: 12px; }
        .info-grid { grid-template-columns: repeat(2, 1fr); }
        .icon-chip { font-size: 11px; padding: 5px 10px; }
        .endpoint-pill { font-size: 11px; padding: 10px 12px; flex-wrap: wrap; }
    }
</style>
</head>
<body>
<div class="container">

    <!-- HERO -->
    <div class="hero">
        <div class="logo-badge">
            <svg class="ico" viewBox="0 0 24 24"><path d="M3 7l4 5 5-8 5 8 4-5v11H3z"/></svg>
            M1NX VIP SYSTEM &middot; v2.0
        </div>
        <h1>
            <svg class="ico" viewBox="0 0 24 24"><path d="M8.5 14.5A2.5 2.5 0 0011 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 11-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 002.5 2.5z"/></svg>
            Free Fire UID Info API
        </h1>
        <p class="subtitle">Ultra-fast, auto-region detection API for Free Fire players. Integrate into your Telegram bot or any app instantly.</p>

        <div class="quick-icons">
            <span class="icon-chip">
                <svg class="ico" viewBox="0 0 24 24"><path d="M13 2L3 14h7l-1 8 10-12h-7l1-8z"/></svg>
                Fast
            </span>
            <span class="icon-chip">
                <svg class="ico" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 010 20M12 2a15 15 0 000 20"/></svg>
                Auto-Region
            </span>
            <span class="icon-chip">
                <svg class="ico" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 14h3M1 9h3M1 14h3"/></svg>
                Bot-Ready
            </span>
            <span class="icon-chip">
                <svg class="ico" viewBox="0 0 24 24"><rect x="5" y="2" width="14" height="20" rx="2"/><path d="M12 18h.01"/></svg>
                Mobile
            </span>
            <span class="icon-chip">
                <svg class="ico" viewBox="0 0 24 24"><path d="M12 2l8 4v6c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10V6l8-4z"/></svg>
                Free
            </span>
        </div>
    </div>

    <!-- LIVE UID CHECKER -->
    <div class="section-title">
        <svg class="ico" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>
        Live UID Checker
    </div>
    <div class="uid-form">
        <div class="input-wrap">
            <span class="prefix">
                <svg class="ico" viewBox="0 0 24 24"><rect x="2" y="5" width="20" height="14" rx="2"/><circle cx="8" cy="12" r="2"/><path d="M14 10h4M14 14h4M5 16c0-1.66 1.34-3 3-3s3 1.34 3 3"/></svg>
            </span>
            <input id="uidInput" type="text" inputmode="numeric" placeholder="Enter Free Fire UID (e.g. 8497574400)" autocomplete="off">
        </div>
        <div class="btn-row">
            <button class="btn btn-primary" id="checkBtn" onclick="checkUID()">
                <span id="btnIcon">
                    <svg class="ico" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
                </span>
                <span id="btnText">Check Player</span>
            </button>
        </div>
        <div id="result"></div>
    </div>

    <!-- ENDPOINTS -->
    <div class="section-title">
        <svg class="ico" viewBox="0 0 24 24"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/></svg>
        API Endpoints
    </div>
    <div class="endpoint-pill">
        <span class="pill-ico">
            <svg class="ico" viewBox="0 0 24 24"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/></svg>
        </span>
        <span class="pill-text" id="ep1">https://{{ domain }}/?uid=YOUR_UID</span>
        <button class="copy-mini" onclick="copyText(document.getElementById('ep1').innerText, this)">
            <svg class="ico" viewBox="0 0 24 24"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
            Copy
        </button>
    </div>
    <div class="endpoint-pill">
        <span class="pill-ico">
            <svg class="ico" viewBox="0 0 24 24"><path d="M13 2L3 14h7l-1 8 10-12h-7l1-8z"/></svg>
        </span>
        <span class="pill-text" id="ep2">https://{{ domain }}/xp-opu?uid=YOUR_UID</span>
        <button class="copy-mini" onclick="copyText(document.getElementById('ep2').innerText, this)">
            <svg class="ico" viewBox="0 0 24 24"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
            Copy
        </button>
    </div>
    <div class="endpoint-pill">
        <span class="pill-ico">
            <svg class="ico" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>
        </span>
        <span class="pill-text" id="ep3">https://{{ domain }}/?uid=YOUR_UID&amp;region=BD</span>
        <button class="copy-mini" onclick="copyText(document.getElementById('ep3').innerText, this)">
            <svg class="ico" viewBox="0 0 24 24"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
            Copy
        </button>
    </div>

    <!-- BOT CODE -->
    <div class="section-title">
        <svg class="ico" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 14h3M1 9h3M1 14h3"/></svg>
        Telegram Bot Integration Code
    </div>
    <p style="color:#94a3b8;font-size:13px;margin-bottom:8px;">Copy this ready-to-run Python code, paste into your bot project, and deploy instantly.</p>
    <div class="code-box">
        <div class="code-header">
            <div class="dots"><i></i><i></i><i></i></div>
            <span class="file-name">
                <svg class="ico" viewBox="0 0 24 24"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
                bot.py &middot; Python 3
            </span>
            <button class="copy-btn" id="copyBotBtn" onclick="copyBotCode()">
                <span id="copyIcon">
                    <svg class="ico" viewBox="0 0 24 24"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
                </span>
                <span id="copyLabel">Copy Code</span>
            </button>
        </div>
        <pre id="botCode">import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ==========================================
#  M1NX VIP  |  Free Fire UID Info Bot
#  Contact : @M1NXGAMINGVIP
# ==========================================

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
API_URL   = "https://{{ domain }}/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "<b>M1NX VIP UID Bot</b>\n\n"
        "Send: <code>/info &lt;UID&gt;</code>\n"
        "Example: <code>/info 8497574400</code>\n\n"
        "Contact: @M1NXGAMINGVIP",
        parse_mode="HTML"
    )

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Please provide a UID!\n"
            "Usage: /info 8497574400"
        )
        return

    uid = context.args[0]
    msg = await update.message.reply_text(
        "<b>Fetching player info...</b>",
        parse_mode="HTML"
    )

    try:
        res = requests.get(f"{API_URL}?uid={uid}", timeout=10)
        data = res.json()

        if data.get("status") == "success":
            text = (
                "<b>M1NX VIP | Player Info</b>\n"
                "------------------------\n"
                f"Name     : {data.get('nickname')}\n"
                f"UID      : <code>{data.get('uid')}</code>\n"
                f"Region   : {data.get('detected_region')}\n"
                f"Level    : {data.get('level')}\n"
                f"EXP      : {data.get('exp')}\n"
                f"Likes    : {data.get('likes')}\n"
                f"BR Rank  : {data.get('br_rank')}\n"
                f"CS Rank  : {data.get('cs_rank')}\n"
                f"Bio      : {data.get('bio')}\n"
                "------------------------\n"
                "<b>Powered by M1NX VIP</b>\n"
                "Contact: @M1NXGAMINGVIP"
            )
            await msg.edit_text(text, parse_mode="HTML")
        else:
            await msg.edit_text("Player information not found.")
    except Exception as e:
        await msg.edit_text(f"Error: {str(e)}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()</pre>
    </div>

    <!-- FOOTER -->
    <div class="footer">
        <p class="dev">
            Made with
            <span class="heart-ico">
                <svg class="ico" viewBox="0 0 24 24"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg>
            </span>
            by <b>M1NX GAMING VIP</b>
        </p>
        <a class="tg-link" href="https://t.me/M1NXGAMINGVIP" target="_blank">
            <svg class="ico" viewBox="0 0 24 24"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
            @M1NXGAMINGVIP
        </a>
    </div>

</div>

<div id="toast"></div>

<script>
    // ============ SVG ICON LIBRARY (JS) ============
    const IC = {
        search:   '<svg class="ico" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>',
        user:     '<svg class="ico" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
        idCard:   '<svg class="ico ico-sm" viewBox="0 0 24 24"><rect x="2" y="5" width="20" height="14" rx="2"/><circle cx="8" cy="12" r="2"/><path d="M14 10h4M14 14h4M5 16c0-1.66 1.34-3 3-3s3 1.34 3 3"/></svg>',
        star:     '<svg class="ico ico-sm" viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
        chart:    '<svg class="ico ico-sm" viewBox="0 0 24 24"><path d="M3 3v18h18M7 14l4-4 4 4 5-7"/></svg>',
        heart:    '<svg class="ico ico-sm" viewBox="0 0 24 24"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg>',
        trophy:   '<svg class="ico ico-sm" viewBox="0 0 24 24"><path d="M6 9H4.5a2.5 2.5 0 010-5H6M18 9h1.5a2.5 2.5 0 000-5H18M4 22h16M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22M18 2H6v7a6 6 0 0012 0V2z"/></svg>',
        sword:    '<svg class="ico ico-sm" viewBox="0 0 24 24"><path d="M14.5 17.5L3 6V3h3l11.5 11.5M13 19l6-6M16 16l4 4M19 21l2-2"/></svg>',
        calendar: '<svg class="ico ico-sm" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>',
        clock:    '<svg class="ico ico-sm" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
        globe:    '<svg class="ico ico-sm" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 010 20M12 2a15 15 0 000 20"/></svg>',
        gem:      '<svg class="ico" viewBox="0 0 24 24"><path d="M6 3h12l4 6-10 13L2 9zM11 3L8 9l4 13 4-13-3-6M2 9h20"/></svg>',
        check:    '<svg class="ico" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>',
        x:        '<svg class="ico" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
        alert:    '<svg class="ico" viewBox="0 0 24 24"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
        copy:     '<svg class="ico" viewBox="0 0 24 24"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>',
        xcircle:  '<svg class="ico ico-xl" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>',
    };

    // ============ UID CHECKER ============
    async function checkUID() {
        const uid = document.getElementById('uidInput').value.trim();
        const btn = document.getElementById('checkBtn');
        const btnIcon = document.getElementById('btnIcon');
        const btnText = document.getElementById('btnText');
        const result = document.getElementById('result');

        if (!uid) {
            showToast('Please enter a UID first!', 'warn');
            return;
        }

        btn.disabled = true;
        btnIcon.innerHTML = '<span class="spinner"></span>';
        btnText.textContent = 'Checking...';
        result.style.display = 'none';

        try {
            const res = await fetch(`/?uid=${encodeURIComponent(uid)}`);
            const data = await res.json();

            if (data.status === 'success') {
                result.className = '';
                result.innerHTML = `
                    <div class="player-head">
                        <div class="avatar">${IC.user}</div>
                        <div>
                            <div class="player-name">${data.nickname}</div>
                            <div class="player-region">${IC.globe} Region: <span class="tag">${data.detected_region}</span></div>
                        </div>
                    </div>
                    <div class="info-grid">
                        <div class="info-item"><div class="lbl">${IC.idCard} UID</div><div class="val">${data.uid}</div></div>
                        <div class="info-item"><div class="lbl">${IC.star} Level</div><div class="val">${data.level}</div></div>
                        <div class="info-item"><div class="lbl">${IC.chart} EXP</div><div class="val">${data.exp}</div></div>
                        <div class="info-item"><div class="lbl">${IC.heart} Likes</div><div class="val">${data.likes}</div></div>
                        <div class="info-item"><div class="lbl">${IC.trophy} BR Rank</div><div class="val">${data.br_rank}</div></div>
                        <div class="info-item"><div class="lbl">${IC.sword} CS Rank</div><div class="val">${data.cs_rank}</div></div>
                        <div class="info-item"><div class="lbl">${IC.calendar} Created</div><div class="val">${data.account_created}</div></div>
                        <div class="info-item"><div class="lbl">${IC.clock} Last Login</div><div class="val">${data.last_login}</div></div>
                    </div>
                    <div class="credit-line">${IC.gem} ${data.credit}</div>
                `;
            } else {
                result.className = 'error';
                result.innerHTML = `
                    <div style="text-align:center;padding:10px 0;">
                        <div style="display:inline-flex;color:#f87171;margin-bottom:6px;">${IC.xcircle}</div>
                        <div style="font-weight:700;color:#f87171;">${data.error || 'Player not found'}</div>
                    </div>
                `;
            }
            result.style.display = 'block';
        } catch (e) {
            result.className = 'error';
            result.innerHTML = `
                <div style="text-align:center;padding:10px 0;">
                    <div style="display:inline-flex;color:#f87171;margin-bottom:6px;">${IC.xcircle}</div>
                    <div style="font-weight:700;color:#f87171;">Network Error. Try again.</div>
                </div>
            `;
            result.style.display = 'block';
        } finally {
            btn.disabled = false;
            btnIcon.innerHTML = IC.search;
            btnText.textContent = 'Check Player';
        }
    }

    document.getElementById('uidInput').addEventListener('keypress', e => {
        if (e.key === 'Enter') checkUID();
    });

    // ============ COPY HELPERS ============
    function copyText(text, btnEl) {
        const doToast = () => {
            showToast('Copied to clipboard!', 'success');
            if (btnEl) {
                const original = btnEl.innerHTML;
                btnEl.innerHTML = IC.check + ' Copied';
                setTimeout(() => { btnEl.innerHTML = original; }, 1600);
            }
        };
        if (navigator.clipboard && window.isSecureContext) {
            navigator.clipboard.writeText(text).then(doToast).catch(() => fallbackCopy(text, doToast));
        } else {
            fallbackCopy(text, doToast);
        }
    }
    function fallbackCopy(text, cb) {
        const ta = document.createElement('textarea');
        ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
        document.body.appendChild(ta); ta.select();
        try { document.execCommand('copy'); cb(); }
        catch (e) { showToast('Copy failed', 'error'); }
        document.body.removeChild(ta);
    }

    function copyBotCode() {
        const code = document.getElementById('botCode').innerText;
        const btn = document.getElementById('copyBotBtn');
        const label = document.getElementById('copyLabel');
        const icon = document.getElementById('copyIcon');

        copyText(code, null);
        btn.classList.add('copied');
        label.textContent = 'Copied!';
        icon.innerHTML = IC.check;
        setTimeout(() => {
            btn.classList.remove('copied');
            label.textContent = 'Copy Code';
            icon.innerHTML = IC.copy;
        }, 2000);
    }

    // ============ TOAST ============
    let toastTimer;
    function showToast(msg, type) {
        const t = document.getElementById('toast');
        const iconMap = { success: IC.check, error: IC.x, warn: IC.alert };
        t.innerHTML = (iconMap[type] || IC.check) + ' <span>' + msg + '</span>';
        t.className = 'show ' + (type || 'success');
        clearTimeout(toastTimer);
        toastTimer = setTimeout(() => { t.className = t.className.replace('show','').trim(); }, 2000);
    }
</script>
</body>
</html>
"""


@app.route('/', methods=['GET'])
def home_region_info():
    uid = request.args.get('uid')
    region = request.args.get('region')

    if not uid:
        domain_name = request.host
        return render_template_string(HOME_HTML, domain=domain_name)

    result, status_code = fetch_player_auto(uid, region)
    return jsonify(result), status_code


@app.route('/xp-opu', methods=['GET'])
def get_region_info():
    uid = request.args.get('uid')
    region = request.args.get('region')

    if not uid:
        return jsonify({"error": "UID parameter is required", "developer": "M1NX GAMING VIP"}), 400

    result, status_code = fetch_player_auto(uid, region)
    return jsonify(result), status_code


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)