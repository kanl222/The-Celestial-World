from PIL import Image

im = Image.open("burning_loop_1.png")
pixels = im.load()  # список с пикселями
x, y = im.size  # ширина (x) и высота (y) изображения


def Cutting(frame:int,number:int):
    for i in range(frame):
        if i!=frame:
            im.crop(box=(x/frame*i, 0, x/frame*(i+1)-1, y)).save('{}.png'.format(str(i+number)))


Cutting(8,5)