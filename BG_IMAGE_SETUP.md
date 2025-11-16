# Background Image Setup Instructions

## Current Status
✅ CSS is configured to display a background image at: `/static/images/bg-image.jpg`
✅ Professional overlay gradient applied
✅ Image will display at full width with fixed attachment (parallax effect)

## How to Add Your Background Image

### Option 1: Save the Image Directly (Recommended)
1. The image you provided in the chat is ready to use
2. Save/Download it to your desktop
3. Rename it to: **bg-image.jpg**
4. Place it in: `static/images/` folder
   - Full path: `c:\Users\hp\Desktop\New folder (3)\static\images\bg-image.jpg`

### Option 2: Using Command Line
```powershell
# Copy the image file to static/images folder
Copy-Item "C:\path\to\your\image.jpg" "c:\Users\hp\Desktop\New folder (3)\static\images\bg-image.jpg"
```

## Image Requirements
- **Format**: JPG, PNG, or WebP
- **Recommended Size**: 1920x1200px or larger
- **File Size**: < 500KB (for fast loading)
- **Aspect Ratio**: 16:9 or wider

## How It Works
When you add the image:
1. CSS will load the image from `/static/images/bg-image.jpg`
2. A professional purple-blue gradient overlay will be applied (50% opacity)
3. The image will be fixed (won't scroll with page)
4. It will cover the entire background
5. Perfect for desktop and mobile views

## CSS Configuration
The background is configured as:
```css
background-image: 
  linear-gradient(135deg, rgba(102, 126, 234, 0.5) 0%, rgba(118, 75, 162, 0.5) 100%),
  url('/static/images/bg-image.jpg');
background-attachment: fixed;
background-size: cover;
background-position: center;
```

## Testing After Adding Image
1. Save the image to `static/images/bg-image.jpg`
2. Refresh your Django development server: `python manage.py runserver`
3. Clear your browser cache (Ctrl+F5 or Cmd+Shift+R)
4. Visit your site - the background image should now appear!

## If Image Doesn't Show
- Check file is named exactly: `bg-image.jpg`
- Check location: `static/images/bg-image.jpg`
- Check file size and format
- Ensure Django `STATIC_URL = '/static/'` is configured
- Run: `python manage.py collectstatic`

---
**Ready?** Save your background image and refresh the page! 🎨
