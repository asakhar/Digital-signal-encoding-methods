from PIL import Image, ImageDraw, ImageFont
from dec import decode_img
beg = 40
font = ImageFont.truetype('minreg.ttf', 10)


def polyline_vertically(draw_im, xy, color="black", width_l=1):
    for i in range(xy[0][1], xy[1][1] - 5, 7):
        draw_im.line([(xy[0][0], i), (xy[1][0], i + 2)], fill=color, width=width_l)
    draw_im.line([(xy[0][0], xy[1][1] - 2), (xy[1][0], xy[1][1])], fill=color, width=width_l)


def polyline_horizon(draw_im, xy, color='black', width1=1):
    for i in range(xy[0][0], xy[1][0] - 3, 8):
        draw_im.line([(i, xy[0][1]), (i + 3, xy[1][1])], fill=color, width=width1)


def elka(img_n, draw_n):
    polyline_horizon(draw_n, [(beg, 0), (img_n.size[0], 0)], 'red', 1)
    polyline_horizon(draw_n, [(beg + 4, 0), (img_n.size[0], 0)], 'green', 1)
    polyline_horizon(draw_n, [(beg, img_n.size[1] - 1), (img_n.size[0], img_n.size[1] - 1)], 'red', 1)
    polyline_horizon(draw_n, [(beg + 4, img_n.size[1] - 1), (img_n.size[0], img_n.size[1] - 1)], 'green', 1)


def nrz(code):
    im = Image.new('RGB', (beg + 32 * len(code), 13), color='white')
    draw_s = ImageDraw.Draw(im)
    elka(im, draw_s)
    draw_s.text((3, 1), text="NRZ", fill="black", width=1, font=font)
    point = [beg, im.size[1] - 2]
    ls = not int(('0' * (8 - len((str(bin(code[0])))[2:])) + (str(bin(code[0])))[2:])[0])
    for i in code:
        t = (str(bin(i)))[2:]
        t = '0' * (8 - len(t)) + t
        for s in t:
            if not int(s) and ls:
                draw_s.line([(point[0], point[1]), (point[0], im.size[1] - 2)], fill="black", width=1)
                point[1] = im.size[1] - 2
            elif int(s) and not ls:
                point[1] = 1
                draw_s.line([(point[0], point[1]), (point[0], im.size[1] - 2)], fill="black", width=1)

            ls = int(s)
            draw_s.line([(point[0], point[1]), (point[0] + 4, point[1])], fill="black",  width=1)
            point[0] += 4
    im.save('digital_signal.png')


def nrzi(code):
    im = Image.new('RGB', (beg + 32 * len(code) , 13), color='white')
    draw_s = ImageDraw.Draw(im)
    elka(im, draw_s)
    draw_s.text((1, 1), text="NRZI", fill="black", width=1, font=font)
    point = [beg, im.size[1] - 2]
    last_s = not int(('0' * (8 - len((str(bin(code[0])))[2:])) + (str(bin(code[0])))[2:])[0])
    sm = 0
    for i in code:
        t = (str(bin(i)))[2:]
        t = '0' * (8 - len(t)) + t
        for s in t:
            no = int(s)
            if sm:
                no = not int(s)

            if not no and last_s:
                draw_s.line([(point[0], point[1]), (point[0], im.size[1] - 2)], fill="black", width=1)
                point[1] = im.size[1] - 2
            elif no and not last_s:
                point[1] = 1
                draw_s.line([(point[0], point[1]), (point[0], im.size[1] - 2)], fill="black", width=1)

            last_s = no
            draw_s.line([(point[0], point[1]), (point[0] + 4, point[1])], fill="black", width=1)
            point[0] += 4
            if int(s):
                sm = not sm
    im.save('digital_signal.png')

def manch(code):
    im = Image.new('RGB', (beg + 64 * len(code) + 1, 13), color='white')
    draw_s = ImageDraw.Draw(im)
    elka(im, draw_s)
    draw_s.text((1, 1), text="MANCH", fill="black", width=1, font=font)
    point = [beg, im.size[1] - 2]
    for i in code:
        t = (str(bin(i)))[2:]
        t = '0' * (8 - len(t)) + t
        for s in t:
            if int(s):
                if point[1] != 1:
                    draw_s.line([(point[0], 1), (point[0], im.size[1] - 2)], fill="black", width=1)
                    point[1] = 1
                draw_s.line([(point[0], point[1]), (point[0] + 4, point[1])], fill="black", width=1)
                point[0] += 4
                draw_s.line([(point[0], point[1]), (point[0], im.size[1] - 2)], fill="black", width=1)
                point[1] = im.size[1] - 2
                draw_s.line([(point[0], point[1]), (point[0] + 4, point[1])], fill="black", width=1)
                point[0] += 4
            else:
                if point[1] != (im.size[1] - 2):
                    draw_s.line([(point[0], im.size[1] - 2), (point[0], 1)], fill="black", width=1)
                    point[1] = im.size[1] - 2
                draw_s.line([(point[0], point[1]), (point[0] + 4, point[1])], fill="black", width=1)
                point[0] += 4
                draw_s.line([(point[0], im.size[1] - 2), (point[0], 1)], fill="black", width=1)
                point[1] = 1
                draw_s.line([(point[0], point[1]), (point[0] + 4, point[1])], fill="black", width=1)
                point[0] += 4
    im.save('digital_signal.png')
    
if __name__ == '__main__':
    tk = ['NRZ', 'NRZI', 'MANCH']
    N = [i for i in range(255)]
    for tmp in tk:
        if tmp == "NRZ":
            nrz(N)
            print("Complete")
        elif tmp == "NRZI":
            nrzi(N)
            print("Complete")
        elif tmp == "MANCH":
            manch(N)
            print("Complete")
        else:
            print("Erorr")
        ng = Image.open('digital_signal.png')
        print(tmp, N == decode_img(ng, tmp))
