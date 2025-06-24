#!/usr/bin/env python3
# ~/.config/waybar/scripts/vpn_minimal.py

import subprocess
import json
import sys

def get_mullvad_status():
    """Get current Mullvad VPN status"""
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
            return True, output.strip(), None
        else:
            return False, None, None
            
    except subprocess.TimeoutExpired:
        return False, None, "Timeout"
    except FileNotFoundError:
        return False, None, "Mullvad CLI not found"
    except Exception as e:
        return False, None, str(e)

def main():
    connected, server_info, error = get_mullvad_status()
    
    if error:
        # Error state
        output = {
            "text": "x",  # Unlock icon
            "tooltip": f"Error: {error}",
            "class": "vpn-disconnected"
        }
    elif connected:
        # Connected - show lock icon
        output = {
            "text": "󰒃",  # Lock icon
            "tooltip": f"VPN Connected\n{server_info}",
            "class": "vpn-connected"
        }
    else:
        # Disconnected - show unlock icon
        output = {
            "text": "x",  # Unlock icon
            "tooltip": "VPN Disconnected",
            "class": "vpn-disconnected"
        }
    
    print(json.dumps(output))

if __name__ == "__main__":
    main()
