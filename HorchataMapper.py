from PIL import Image, ImageDraw
from HorchataUtils import generate_random_field, generate_polygon_map


field = generate_random_field(950, 200)
pols = generate_polygon_map(field)

image = Image.new("RGB", (1000, 1000))
draw = ImageDraw.Draw(image)

for pol in pols:
    draw.polygon(pol.exterior.coords)
    
image.show()