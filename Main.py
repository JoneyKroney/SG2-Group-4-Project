# ADD THE COMMENTS AND THE OPENING EXPLANATION TO PROGRAM


import os
from PIL import Image
import numpy as np
import math

def IsFileValid(filename):
    pngFileHeader = b'\x89PNG\r\n\x1a\n'

    path = "./" + filename
    if not filename.lower().endswith(".png"):
        print("Filename must end with '.png'")
        return False

    if not os.path.isfile(path):
        print("File does not exist")
        return False

    if os.path.getsize(path) == 0:
        print("File is empty (0 bytes)")
        return False
        
    with open(path, "rb") as file:
        header = file.read(8)
        if header != pngFileHeader:
            print("File is not a valid PNG")
            return False

    return True

def ArrayToImage(pattern, scale=1):
    h = len(pattern)
    w = len(pattern[0])

    img = Image.new("L", (w * scale, h * scale))  # grayscale
    px = img.load()

    for y, row in enumerate(pattern):
        for x, val in enumerate(row):
            color = 255 if val else 0  # 1→white, 0→black
            for dy in range(scale):
                for dx in range(scale):
                    px[x * scale + dx, y * scale + dy] = color

    return img

def ShiftUpLeft(arrayToShift, x, y):
    h = len(arrayToShift)
    w = len(arrayToShift[0])

    result = []
    for i in range(h):
        row = []
        for j in range(w):
            src_i = i + y
            src_j = j + x
            if src_i < h and src_j < w:
                row.append(arrayToShift[src_i][src_j])
            else:
                row.append(0)
        result.append(row)
    return result



dontEndProgram = True


pattern = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,0,1,1,1,1,1,0],
    [0,1,1,1,1,1,0,1,1,1,1,1,0],
    [0,1,1,1,1,1,0,1,1,1,1,1,0],
    [0,1,1,1,1,1,0,1,1,1,1,1,0],
    [0,1,1,1,1,1,0,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,0,1,1,1,1,1,0],
    [0,1,1,1,1,1,0,1,1,1,1,1,0],
    [0,1,1,1,1,1,0,1,1,1,1,1,0],
    [0,1,1,1,1,1,0,1,1,1,1,1,0],
    [0,1,1,1,1,1,0,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0]

]
 
while(dontEndProgram):
    filename = input("Enter the name of the text file: ")
    
    if(IsFileValid(filename) == False):
        continue
    
    image2 = Image.open("./" + filename).convert("L")
    
    pixels = np.array(image2)

# This checks if a pixle is 0 since white would be 256 so if a pixle is above 0 then it gets converted to true and 0 gets converted to false
# Then .astype(int) convets true and false to 0 and 1
    ZerosAndOnes = (pixels != 0).astype(int)
    
    imageHeight, imageWidth = 250, 250
    patternHeight = len(pattern)
    PatterWidth = len(pattern[0]) if patternHeight else 0
    patternCenterX, patternCenterY = math.ceil(patternHeight/2), math.ceil(PatterWidth/2)
    matches = []
    
    for row in range(imageHeight - (patternHeight - 1)):
            for col in range(imageWidth - (PatterWidth - 1)):
                section = ZerosAndOnes[row:row + patternHeight, col:col + PatterWidth]
    
                if np.array_equal(section, pattern):
                    topLeftCornerX = col 
                    topLeftCornerY = row 
                    matches.append((topLeftCornerX, topLeftCornerY))


    if(len(matches) != 2):
        print("More than 2 patterns in png" if (len(matches) > 2) else "Less than 2 patterns in png")
        continue
    
    
    if(matches[0][1] != matches[1][1]):
        print("Patterns are not lined up horizontally")
        continue
        
    distanceFromTopLeftCornerX = matches[0][0]
    distanceFromTopLeftCornerY = matches[0][1]

    
    trimmed = ShiftUpLeft(ZerosAndOnes, distanceFromTopLeftCornerX, distanceFromTopLeftCornerY)
    
    image2.show()
    
    ArrayToImage(trimmed).show()
    
    input("Press Enter to continue...")
    
    pixels = list(image2.getdata())
    
    minAlpha = min(pixels)
    maxSAlpha = max(pixels)
    
    blackCount  = sum(1 for p in pixels if p == 0)
    whiteCount  = sum(1 for p in pixels if p == 255)
    
    avgAlpha = sum(pixels) / len(pixels)
    
    print(f"Size:                {imageWidth} x {imageHeight}")
    print(f"Pixel Alpha range:   {minAlpha} - {maxSAlpha}")
    print(f"Black pixels:        {blackCount}")
    print(f"White pixels:        {whiteCount}")
    print(f"Average Alpha:       {avgAlpha:.2f}")
    
    dontEndProgram = False