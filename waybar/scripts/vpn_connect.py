#!/usr/bin/env python3
import subprocess
import sys
import time

# Updated server list with flag emojis
VPN_SERVERS = {
    "AUS": {"location": "au adl au-adl-wg-301", "name": "Australia", "city": "Adelaide", "flag": "🇦🇺"},
    "SWE": {"location": "se sto se-sto-wg-001", "name": "Sweden", "city": "Stockholm", "flag": "🇸🇪"},
    "SGP": {"location": "sg sin sg-sin-wg-001", "name": "Singapore", "city": "Singapore", "flag": "🇸🇬"},
    "JPN": {"location": "jp tok jp-tok-wg-001", "name": "Japan", "city": "Tokyo", "flag": "🇯🇵"},
    "USA": {"location": "us sfo us-sfo-wg-001", "name": "USA", "city": "San Francisco", "flag": "🇺🇸"},
    "UK": {"location": "gb lon gb-lon-wg-001", "name": "UK", "city": "London", "flag": "🇬🇧"}
}

def connect_to_server(server_code):
    """Connect to a specific server using correct Mullvad CLI syntax"""
    if server_code not in VPN_SERVERS:
        print(f"Unknown server code: {server_code}")
        return False
    
    location = VPN_SERVERS[server_code]["location"]
    name = VPN_SERVERS[server_code]["name"]
    
    try:
        # Disconnect first if connected
        print(f"Disconnecting from current server...")
        subprocess.run(['mullvad', 'disconnect'], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE, 
                      timeout=10)
        time.sleep(2)  # Give it time to disconnect
        
        # Set the relay location
        print(f"Setting location to {name}...")
        location_parts = location.split()
        result = subprocess.run(['mullvad', 'relay', 'set', 'location'] + location_parts, 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE, 
                              timeout=15)
        
        if result.returncode != 0:
            error_msg = result.stderr.decode() if result.stderr else "Unknown error setting location"
            print(f"Failed to set location: {error_msg}")
            return False
        
        # Connect
        print(f"Connecting to {name}...")
        result = subprocess.run(['mullvad', 'connect'], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE, 
                              timeout=30)
        
        if result.returncode == 0:
            # Send notification (optional - requires notify-send)
            try:
                subprocess.run(['notify-send', 
                              'VPN Connected', 
                              f'Connected to {name}', 
                              '--icon=network-vpn',
                              '--timeout=3000'], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
            except:
                pass  # Notification not critical
            print(f"Successfully connected to {name}")
            return True
        else:
            error_msg = result.stderr.decode() if result.stderr else "Unknown error"
            print(f"Failed to connect to {name}: {error_msg}")
            return False
            
    except Exception as e:
        print(f"Error connecting: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} [AUS|SWE|SGP|JPN|USA|UK]")
        sys.exit(1)
    
    server_code = sys.argv[1].upper()
    
    if server_code not in VPN_SERVERS:
        print(f"Unknown server code: {server_code}")
        print(f"Available servers: {', '.join(VPN_SERVERS.keys())}")
        sys.exit(1)
    
    success = connect_to_server(server_code)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
