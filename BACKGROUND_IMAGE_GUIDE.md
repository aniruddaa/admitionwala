# Background Image Integration Guide

## Current Status
✅ **Old background images deleted**
✅ **Professional color scheme applied**
✅ **Header, Footer, Buttons updated**

## Color Scheme Applied
- **Header**: Dark blue gradient (#2c3e50 to #34495e)
- **Footer**: Dark blue gradient with professional styling
- **Buttons**: Professional blue (#3498db to #2980b9)
- **Background**: Purple gradient (ready for your image)
- **Accent Color**: Professional blue (#3498db)

## How to Add Your Background Image

### Option 1: Save Image to Project
1. Save your image as `bg-image.jpg` in `static/images/` folder
2. Uncomment the CSS in `static/background.css` (lines 25-29):

```css
.bg-animations {
  background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)),
              url('/static/images/bg-image.jpg') center center/cover no-repeat;
  background-attachment: fixed;
}
```

### Option 2: Upload via Django Admin
1. Go to Django admin panel
2. Create a media folder for background images
3. Upload your image there
4. Update the CSS path to reference it

### Option 3: Use External URL
Update the CSS to use your image URL directly:
```css
background-image: url('https://your-image-url.jpg');
```

## File Structure
```
static/
├── background.css (Professional colors & styling)
├── design.css (Updated accent colors)
├── custom.css (Updated button colors)
├── images/
│   ├── admitionwala_logo.svg
│   └── bg-image.jpg (YOUR IMAGE HERE)
└── ...
```

## Current Color Palette
```
Primary Blue: #3498db
Dark Blue: #2980b9
Dark Gray: #2c3e50
Light Gray: #ecf0f1
```

## Testing the Changes
1. Restart Django server: `python manage.py runserver`
2. Visit http://localhost:8000/
3. Verify:
   - Header is dark blue with professional styling ✓
   - Footer is dark blue ✓
   - All buttons are professional blue ✓
   - Background is purple gradient (ready for image) ✓
   - Text colors are readable ✓

## Next Steps
1. Add your background image to `static/images/bg-image.jpg`
2. Uncomment the image CSS in `static/background.css`
3. Reload your browser (clear cache if needed)
4. Verify the background image displays correctly

## Notes
- Old background images (bg-hero.jpg, college_bg.jpg) have been removed
- All color references updated from orange to professional blue
- Professional color scheme applied across all pages
- Ready to accept your custom background image
