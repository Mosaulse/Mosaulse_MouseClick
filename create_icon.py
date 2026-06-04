from PIL import Image, ImageDraw

# Create a new image with transparent background
img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw mouse body (circle)
mouse_radius = 60
mouse_center = (128, 128)
draw.ellipse([mouse_center[0]-mouse_radius, mouse_center[1]-mouse_radius, 
              mouse_center[0]+mouse_radius, mouse_center[1]+mouse_radius], 
             fill=(100, 100, 100), outline=(0, 0, 0), width=2)

# Draw mouse button
button_radius = 20
draw.ellipse([mouse_center[0]-button_radius, mouse_center[1]-button_radius, 
              mouse_center[0]+button_radius, mouse_center[1]+button_radius], 
             fill=(150, 150, 150), outline=(0, 0, 0), width=1)

# Draw click effect (ripple)
for i in range(3):
    ripple_radius = button_radius + i*10
    draw.ellipse([mouse_center[0]-ripple_radius, mouse_center[1]-ripple_radius, 
                  mouse_center[0]+ripple_radius, mouse_center[1]+ripple_radius], 
                 outline=(0, 200, 0, 100), width=2)

# Save as PNG
img.save('mouse_click_icon.png')
print("Icon created successfully!")