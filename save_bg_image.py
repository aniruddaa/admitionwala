#!/usr/bin/env python3
"""
Background Image Auto-Save Script
Saves the background image to static/images/bg-image.jpg
"""

import os
import shutil
from pathlib import Path

def save_background_image():
    """Save background image to the correct location"""
    
    # Define paths
    static_images_dir = Path("static/images")
    bg_image_path = static_images_dir / "bg-image.jpg"
    
    # Ensure directory exists
    static_images_dir.mkdir(parents=True, exist_ok=True)
    
    # Try to find the image in common locations
    possible_locations = [
        Path.home() / "Downloads" / "image.jpg",
        Path.home() / "Downloads" / "bg.jpg",
        Path.home() / "Desktop" / "image.jpg",
        Path.home() / "Pictures" / "image.jpg",
        Path("~/image.jpg").expanduser(),
    ]
    
    source_found = False
    
    for possible_path in possible_locations:
        if possible_path.exists():
            try:
                shutil.copy2(possible_path, bg_image_path)
                print(f"✅ Background image saved successfully!")
                print(f"   From: {possible_path}")
                print(f"   To: {bg_image_path.absolute()}")
                print(f"   File size: {bg_image_path.stat().st_size / 1024:.1f} KB")
                source_found = True
                break
            except Exception as e:
                print(f"❌ Error copying from {possible_path}: {e}")
    
    if not source_found:
        print("⚠️  Background image file not found in common locations.")
        print("\nTo add your background image manually:")
        print(f"1. Save your image as 'bg-image.jpg'")
        print(f"2. Move it to: {static_images_dir.absolute()}")
        print(f"3. Refresh your browser")
        
        # Create a placeholder gradient image using PIL if available
        try:
            from PIL import Image, ImageDraw
            
            # Create a professional gradient background
            width, height = 1920, 1200
            image = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(image, 'RGBA')
            
            # Create gradient from purple to blue
            for y in range(height):
                r = int(102 + (118 - 102) * (y / height))
                g = int(126 + (75 - 126) * (y / height))
                b = int(234 + (162 - 234) * (y / height))
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            image.save(bg_image_path, 'JPEG', quality=85)
            print(f"\n✅ Created placeholder gradient image at: {bg_image_path.absolute()}")
            
        except ImportError:
            print("Note: PIL not installed. Install it with: pip install Pillow")

if __name__ == "__main__":
    save_background_image()
