from PIL import Image
import numpy as np
import math
from math import sin,cos,degrees

mat_a =[[65,75,60,70,56,80,68,50,40,50,69,62,76,64],[170,188,150,170,130,203,160,110,80,153,148,140,164,120]]

if __name__ == "__main__":
        im = Image.open("sample01.bmp")
        mata= np.asarray(im)
        mata.setflags(write=1)
        maxq= np.amax(mata)
        minq= np.amin(mata)
        q_set= set()
        im.show()
        print(mata,end='\n\n')
        print(maxq)
        print(minq)
        
        intter= math.floor((maxq-minq)/4)
        print(intter)
        for n in range(len(mata)):
                for m in range(len(mata[n])):
                        for i in np.nditer(mata[n][m]):
                                if i <= intter:
                                        i = intter
                                elif i > intter and i <= 2*intter:
                                        i = 2*intter
                                elif i > 2*intter and i <= 3*intter:
                                        i = 3*intter
                                elif i > 3*intter:
                                        i = 4*intter
                                mata[n,m] =math.floor(i)
                                q_set.add(i)
        print(mata)
        print(q_set)
        Image.fromarray(mata).save("test.bmp")
        '''
        phi =math.atan(2.5)
        mat_b =[[cos(phi),sin(phi)],[sin(phi),cos(phi)*(-1)]]
        '''
        '''for i in range(len(mat_a[0])):
                for j in range(len(mat_a)):
                        p =(mat_a[j][i],mat_a[j+1][i])
                        x =p[0]
                        y =0
                        np.sqrt(np.sum(np.square(x-y)))
                        break
        '''
        """im.show()"""
    
