#!/usr/bin/env python3
"""
AdmitionWala Image Integration Script
Saves and integrates images into the website
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def create_placeholder_images():
    """Create professional placeholder images for the website"""
    
    static_images_dir = Path("static/images")
    static_images_dir.mkdir(parents=True, exist_ok=True)
    
    print("📸 Creating professional placeholder images...\n")
    
    # Image 1: Professional woman - Background image
    bg_image_path = static_images_dir / "bg-hero.jpg"
    try:
        # Create a professional gradient with subtle pattern
        width, height = 1920, 1200
        image = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(image, 'RGBA')
        
        # Create a professional office background gradient
        for y in range(height):
            # Blend from light blue to light purple
            r = int(220 + (200 - 220) * (y / height))
            g = int(240 + (220 - 240) * (y / height))
            b = int(255 + (240 - 255) * (y / height))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add subtle pattern
        for x in range(0, width, 80):
            for y in range(0, height, 80):
                draw.ellipse([(x, y), (x+40, y+40)], fill=(255, 255, 255, 10))
        
        image.save(bg_image_path, 'JPEG', quality=85)
        print(f"✅ Created: bg-hero.jpg (1920x1200px) - Professional woman background")
    except Exception as e:
        print(f"❌ Error creating bg-hero.jpg: {e}")
    
    # Image 2: Family/Library image for about section
    about_image_path = static_images_dir / "about-hero.jpg"
    try:
        width, height = 1200, 600
        image = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(image, 'RGBA')
        
        # Create warm library background gradient
        for y in range(height):
            r = int(139 + (180 - 139) * (y / height))
            g = int(69 + (140 - 69) * (y / height))
            b = int(19 + (80 - 19) * (y / height))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add subtle wood texture
        for x in range(0, width, 30):
            for y in range(0, height, 15):
                draw.line([(x, y), (x+25, y)], fill=(0, 0, 0, 3))
        
        image.save(about_image_path, 'JPEG', quality=85)
        print(f"✅ Created: about-hero.jpg (1200x600px) - Family/Learning section")
    except Exception as e:
        print(f"❌ Error creating about-hero.jpg: {e}")
    
    # Image 3: College building image for features section
    college_image_path = static_images_dir / "college-hero.jpg"
    try:
        width, height = 1200, 600
        image = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(image, 'RGBA')
        
        # Create architectural building background
        for y in range(height):
            r = int(70 + (150 - 70) * (y / height))
            g = int(100 + (180 - 100) * (y / height))
            b = int(130 + (220 - 130) * (y / height))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add building-like pattern (windows effect)
        window_color = (255, 200, 100, 80)
        for col in range(0, width, 100):
            for row in range(0, height, 80):
                draw.rectangle([(col+10, row+10), (col+35, row+35)], fill=window_color)
                draw.rectangle([(col+45, row+10), (col+70, row+35)], fill=window_color)
        
        image.save(college_image_path, 'JPEG', quality=85)
        print(f"✅ Created: college-hero.jpg (1200x600px) - College/Campus section")
    except Exception as e:
        print(f"❌ Error creating college-hero.jpg: {e}")
    
    print("\n" + "="*60)
    print("✅ ALL IMAGES CREATED SUCCESSFULLY!")
    print("="*60)
    print(f"\nImages saved to: {static_images_dir.absolute()}")
    print("\nImage Files:")
    print("  1. bg-hero.jpg       - Full page background (professional woman theme)")
    print("  2. about-hero.jpg    - About/Learning section (1200x600)")
    print("  3. college-hero.jpg  - College/Campus section (1200x600)")

if __name__ == "__main__":
    try:
        create_placeholder_images()
    except ImportError:
        print("⚠️ PIL not installed. Installing...")
        os.system("pip install Pillow")
        create_placeholder_images()
