def esPrimo(num):
    ret=True
    if(isinstance(num, int)):
        if(num==1 or num==2):
            ret=True
        else:
            i=2
            while i < (int(num/2))+1:
                if((int(num%i))==0):
                    ret=False
                    #return ret
                i=i+1
    return ret

n=1
while(True):
    if(esPrimo(n)):
        print(n)
    n=n+1