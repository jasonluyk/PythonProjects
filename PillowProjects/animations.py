import os
from PIL import Image

folder_path = 'resources/animation'
# Sort first to fix the "random" order
files = sorted([f for f in os.listdir(folder_path) if f.endswith('.png')])

# Create the list of UNIQUE objects
images = [Image.open(os.path.join(folder_path, name)) for name in files]

# Double check the length matches your folder count
print(f"Loaded {len(images)} unique frames.")

# Save
images[0].save('animation.gif', append_images=images[1:], save_all=True, duration=150, loop=1)