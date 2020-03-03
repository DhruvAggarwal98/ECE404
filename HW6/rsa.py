#HW6
#aggarw45
#Dhruv Aggarwal
#2/3
import sys
from BitVector import* 
from PrimeGenerator import*

e = 65537
e_bv = BitVector(intVal = e)


def gcd(a,b):
    if (b == 0):
        return a
    else:
        return gcd(b,a%b)

def coprime(a,b):
    return gcd(a,b) == 1
def private_key_gen(totient_bv):
    p_key_bv = e_bv.multiplicative_inverse(totient_bv)
    return int(p_key_bv)
def encrypt(input,mod,output):
    input_bv = BitVector(filename = input)
    final_output = open(output,"w")
    
    #read 128 bits from the file
    #if its less than 128 than pad the block 
    #now that you have 128 then you pad an aditional 128 on the left because this algorithm is for 265 bit
    while input_bv.more_to_read:
        text = input_bv.read_bits_from_file(128)
        if text.length() != 128:
            text.pad_from_right(128-text.length())

        text.pad_from_left(128)
        final_text = int(text)
        new = pow(final_text,e,mod)
        cipher_block = BitVector(intVal = new,size = 256)
        final_output.write(cipher_block.get_bitvector_in_hex())
def calculation(var,var2):
    return var * int(var2)

def decrypt(mod, d,p,q):
    p_bv = BitVector(intVal = p)
    q_bv = BitVector(intVal = q)

    final_output = open(sys.argv[5],"w+")
    mi_p = p_bv.multiplicative_inverse(q_bv)
    mi_q = q_bv.multiplicative_inverse(p_bv)

    xp = calculation(q,mi_q)
    xq = calculation(p,mi_p)

    input_file = open(sys.argv[2],"r")
    string_input = input_file.read()
    input_bv = BitVector(hexstring = string_input)
    counter = 0
    while counter < (len(input_bv)/256):
        text = input_bv[(counter*256):((counter+1)*256)]
        #from his notes
        new_text = text.int_val()
        
        vp = pow(new_text,d,p)
        vq = pow(new_text,d,q)

        #chine remainder theroem 
        crt = (vp*xp + vq*xq) % mod
        final = BitVector(intVal = crt,size = 128)
        final_output.write(final.get_bitvector_in_ascii())
        counter = counter+1      

def generate():
    number = PrimeGenerator(bits = 128,debug = 0)
    flag = False
    while True:
        l = BitVector(bitstring = '11')
        p = number.findPrime()
        q = number.findPrime()
        p_bv = BitVector(intVal = p)
        q_bv = BitVector(intVal = q)

        #If the two left bits are set then keep it false otherwise make it true
        if p_bv[0:2] == l and q_bv[0:2] == l:
            flag = True
        #if the two numbers are the same than break then set the flag to true 
        if p == q:
            flag == False
        else:
            flag == True
        #check for co prime 
        
        if coprime(p-1,e) == 1 and coprime(q-1,e) == 1:
            flag = True
        
        if flag == True:
            break
        else:
            flag = False
    return p,q

if sys.argv[1] == "-g":
    p,q = generate()
    with open(sys.argv[2], 'w+') as f:
        f.write(str(p))
    with open(sys.argv[3], 'w+') as f2:
        f2.write(str(q))

if sys.argv[1] == "-e":
    f1 = open(sys.argv[3],"r")
    f2 = open(sys.argv[4],"r")
    p = int(f1.read())
    q = int(f2.read())
    mod = p * q
    encrypt(sys.argv[2],mod,sys.argv[5])

if sys.argv[1] == "-d":
    f1 = open(sys.argv[3],"r")
    f2 = open(sys.argv[4],"r")
    p = int(f1.read())
    q = int(f2.read())
    mod = q*p
    totient = (p-1)*(q-1)
    totient_bv = BitVector(intVal = totient)
    d = private_key_gen(totient_bv)
    decrypt(mod,d,p,q)