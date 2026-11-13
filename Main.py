# Python is the language used for this program
# Worked on by John Lowrie, Chao Ling, Rohan Mathew, Kavion Norman, Gary Pelari
# CMP SCI 4500 Introduction to the Software Profession

# This project was started on 11/5/26
# This project was revised on 11/6/26

# validates that both sit on the same horizontal row, then shifts the image so the left most marker lands in 
# the top-left corner. Finally, it displays the original, the shifted result, and prints pixel statistics for 
# the orignal image.

# Important data structers would be 
# the pattern being searched for which is an multidimensional array of 1 and 0
# the inputed image 
# the array of 1 and 0 that represent the image 
# the matches array which is an array of tuples that have the coodiantes of found patterns

# editors used would be vs code and thonny

# sources 
# https://stackoverflow.com/questions/73757281/creating-a-grayscale-image-from-an-array-of-values making image from array 
# https://www.geeksforgeeks.org/python/python-using-2d-arrays-lists-the-right-way/ for dealing with 2d arrays and shifting them
#  Code has been borrowed from the SG1 Group 6 project



import os
from PIL import Image
import numpy as np

# ----------------------------------- IsFileValid -----------------------------------
# Makes sure inputted image is valid  
# accepts string parameter for the filename
# returns true or false for if the filename is valid
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

# ----------------------------------- ArrayToImage -----------------------------------
# Turns multidimensional array of 1 and 0 into image where 1 is white and 0 is bla
# accepts multidimensional array of 1 and 0
# returns image version of that passed in array 
def ArrayToImage(pattern):
# Get image dimensions
    height = len(pattern)
    width = len(pattern[0])

# Make empty image to fill up later
    img = Image.new("L", (width , height ))  # grayscale
    px = img.load()

# go over each value in the array and make that into a pixle in the image
    for y, row in enumerate(pattern):
        for x, val in enumerate(row):
            color = 255 if val else 0  # 1→white, 0→black
            px[x, y] = color

    return img

# ----------------------------------- ShiftUpLeft -----------------------------------
# Removes the rows and collumns of a multdimensional array as specfied with input keeps array size and fill in space with 0
# accepts the multdimensional array, and a x and y on how much to shift in the x and y directions 
# returns the multdimensional array shifted
def ShiftUpLeft(arrayToShift, x, y):
    height = len(arrayToShift)
    width = len(arrayToShift[0])

    result = []
    
# This goes over each cell in arrayToShift it get the cell + x and y right and down and appends that to a new array
# Then if the + x and y would result in being out of bounds then it appends a 0 this effectivly shiofts the array 
    for i in range(height):
        row = []
        for j in range(width):
            sourceI = i + y
            sourceJ = j + x
            if sourceI < height and sourceJ < width:
                row.append(arrayToShift[sourceI][sourceJ])
            else:
                row.append(0)
        result.append(row)
    return result



# ----------------------------------- START OF PROGRAM -----------------------------------
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

print("This program locates two patterns (a 13 by 13 cross in a box) within a 250 by 250 black and white PNG, validates that both sit on the same horizontal row, then shifts the image so the left most marker lands in the top-left corner. Finally, it displays the original, the shifted result, and prints pixel statistics for the orignal image.")
 
while(dontEndProgram):
    filename = input("Enter the name of the image file: ")
    
    if(IsFileValid(filename) == False):
        continue
    
    orignalImage = Image.open("./" + filename).convert("L")
    
    # image opening and conversion to array borrowed from the SG1 Group 6 project
    pixels = np.array(orignalImage)

# This checks if a pixle is 0 since white would be 256 so if a pixle is above 0 then it gets converted to true and 0 gets converted to false
# Then .astype(int) convets true and false to 0 and 1
    zerosAndOnes = (pixels != 0).astype(int)
    
    imageWidth, imageHeight = orignalImage.size
    patternHeight = len(pattern)
    patterWidth = len(pattern[0]) if patternHeight else 0
    matches = []
    
# image pattern checking borrowed from the SG1 Group 6 project
# This for loop checks each pixle does the pattern exist starting from there 
    for row in range(imageHeight - (patternHeight - 1)):
            for col in range(imageWidth - (patterWidth - 1)):
                section = zerosAndOnes[row:row + patternHeight, col:col + patterWidth]
    
                if np.array_equal(section, pattern):
                    matches.append((col, row))

    if(len(matches) != 2):
        print("More than 2 patterns in png" if (len(matches) > 2) else "Less than 2 patterns in png")
        continue
    
    if(matches[0][1] != matches[1][1]):
        print("Patterns are not lined up horizontally")
        continue
        
# the pattern finder gets the location of the top left pixle and that pixles value is how far its from the top left corner
    distanceFromTopLeftCornerX = matches[0][0]
    distanceFromTopLeftCornerY = matches[0][1]

    
    shifted = ShiftUpLeft(zerosAndOnes, distanceFromTopLeftCornerX, distanceFromTopLeftCornerY)
    
    orignalImage.show()
    
    ArrayToImage(shifted).show()
        
    input("Press Enter to continue...")

    
# this turns the image into an array of pixles so all the math functions we need to do is built in 
    pixels = orignalImage.get_flattened_data()
    
    minAlpha = min(pixels)
    maxAlpha = max(pixels)
    
    blackCount  = sum(1 for p in pixels if p == 0)
    whiteCount  = sum(1 for p in pixels if p == 255)
    
    avgAlpha = (whiteCount * 255) / (imageHeight * imageWidth) 
    
    print(f"Size:                {imageWidth} x {imageHeight}")
    print(f"Pixel Alpha range:   {minAlpha} - {maxAlpha}")
    print(f"Black pixels:        {blackCount}")
    print(f"White pixels:        {whiteCount}")
    print(f"Average Alpha:       {avgAlpha:.2f}")
    
    dontEndProgram = False