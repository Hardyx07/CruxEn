# Developer Profile Setup Guide

## Update Your Profile Links

Open `app/page.tsx` and update the following links in the footer section:

### 1. GitHub Link (Line ~65)
```tsx
href="https://github.com/yourusername"
```
Replace `yourusername` with your actual GitHub username.

### 2. LinkedIn Link (Line ~80)
```tsx
href="https://linkedin.com/in/yourusername"
```
Replace `yourusername` with your actual LinkedIn username.

### 3. Email Link (Line ~95)
```tsx
href="mailto:your.email@example.com"
```
Replace with your actual email address.

### 4. Developer Name (Line ~52)
```tsx
<h3 className="text-2xl font-semibold text-foreground font-serif">
  Built by Hardi
</h3>
```
Update "Hardi" to your preferred display name.

### 5. Developer Description (Line ~55)
```tsx
<p className="text-sm text-muted-foreground/70 font-light max-w-md">
  Crafting intelligent solutions at the intersection of AI and elegant design
</p>
```
Update with your own tagline or description.

## Features Included

✅ **Modern glassmorphic design** matching your project's aesthetic
✅ **Hover effects** with smooth animations and glow effects  
✅ **Responsive layout** works on desktop and mobile
✅ **Three social links**: GitHub, LinkedIn, Email
✅ **Accessible** with proper ARIA labels
✅ **Auto copyright year** updates automatically
✅ **Elegant divider** with animated dots
✅ **Decorative gradient orbs** for depth

## Design Details

- **Font**: Uses your project's existing font-serif for headings
- **Colors**: Matches your accent colors and muted-foreground palette
- **Spacing**: Proper mt-32 for separation from main content
- **Z-index**: z-20 to appear above background effects
- **Animations**: Scale on hover, glow effects, color transitions

## Preview

The profile section appears at the bottom of the homepage with:
1. A subtle divider line above it
2. Your name and tagline
3. Three social icons that scale and glow on hover
4. A copyright notice below
5. Glassmorphic background consistent with the rest of the site

Enjoy! 🚀
