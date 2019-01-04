import os
from PIL import Image
from numpy import asarray
from collections import deque

def wfile(wbuf,filename):
    size =wbuf.__len__()
    with open(filename,"a") as fw:
        for _ in range(wbuf.__len__()-1):
            fw.write(str(wbuf.popleft())+" ")
    wbuf.clear()
    return size

def bufferWrite(currentBufferSize,buffer,filename,array,j,k):   
    currentBufferSize =0
    if buffer.__len__() ==256:
        buffer.append(array[j][k])
        currentBufferSize =wfile(buffer,filename)
    else:
        buffer.append(array[j][k])
    return currentBufferSize
    
def gld(ar,j,k,writeBufferSize):   # Go left and down
    if k != maxE:
        k =k+1
    else:
        j =j+1    
    writeBufferSize +=bufferWrite(writeBufferSize,writeBuffer,filename,ar,j,k)
    while k != 0 :
        if j !=maxD:
            j =j+1
            k =k-1
        else:
            break
        writeBufferSize +=bufferWrite(writeBufferSize,writeBuffer,filename,ar,j,k)
    return j,k,writeBufferSize

def gur(ar,j,k,writeBufferSize):   # Go up and right
    if j != maxD:
        j =j+1
    else:
        k =k+1
    writeBufferSize +=bufferWrite(writeBufferSize,writeBuffer,filename,ar,j,k)
    if (j,k) != (maxD,maxE):
        while j != 0:
            if k !=maxE:    
                j =j-1
                k =k+1
            else:
                break
            writeBufferSize +=bufferWrite(writeBufferSize,writeBuffer,filename,ar,j,k)
    else:
        pass
    return j,k,writeBufferSize

if __name__ == "__main__":
    #mat_a =[[65,75,60,50,51],[170,188,150,250,511],[1,2,3,5,4]]
    j =0
    k =0
    im =Image.open("sample_128.bmp")
    mat_a =asarray(im)
    writeBuffer =deque([])
    exit_flag =False
    writeBufferSize =0
    totalE =len(mat_a) * len(mat_a[0])
    maxE =len(mat_a[0])-1       #number of elements in each dimension (Count in python-list)
    maxD =len(mat_a)-1          #number of dimension in given matrix (Count in python-list)
    writeBuffer.append(mat_a[0][0])
    filename ="out.txt"

    if os.path.exists(filename):
        os.remove(filename)
    open(filename, "x")
    while exit_flag !=True:
        try :
            '''Going left & down '''
            j,k,writeBufferSize =gld(mat_a,j,k,writeBufferSize)
            '''Going up & right'''
            j,k,writeBufferSize =gur(mat_a,j,k,writeBufferSize)
            if (j,k) == (maxD,maxE):
                writeBuffer.append(mat_a[-1][-1])
                writeBufferSize +=wfile(writeBuffer,filename)
                exit_flag =True
        except IndexError:
            pass
    #print(mat_a)
    print("Elements of image: "+str(writeBufferSize-1))    
    print("image size: "+str(totalE))