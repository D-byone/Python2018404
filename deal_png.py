# -*- coding:utf-8 -*-
# from PIL import Image


from PIL import Image

# 打开要处理的图像
img_src = Image.open('123.png')

# 转换图片的模式为RGBA
img_src = img_src.convert('RGBA')

# 获得文字图片的每个像素点
src_strlist = img_src.load()

print src_strlist
print img_src.load()

# 100,100 是像素点的坐标
# data = src_strlist[1,1]
# 结果data是一个元组包含这个像素点的颜色信息    栗子：(0, 0, 0, 255)


for i in range(0,img_src.size[0]):
    for j in range(0,img_src.size[1]):
        data = src_strlist[i,j]
        print "----" , data
        if data[3] == 0:
            img_src.putpixel((i,j),(data[0],data[1],data[2],255))
        #     pass
        # else:
        #     img_src.putpixel((i,j),(135,206,255,255))
        #     pass
        print src_strlist[i,j]

print img_src.size  #图片的尺寸
print img_src.mode  #图片的模式
print img_src.format  #图片的格式
img_src.show()


img_src.save('123.png')