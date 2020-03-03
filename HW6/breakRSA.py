#HW6
#aggarw45
#Dhruv Aggarwal
#2/3
import sys
from BitVector import* 
from PrimeGenerator import*
import numpy as np


e = 3

def gcd(a,b):
    if (b == 0):
        return a
    else:
        return gcd(b,a%b)

def coprime(a,b):
    return gcd(a,b) == 1

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

if sys.argv[1] == "-e":
    p1,q1 = generate()
    p2,q2 = generate()
    p3, q3 = generate()
    n1 = p1*q1
    n2 = p2*q2
    n3 = p3*q3
    
    three_output = open(sys.argv[6],"w+")
    
    three_output.write(str(n1))
    three_output.write("\n")
    three_output.write(str(n2))
    three_output.write("\n")
    three_output.write(str(n3))
    
    encrypt(sys.argv[2],n1,sys.argv[3])
    encrypt(sys.argv[2],n2,sys.argv[4])
    encrypt(sys.argv[2],n3,sys.argv[5])