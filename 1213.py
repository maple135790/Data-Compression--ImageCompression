from PIL import Image
import numpy as np

im = Image.open("sample01.bmp")
mata= [[64,2,3,61,60,0,7,57]]
matb= np.asfarray(mata)

for n in range(len(mata)):
    for m,i in range(len(mata[n])-1):
        matb[n,m]= (mata[n][m]+mata[n][m+1])/2
        m+=1
print(matb)