import z_scan
from PIL import Image
from numpy import asarray
from collections import deque

def wfile(wbuf,filename):
    size =wbuf.__len__()
    with open(filename,"a") as fw:
        for i in range(len(wbuf)-2):
            fw.write(str(wbuf.popleft())+" ")
    wbuf.clear()
    return size

#def writeFile(filename,imageArray):
if __name__ =="__main__":
    filename ="test.txt"
    im =Image.open("sample02.bmp")
    imageArray =asarray(im)
    writeBuffer =deque([])
    size =0
    totalE =len(imageArray) * len(imageArray[0])

    for i in range(len(imageArray)):
        for j in range(len(imageArray[0])):
            writeBuffer.append(imageArray[i][j])
            if len(writeBuffer)>=256:
                size +=wfile(writeBuffer,filename)
    size +=wfile(writeBuffer,filename)
       
    print("buffer total size: "+str(size))
    print("picture total size: "+str(totalE))
    