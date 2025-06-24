#!/usr/bin/env python3
import subprocess
import json
import sys

# Same server list as status script with flag emojis
VPN_SERVERS = {
    "AUS": {"location": "au adl au-adl-wg-301", "name": "Australia", "city": "Adelaide", "flag": "🇦🇺"},
    "SWE": {"location": "se sto se-sto-wg-001", "name": "Sweden", "city": "Stockholm", "flag": "🇸🇪"},
    "SGP": {"location": "sg sin sg-sin-wg-001", "name": "Singapore", "city": "Singapore", "flag": "🇸🇬"},
    "JPN": {"location": "jp tok jp-tok-wg-001", "name": "Japan", "city": "Tokyo", "flag": "🇯🇵"},
    "USA": {"location": "us sfo us-sfo-wg-001", "name": "USA", "city": "San Francisco", "flag": "🇺🇸"},
    "UK": {"location": "gb lon gb-lon-wg-001", "name": "UK", "city": "London", "flag": "🇬🇧"}
}

def get_current_location():
    """Get currently connected location code"""
    try:
        result = subprocess.run(['mullvad', 'status'], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE, 
                              text=True, 
                              timeout=10)
        
        if "Connected" in result.stdout:
            for line in result.stdout.splitlines():
                if "Relay:" in line or "Server:" in line:
                    server_info = line.split(":", 1)[1].strip()
                    # Match against our servers
                    for code, info in VPN_SERVERS.items():
                        server_name = info["location"].split()[-1]  # Get the server name part
                        if server_name in server_info or info["city"].lower() in server_info.lower():
                            return code
        return None
    except:
        return None

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"text": "ERR", "class": "button-error"}))
        sys.exit(1)
    
    button_code = sys.argv[1].upper()
    
    if button_code not in VPN_SERVERS:
        print(json.dumps({"text": "ERR", "class": "button-error"}))
        sys.exit(1)
    
    current_location = get_current_location()
    
    # Determine button state
    if current_location == button_code:
        # This button's location is active
        output = {
            "text": VPN_SERVERS[button_code]["flag"],
            "tooltip": f"Connected to {VPN_SERVERS[button_code]['name']}\nClick to reconnect",
            "class": "button-active"
        }
    else:
        # This button's location is not active
        output = {
            "text": VPN_SERVERS[button_code]["flag"],
            "tooltip": f"Connect to {VPN_SERVERS[button_code]['name']}\n({VPN_SERVERS[button_code]['city']})",
            "class": "button-inactive"
        }
    
    print(json.dumps(output))

if __name__ == "__main__":
    main()
