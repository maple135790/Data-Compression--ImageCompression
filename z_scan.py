from collections import deque
import os

def gld(ar,j,k):
    if k != maxE:
        k =k+1
    else:
        j =j+1    
    print(ar[j][k])
    writeBuffer.append(ar[j][k])
    while k != 0 :
        if j !=maxD:
            j =j+1
            k =k-1
        else:
            break
        print(ar[j][k])
        writeBuffer.append(ar[j][k])
    return j,k

def gur(ar,j,k):
    if j != maxD:
        j =j+1
    else:
        k =k+1
    print(ar[j][k])
    writeBuffer.append(ar[j][k])
    while j != 0:
        if k !=maxE:
            j =j-1
            k =k+1
        else:
            break
        print(ar[j][k])
        writeBuffer.append(ar[j][k])
    if ar[j][k] == ar[-2][-1]:
        j =-1
        k =-1
        print(ar[-1][-1])
        writeBuffer.append(ar[-1][-1])
    return j,k

def wfile(wbuf,filename):
    with open(filename,"a") as fw:
        for i in range(len(wbuf)-1):
            fw.write(str(wbuf.popleft())+" ")
    wbuf.clear()
    a

if __name__ == "__main__":
    mat_a =[[65,75,60,50,51],[170,188,150,250,511],[1,2,3,5,4]]
    
    j =0
    k =0
    writeBuffer =deque([])
    exit_flag =False
    totalE =len(mat_a) * len(mat_a[0])
    maxE =len(mat_a[0])-1       #number of elements in each dimension
    maxD =len(mat_a)-1          #number of dimension in given matrix
    print(mat_a[0][0])
    writeBuffer.append(mat_a[0][0])
    filename ="out.txt"
    if os.path.exists(filename):
        os.remove(filename)
    open(filename, "x")
    while exit_flag !=True:
        try :
            '''Going left & down '''
            j,k =gld(mat_a,j,k)
            '''Going up & right'''
            j,k =gur(mat_a,j,k)
            if len(writeBuffer) >=256:
                wfile(writeBuffer,filename)
            if mat_a[j][k] == mat_a[-1][-1]:
                writeBuffer.append(mat_a[-1][-1])
                wfile(writeBuffer,filename)
                exit_flag =True
        except IndexError:
            pass
    