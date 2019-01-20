import os
import numpy as np
from PIL import Image
from numpy import asarray
from collections import deque
from os import path as op
import hashlib

def LZW_decode(r_Dict):
    if os.path.exists("dec.txt"):
        os.remove("dec.txt")    
    with open("cpf.bin","rb") as df:
        erw =df.read()
        #print("\nCompressed :"+str(erw),end='\n\n')
        #print("Compressed Length :"+str(len(erw)))
        b =0
        #r_Dict = {bytes([i]): chr(i) for i in range(128)}
        write_stream =deque([])
        o_Dict =r_Dict.copy()
        cw =erw[0:1]
        write_stream.append(str(r_Dict.get(cw)))
        while b != len(erw)-1:           
            #current_word =erw[b:j]
            if len(r_Dict) ==256:
                r_Dict =o_Dict.copy()
            if write_stream.__len__() ==256:
                with open("dec.txt","a") as sf:
                    while write_stream.__len__() !=0:
                        sf.write(write_stream.popleft())
            b +=1
            pw =cw
            cw =erw[b:b+1]
            if cw in r_Dict:
                write_stream.append(str(r_Dict[cw]))
                r_Dict[bytes([len(r_Dict)])] =r_Dict[pw]+r_Dict[cw][0:1]
            else:
                r_Dict[bytes([len(r_Dict)])] =r_Dict[pw]+r_Dict[(list(r_Dict.keys())[-1])][-1]
                write_stream.append(r_Dict[(list(r_Dict.keys())[-1])])
        #print("Decode :"+write_stream,end='\n')
        with open("dec.txt","a") as sf:
            while write_stream.__len__() !=0:
                sf.write(write_stream.popleft())
    return erw

def LZW_plainText(Dict,stre):
    b =0
    o_asciiDict =Dict.copy()
    current_word =stre[0]
    write_stream =bytes()
    for j in range(len(stre)):
        current_word =stre[b:j+1]
        if len(Dict) ==256:
            Dict =o_asciiDict.copy()
        while current_word not in Dict:   # Add words that's not in the Dict
            write_stream +=bytes(Dict.get(stre[b:j]))
            Dict[current_word] =bytes([len(Dict)]) 
            b =j
        if j ==len(stre)-1:
            write_stream +=bytes(Dict.get(current_word))
            #Dict[current_word] =bytes([len(Dict)])
            break 
    fw =open("cpf.bin",'wb')
    '''aw =bytes(write_stream,"ascii")'''
    fw.write(bytes(write_stream))
    fw.close()
    return

def qzr(array):  # 8-level simple quantizer
    #cArray =[[None]*(maxE+1)]*(maxD+1)
    cArray =np.zeros((maxD+1,maxE+1),dtype= int)
    decDict =dict()
    maxq =np.amax(array)
    minq =np.amin(array)
    level =4
    ival =int((maxq-minq)/level)
    for n in range(len(array)):  # Long and stink, don't open
        for m in range(len(array[0])):
            #for i in np.nditer(array[n][m]):
            i =array[n][m]
            if i <= ival:
                i = ival
            elif i > ival and i <= 2*ival:
                i = ival*2
            elif i > 2*ival and i <= 3*ival:
                i = ival*3
            else:
            #elif i > 3*ival and i <= 4*ival:
                i = ival*4
            '''    
            elif i > 4*ival and i <= 5*ival:
                i = ival*5   
            elif i > 5*ival and i <= 6*ival:
                i = ival*6
            elif i > 6*ival and i <= 7*ival:
                i = ival*7
            elif i > 7*ival:
                i = ival*8
            '''
            cArray[n][m] =int(np.floor(i)) 
    for i in range(0,4):
        decw =np.binary_repr(i, width= 2)
        decw =bytes(decw,"ascii")
        decDict[bytes([int(np.floor(ival*(i+1)))])] =decw
    return cArray,decDict

def wfile(wbuf,decodeDict,filename):
    size =wbuf.__len__()
    with open(filename,"ab") as fw:
        for _ in range(wbuf.__len__()-1):
            a =wbuf.popleft()
            fw.write(decodeDict[a])          
    wbuf.clear()
    return size

def bufferWrite(currentBufferSize,buffer,filename,array,j,k):   
    currentBufferSize =0
    if buffer.__len__() ==256:
        buffer.append(bytes([mat_a[j][k].astype("int_")]))
        currentBufferSize =wfile(buffer,decDict,filename)
    else:
        buffer.append(bytes([mat_a[j][k].astype("int_")]))
    return currentBufferSize

