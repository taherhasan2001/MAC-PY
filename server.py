from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import platform

app = Flask(__name__)
CORS(app)  # Enable CORS

mac_dict = {
    "مكتبة غرفة 1": ["34:fc:b9:2b:96:00", "34:fc:b9:2b:96:10"],
    "مكتبة غرفة 2": ["94:64:24:ad:b5:50"],
    "مكتبة طابق2 غرفة1": ["34:fc:b9:2b:8f:70"],
    "مكتبة طابق2 غرفة2": ["34:fc:b9:2b:8e:50"]
}


def get_current_ap_mac():
    try:
        if platform.system() == 'Windows':
            result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'BSSID' in line:
                    list = line.split(':')
                    return ':'.join(list[1:len(list)]).strip()
        elif platform.system() in ['Linux', 'Darwin']:
            result = subprocess.run(['nmcli', '-t', '-f', 'ACTIVE,BSSID', 'device', 'wifi'], capture_output=True,
                                    text=True)
            for line in result.stdout.split('\n'):
                if 'yes' in line:
                    return line.split(':')[1].strip()
    except Exception as e:
        print(f"An error occurred: {e}")
    return None


@app.route('/get_ap_info')
def get_ap_info():
    current_address = get_current_ap_mac()
    if not current_address:
        return jsonify({"status": "error", "message": "Unable to get MAC address"})

    for key, values in mac_dict.items():
        if current_address in values:
            return jsonify({"status": "success", "ap_name": key, "mac_address": current_address})

    return jsonify({"status": "unknown", "mac_address": current_address})


if __name__ == '__main__':
    app.run(debug=True)
