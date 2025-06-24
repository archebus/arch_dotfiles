#!/bin/bash

# Configuration
WALLPAPER_DIR="$HOME/Pictures/Wallpapers"
TRANSITION="any"
DURATION="1"
SAME_WALLPAPER="false"  # Set to "true" to use the same wallpaper on all monitors

# Create wallpapers directory if it doesn't exist
mkdir -p "$WALLPAPER_DIR"

# Check if swww daemon is running, if not initialize it
if ! pgrep -x "swww-daemon" > /dev/null; then
    swww-daemon
fi

# Function to get a random wallpaper
get_random_wallpaper() {
    find "$WALLPAPER_DIR" -type f \( -iname '*.jpg' -o -iname '*.png' -o -iname '*.jpeg' \) | shuf -n 1
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --same)
            SAME_WALLPAPER="true"
            shift
            ;;
        --dir=*)
            WALLPAPER_DIR="${1#*=}"
            shift
            ;;
        --transition=*)
            TRANSITION="${1#*=}"
            shift
            ;;
        --duration=*)
            DURATION="${1#*=}"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--same] [--dir=DIRECTORY] [--transition=TYPE] [--duration=SECONDS]"
            exit 1
            ;;
    esac
done

# Get wallpapers
if [ "$SAME_WALLPAPER" = "true" ]; then
    # Use the same wallpaper for all monitors
    WALLPAPER_SINGLE=$(get_random_wallpaper)
    WALLPAPER_LEFT="$WALLPAPER_SINGLE"
    WALLPAPER_MIDDLE="$WALLPAPER_SINGLE"
    WALLPAPER_RIGHT="$WALLPAPER_SINGLE"
    echo "Using the same wallpaper for all monitors: $WALLPAPER_SINGLE"
else
    # Get random wallpapers for each monitor
    WALLPAPER_LEFT=$(get_random_wallpaper)
    WALLPAPER_MIDDLE=$(get_random_wallpaper)
    WALLPAPER_RIGHT=$(get_random_wallpaper)
fi

# Define transition types
TRANSITIONS=("simple" "wipe" "wave" "grow" "outer" "any")
if [ "$TRANSITION" == "any" ]; then
    TRANSITION=${TRANSITIONS[$RANDOM % ${#TRANSITIONS[@]}]}
fi

echo "Setting wallpapers with $TRANSITION transition..."

# Set wallpaper for left monitor (HDMI-A-1) - horizontal 1920x1080
echo "Setting left monitor (HDMI-A-1) wallpaper to: $WALLPAPER_LEFT"
swww img --outputs HDMI-A-1 "$WALLPAPER_LEFT" \
    --transition-type "$TRANSITION" \
    --transition-duration "$DURATION" \
    --transition-fps 60 \
    --transition-pos 0.5,0.5

# Set wallpaper for middle monitor (DP-2) - horizontal 2560x1440
echo "Setting middle monitor (DP-2) wallpaper to: $WALLPAPER_MIDDLE"
swww img --outputs DP-2 "$WALLPAPER_MIDDLE" \
    --transition-type "$TRANSITION" \
    --transition-duration "$DURATION" \
    --transition-fps 60 \
    --transition-pos 0.5,0.5

# Set wallpaper for right monitor (DP-1) - vertical 1080x1920
echo "Setting right monitor (DP-1) wallpaper to: $WALLPAPER_RIGHT"
swww img --outputs DP-1 "$WALLPAPER_RIGHT" \
    --transition-type "$TRANSITION" \
    --transition-duration "$DURATION" \
    --transition-fps 60 \
    --transition-pos 0.5,0.5
