
'''
# n-level quantumlizer
def qzr(seq):
    ul =max(seq)
    dl =min(seq)
    c =len(seq)
    ul
'''

def dn1(seq):
    dseq1 =[None]*len(seq)
    for i in range(len(seq)):
        if i ==0:
            dseq1[0] =seq[0]
        else:
            dseq1[i] =round(seq[i]-seq[i-1],1)
    print(dseq1)

if __name__ =="__main__":
    seq =[6.2,9.7,13.2,5.9,8,7.4,4.2,1.8]
    dn1(seq)