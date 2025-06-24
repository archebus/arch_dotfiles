#!/usr/bin/env python3
import subprocess
import json
import sys

# Updated VPN Server locations with working Australia servers
VPN_SERVERS = {
    "AUS": {"server": "au-adl-wg-301", "name": "Australia", "city": "Adelaide"},
    "SWE": {"server": "se-sto-wg-001", "name": "Sweden", "city": "Stockholm"},
    "SGP": {"server": "sg-sin-wg-001", "name": "Singapore", "city": "Singapore"},
    "JPN": {"server": "jp-tok-wg-001", "name": "Japan", "city": "Tokyo"},
    "USA": {"server": "us-sfo-wg-001", "name": "USA", "city": "San Francisco"},
    "UK": {"server": "gb-lon-wg-001", "name": "UK", "city": "London"}
}

def get_mullvad_status():
    """Get current Mullvad VPN status and server"""
    try:
        result = subprocess.run(['mullvad', 'status'], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE, 
                              text=True, 
                              timeout=10)
        
        if result.returncode != 0:
            return False, None, "Command failed"
            
        output = result.stdout
        
        # Check if connected
        if "Connected" in output:
            # Extract server info
            for line in output.splitlines():
                if "Relay:" in line or "Server:" in line:
                    server_info = line.split(":", 1)[1].strip()
                    return True, server_info, None
            return True, "Connected (unknown server)", None
        else:
            return False, None, None
            
    except subprocess.TimeoutExpired:
        return False, None, "Timeout"
    except FileNotFoundError:
        return False, None, "Mullvad CLI not found"
    except Exception as e:
        return False, None, str(e)

def get_current_location():
    """Determine which of our predefined locations is currently active"""
    connected, server_info, error = get_mullvad_status()
    
    if not connected or not server_info:
        return None
        
    # Match against our known servers
    for code, info in VPN_SERVERS.items():
        if info["server"] in server_info or info["city"].lower() in server_info.lower():
            return code
    
    return "OTHER"  # Connected but not to one of our predefined servers

def main():
    current_location = get_current_location()
    connected, server_info, error = get_mullvad_status()
    
    if error:
        # Error state
        output = {
            "text": "VPN ERR",
            "tooltip": f"Error: {error}",
            "class": "vpn-error"
        }
    elif connected:
        if current_location and current_location in VPN_SERVERS:
            # Connected to one of our servers
            location_name = VPN_SERVERS[current_location]["name"]
            output = {
                "text": f"VPN {current_location}",
                "tooltip": f"Connected to {location_name}\nServer: {server_info}\n\nRight-click to disconnect",
                "class": "vpn-connected"
            }
        else:
            # Connected to different server
            output = {
                "text": "VPN ON",
                "tooltip": f"Connected to: {server_info}\n\nRight-click to disconnect",
                "class": "vpn-connected-other"
            }
    else:
        # Disconnected
        output = {
            "text": "VPN OFF",
            "tooltip": "VPN Disconnected\n\nUse buttons to connect to specific locations",
            "class": "vpn-disconnected"
        }
    
    print(json.dumps(output))

if __name__ == "__main__":
    main()