'''
def haar(array): # Haar function
    t =np.log2(maxD)
    r =np.ceil(maxE/2)
    for i in range(maxD):
        for j in range(0,maxE,2):
            try:
                avg =(array[i][j]+array[i][j+1])/2
                dif =(array[i][j]-array[i][j+1])/2
            except IndexError :
                avg =(array[i][j]+0)/2
                dif =avg
            array[i][r] =avg
            array[]
    return 1
'''
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

def gld_d(i,ar,j,k,Dict,decw,a,b):   # Go left and down
    
    if k != maxE:
        k =k+1
    else:
        j =j+1
    ar[j][k] =Dict.get(decw[a:b+i])
    while k != 0 :
        if j !=maxD:
            j =j+1
            k =k-1
            a =b+i
            b =b+i
        else:
            break
        ar[j][k] =Dict.get(decw[a:b+i])
    return j,k

def gur_d(i,ar,j,k,Dict,decw,a,b):   # Go up and right
    
    if j != maxD:
        j =j+1
    else:
        k =k+1
    ar[j][k] =Dict.get(decw[a:b+i])
    if (j,k) != (maxD,maxE):
        while j != 0:
            if k !=maxE:
                j =j-1
                k =k+1
                a =b+i
                b =b+i
            else:
                break
            ar[j][k] =Dict.get(decw[a:b+i])
    else:
        pass
    return j,k

def decFile():
    with open("dec.txt","r") as da:
        a =0
        b =0
        i =1
        j =0
        k =0
        exit_flag =False
        unfilled =da.read()
        r_decDict ={j.decode("ascii"):int.from_bytes(k,byteorder='big') for k, j in decDict.items()}
        pArray =np.zeros((maxD+1,maxE+1),dtype=int)
        pArray[0][0] =r_decDict[unfilled[0:2]]
        while exit_flag != True:
            if unfilled[a:b+i] in r_decDict:
                b =b+i
                a =b
                j,k =gld_d(i,pArray,j,k,r_decDict,unfilled,a,b)
                j,k =gur_d(i,pArray,j,k,r_decDict,unfilled,a,b)
                
                #i =1
                if (j,k) == (maxD,maxE):
                    pArray[maxD][maxE] =r_decDict[unfilled[totalE:totalE+2]]
                    exit_flag =True
            else:
                i +=1
    return pArray

if __name__ == "__main__":
    j =0
    k =0
    filename ="out.txt"
    imageName ="sample02.bmp"
    im =Image.open(imageName) 
    mat_a =asarray(im)
    dim =mat_a.ndim
    original_a =mat_a
    writeBuffer =deque([])
    exit_flag =False
    writeBufferSize =0
    
    if dim == 2:
        totalE =len(mat_a) * len(mat_a[0])
        maxE =len(mat_a[0])-1       #number of elements in each dimension (Count in python-list)
        maxD =len(mat_a)-1          #number of dimension in given matrix (Count in python-list)
    else:
        totalE =len(mat_a[0]) * len(mat_a[0][0])
        maxE =len(mat_a[0][0])-1       #number of elements in each dimension (Count in python-list)
        maxD =len(mat_a[0])-1
    binaryDict ={'0':bytes([0]),'1':bytes([1])}
    r_binaryDict ={bytes([0]):'0',bytes([1]):'1'}

    mat_a,decDict =qzr(mat_a) # Quantilize image first
    mat_a =asarray(mat_a,dtype=np.unicode_)
    writeBuffer.append(bytes([mat_a[0][0].astype("int_")]))
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
                writeBuffer.append(bytes([mat_a[-1][-1].astype("int_")]))
                writeBufferSize +=wfile(writeBuffer,decDict,filename)
                exit_flag =True
        except IndexError:
            pass
    print("Elements of image: "+str(writeBufferSize-1))    
    print("image size: "+str(totalE))
    
    f =open(filename,"r")
    stre =f.read()
    LZW_plainText(binaryDict,stre)
    c_len =LZW_decode(r_binaryDict)
    print("Compressed Ratio :"+str(op.getsize(imageName)/op.getsize("cpf.bin")))
    clonePicArray =decFile()
    matb =asarray(mat_a,dtype=np.float)
    im1 =Image.fromarray(matb)
    im1_L =im1.convert("L")
    im1_L.save("test.bmp")
    im1_L.show()
    mse = np.sum((original_a.astype("float") - matb) ** 2)
    mse /= float(original_a.shape[0] * original_a.shape[1])
    print(mse)
