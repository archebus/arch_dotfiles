#!/usr/bin/env python3
import subprocess
import sys
import time
import json

# Same server list as status script
VPN_SERVERS = {
    "AUS": {"server": "au-syd-wg-001", "name": "Australia"},
    "SGP": {"server": "sg-sin-wg-001", "name": "Singapore"}, 
    "JPN": {"server": "jp-tok-wg-001", "name": "Japan"},
    "USA": {"server": "us-sfo-wg-001", "name": "USA West"},
    "UK": {"server": "gb-lon-wg-001", "name": "UK"}
}

# Order for cycling
SERVER_ORDER = ["AUS", "SGP", "JPN", "USA", "UK"]

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
                if "Relay:" in line:
                    server_info = line.split(":", 1)[1].strip()
                    # Match against our servers
                    for code, info in VPN_SERVERS.items():
                        if info["server"] in server_info:
                            return code
        return None
    except:
        return None

def connect_to_server(server_code):
    """Connect to a specific server"""
    if server_code not in VPN_SERVERS:
        print(f"Unknown server code: {server_code}")
        return False
    
    server = VPN_SERVERS[server_code]["server"]
    name = VPN_SERVERS[server_code]["name"]
    
    try:
        # Disconnect first if connected
        subprocess.run(['mullvad', 'disconnect'], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE, 
                      timeout=10)
        time.sleep(1)
        
        # Connect to new server
        result = subprocess.run(['mullvad', 'connect', '--server', server], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE, 
                              timeout=30)
        
        if result.returncode == 0:
            # Send notification (optional - requires notify-send)
            try:
                subprocess.run(['notify-send', 
                              'VPN Connected', 
                              f'Connected to {name}', 
                              '--icon=network-vpn'], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
            except:
                pass  # Notification not critical
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error connecting: {e}")
        return False

def get_next_server(current, direction="next"):
    """Get the next server in the cycle"""
    if current not in SERVER_ORDER:
        # If not connected to one of our servers, start with first
        return SERVER_ORDER[0]
    
    current_index = SERVER_ORDER.index(current)
    
    if direction == "next":
        next_index = (current_index + 1) % len(SERVER_ORDER)
    else:  # prev
        next_index = (current_index - 1) % len(SERVER_ORDER)
    
    return SERVER_ORDER[next_index]

def main():
    if len(sys.argv) < 2:
        # Default behavior: cycle to next server
        action = "next"
    else:
        action = sys.argv[1].lower()
    
    current_location = get_current_location()
    
    if action in ["next", "prev"]:
        # Cycle through servers
        next_server = get_next_server(current_location, action)
        if connect_to_server(next_server):
            print(f"Connected to {VPN_SERVERS[next_server]['name']}")
        else:
            print(f"Failed to connect to {VPN_SERVERS[next_server]['name']}")
    
    elif action == "disconnect":
        # Disconnect VPN
        try:
            subprocess.run(['mullvad', 'disconnect'], timeout=10)
            print("VPN disconnected")
        except:
            print("Failed to disconnect")
    
    elif action.upper() in VPN_SERVERS:
        # Connect to specific server
        server_code = action.upper()
        if connect_to_server(server_code):
            print(f"Connected to {VPN_SERVERS[server_code]['name']}")
        else:
            print(f"Failed to connect to {VPN_SERVERS[server_code]['name']}")
    
    else:
        print(f"Usage: {sys.argv[0]} [next|prev|disconnect|{'/'.join(SERVER_ORDER)}]")
        sys.exit(1)

if __name__ == "__main__":
    main()
