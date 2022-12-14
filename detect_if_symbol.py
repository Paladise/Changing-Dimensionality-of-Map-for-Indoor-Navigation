import cv2 as cv
import numpy as np
from drawing import create_image_from_box
from image_similarity_measures.quality_metrics import rmse
from PIL import Image
from random import choice, random, sample


def detect_if_symbol(pixels, thresholds, x1, x2, y1, y2):
    """
    Given box of potential symbol, determine whether that image
    is indeed a symbol and return which symbol it is (according to key, if given one)
    
    Currently uses root mean squared as an image similarity measure
    """

    test_image = create_image_from_box(pixels, x1, x2, y1, y2, 0)
    width, height = test_image.size

    for symbol in thresholds.keys():
        key_image = cv.imread("images/" + symbol + ".png")
        key_width, key_height = key_image.shape[1], key_image.shape[0]

        left = round((width - key_width)/2)
        top = round((height - key_height)/2)
        x_right = round(width - key_width) - left
        x_bottom = round(height - key_height) - top
        right = width - x_right
        bottom = height - x_bottom

        # Crop the center of the image
        test_image = test_image.crop((left, top, right, bottom))

        test_cv_image = cv.cvtColor(np.array(test_image), cv.COLOR_GRAY2RGB)
#         test_image = cv.resize(test_image, (key_image.size[0], key_image.size[1]), interpolation = cv.INTER_AREA)

        m = rmse(key_image, test_cv_image).item()

        if m < thresholds[symbol]:
            return symbol

    return ""


def get_similarity_thresholds(symbols = ["door", "stairs", "signage"]):
    """
    Given possible symbols, construct possible thresholds for similarity images
    by creating several distorted images and comparing their rmses, then returning a dictionary of
    symbols and their threshold values
    """
    
    def inside(x, y):
        if x > 0 and x < w - 1 and y > 0 and y < h - 1:
            return True
        else:
            return False
    
    thresholds = {}

    for symbol in symbols:

        print("Looking at symbol:", symbol)

        avg = []
        for _ in range(25):

            image = Image.open(f"images/{symbol}.png").convert("RGB")
            pixels = image.load()
            w, h = image.size[0], image.size[1]
            image = create_image_from_box(pixels, 0, w, 0, h, 1).convert("RGB")
    #         print_image_with_ascii(image.convert("L"), border = True)

            data = np.array(image)
            data[(data == (0, 0, 0)).all(axis = -1)] = (255, 0, 0)
            img = Image.fromarray(data, mode='RGB')

            temp = choice([(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)])
            c, f = temp[0], temp[1]


            a = 1
            b = 0
    #         c = 1 #left/right (i.e. 5/-5)
            d = 0
            e = 1
    #         f = 0 #up/down (i.e. 5/-5)
            img = img.transform(img.size, Image.Transform.AFFINE, (a, b, c, d, e, f))

            data = np.array(img)
            data[(data == (0, 0, 0)).all(axis = -1)] = (255, 255, 255)
            img = Image.fromarray(data, mode='RGB')

            data = np.array(img)
            data[(data == (255, 0, 0)).all(axis = -1)] = (0, 0, 0)
            image = Image.fromarray(data, mode='RGB')

            pixels = image.load()
            w, h = image.size[0], image.size[1]


            empty, not_empty = [], []

            for x in range(w):
                for y in range(h):
                    if pixels[x, y] == (255, 255, 255):
                        if any(pixels[x + x3, y + y3] == (0, 0, 0) for x3 in range(-1, 2) for y3 in range(-1, 2) if inside(x + x3, y + y3)):
                            empty.append((x, y))
                    else:
                        if any(pixels[x + x3, y + y3] == (255, 255, 255) for x3 in range(-1, 2) for y3 in range(-1, 2) if inside(x + x3, y + y3)):
                            not_empty.append((x, y))

            num = choice(range(15, 25))
            num2 = 0
            if num > 1:
                num2 = choice([i for i in range(num - 1)])
            num -= num2

            image2 = image.copy()
            pixels2 = image2.load()

            num = min(num, len(empty))

            for e in sample(empty, num):            
                x, y = e
                pixels2[x, y] = (0, 0, 0)

            num2 = min(num2, len(not_empty))

            for e in sample(not_empty, num2):
                x, y = e
                pixels2[x, y] = (255, 255, 255)

            m = round(rmse(cv.cvtColor(np.array(image.convert("L")), cv.COLOR_GRAY2RGB), cv.cvtColor(np.array(image2.convert("L")), cv.COLOR_GRAY2RGB)).item(), 4)

    #         print_image_with_ascii(image2.convert("L"), border = True)        
    #         print(m)
    #         print("Symbol:", symbol)
    #         print(num, num2)        
    #         input()
            avg.append(m)

        threshold = sum(avg) / len(avg)


        thresholds[symbol] = threshold
        
    print("Thresholds:", thresholds)
    return thresholds