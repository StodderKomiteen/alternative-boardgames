import ctypes
from tkinter import PhotoImage

# def get_screen_size(out_type=str):
def get_screen_size():
    try:
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    except:
        screensize = 800, 600

    # screensize = (screensize[0], screensize[1]-100)

    return screensize

    # if out_type == str:
    #     return f"{screensize[0]}x{screensize[1]}"
    # elif out_type == tuple:
    #     return screensize
    # else:
    #     raise ValueError(f"Invalid output type: {out_type}")    

def resizeImage(img, newWidth, newHeight):
    oldWidth = img.width()
    oldHeight = img.height()
    newPhotoImage = PhotoImage(width=newWidth, height=newHeight)
    for x in range(newWidth):
        for y in range(newHeight):
            xOld = int(x*oldWidth/newWidth)
            yOld = int(y*oldHeight/newHeight)
            rgb = '#%02x%02x%02x' % img.get(xOld, yOld)
            newPhotoImage.put(rgb, (x, y))
    return newPhotoImage