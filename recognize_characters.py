import colorsys
import random
import sys
from PIL import Image

sys.setrecursionlimit(10000) # We don't talk about this line


def flood(x, y, found, min_x, max_x, min_y, max_y):
    # print(f"Flooding on ({x}, {y})")
    try: # Crude way of making sure pixel is not outside of image
        pixels[x, y]
    except:
        return found, min_x, max_x, min_y, max_y

    if pixels[x, y] == (0, 0, 0) and (x, y) not in found: # Found unvisited black pixel
        found.add((x, y))

        if x < min_x:
            min_x = x
        elif x > max_x:
            max_x = x

        if y < min_y:
            min_y = y
        elif y > max_y:
            max_y = y

        for x1 in range(-1, 2):
            for y1 in range(-1, 2):
                # print(f"({x}, {y}) calling:", (x + x1, y + y1))
                found, min_x, max_x, min_y, max_y = flood(x + x1, y + y1, found, min_x, max_x, min_y, max_y)

    return found, min_x, max_x, min_y, max_y


def draw_line(x1, x2, y1, y2, r, g, b):
    
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            try: # Crude way of making sure pixel is not outside of image
                pixels[x, y] = (r, g, b)
            except:
                pass


file_name = "map5.jpg"

image = Image.open(file_name)
pixels = image.load()
width, height = image.width, image.height

# Convert to black and white

for x in range(width):
    for y in range(height):
        r, g, b = pixels[x, y]
        if 0.2126*r + 0.7152*g + 0.0722*b < 255/2: 
            pixels[x, y] = (0, 0, 0)
        else:
            pixels[x, y] = (255, 255, 255)

# Drawing boxes around potential candidates

loaded_pixels = set()
rectangles = set()
for x in range(width):
    print(width - x, "x left")
    for y in range(height):
        if (x, y) in loaded_pixels or pixels[x, y] == (255, 255, 255): # Skip over looked-at pixels or white pixels
            continue

        found, min_x, max_x, min_y, max_y = flood(x, y, set(), x, x, y, y)
        x_len = max_x - min_x
        y_len = max_y - min_y

        loaded_pixels.update(found)

        if 10 < len(found) and len(found) < 500 and x_len < 30 and y_len > 5 and y_len < 30: # Is appropriate size for character
            print(f"Drawing box, {x_len} by {y_len} ==> {len(found)}")
            rectangles.add((min_x, max_x, min_y, max_y))
            h,s,l = random.random(), 0.5 + random.random()/2.0, 0.4 + random.random()/5.0
            r,g,b = [int(256*i) for i in colorsys.hls_to_rgb(h,l,s)]
            draw_line(min_x, max_x, min_y, min_y, r, g, b)
            draw_line(max_x, max_x, min_y, max_y, r, g, b)
            draw_line(min_x, max_x, max_y, max_y, r, g, b)
            draw_line(min_x, min_x, min_y, max_y, r, g, b)
       
image.show()
image.save("custom_boxes.png")

# Save & Replace Characters

def save_and_replace_char(x1, x2, y1, y2):
    padding = 3
    image2 = Image.new("RGB", (x2 - x1 + 1 + 2*padding, y2 - y1 + 1 + 2*padding), color = "white")
    pixels2 = image2.load()
    for x in range(x1 + 1, x2):
        for y in range(y1 + 1, y2):
            print(f"x: {x}, y: {y}, x1: {x1}, y1: {y1}")
            pixels2[x - x1 + padding, y - y1 + padding] = pixels[x, y]
            print("color:", pixels[x, y])
    image2.show()
    exit()

used_rectangles = set()

for rectangle in rectangles:
    used_rectangles.add(rectangle)
    if len(used_rectangles) <= 6:
        continue
    ax1, ax2, ay1, ay2 = rectangle

    overlap = False

    for rectangle2 in (rectangles - used_rectangles):
        bx1, bx2, by1, by2 = rectangle2

        if ax1 <= bx2 and ax2 >= bx1 and ay1 >= by2 and ay2 <= by1: # Rectangles overlap
            overlap = True
            area_a = (ax2 - ax1) * (ay2 - ay1)
            area_b = (bx2 - bx1) * (by2 - by1)

            if area_a < area_b:
                save_and_replace_char(ax1, ax2, ay1, ay2)
                save_and_replace_char(bx1, bx2, by1, by2)
            else:
                save_and_replace_char(bx1, bx2, by1, by2)
                save_and_replace_char(ax1, ax2, ay1, ay2)

            break

    if not overlap:
        save_and_replace_char(ax1, ax2, ay1, ay2)
                    