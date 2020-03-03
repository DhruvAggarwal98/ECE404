#HW6
#aggarw45
#Dhruv Aggarwal
#2/3
import sys
from BitVector import* 
from PrimeGenerator import*
import numpy as np
from solve_pRoot import *

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

def read_bits(x):
    return x.read_bits_from_file(256).int_val()
def convert_text(x):
    return BitVector(intVal = x,size=256)
def calculate_cracked():
    f1 = open(sys.argv[5],"r")
    f2 = open(sys.argv[6],"w+")
    all_n = f1.readlines()
    n1 = all_n[0]
    n2 = all_n[1]
    n3 = all_n[2]
    n1 = n1.strip()
    n2 = n2.strip()
    n3 = n3.strip()
    n1_bv = BitVector(intVal= int(n1))
    n2_bv = BitVector(intVal = int(n2))
    n3_bv = BitVector(intVal= int(n3))
    mod = int(n1)*int(n2)*int(n3)
    final_n1 = mod / int(n1)
    final_n2 = mod / int(n2)
    final_n3 = mod / int(n3)
    
    final_n1_bv = BitVector(intVal = int(final_n1))
    final_n2_bv = BitVector(intVal = int(final_n2))
    final_n3_bv = BitVector(intVal = int(final_n3))
    # print(final_n1_bv,final_n2_bv,final_n3_bv)

    d1 = int(final_n1_bv.multiplicative_inverse(n1_bv))
    d2 = int(final_n2_bv.multiplicative_inverse(n2_bv))
    d3 = int(final_n3_bv.multiplicative_inverse(n3_bv))
    # print(d1,d2,d3)
    input_bv1 = BitVector(filename = sys.argv[2])
    input_bv2 = BitVector(filename = sys.argv[3])
    input_bv3 = BitVector(filename = sys.argv[4])
    while input_bv1.more_to_read and input_bv2.more_to_read and input_bv3.more_to_read:
        c1 = read_bits(input_bv1)
        c2 = read_bits(input_bv2)
        c3 = read_bits(input_bv3)

        crt = ((c1*final_n1*d1)+(c2*final_n2*d2)+(c3*final_n3*d3))
        print(crt)
        cube = solve_pRoot(3,crt)
        plaintext_bv = convert_text(cube)
        f2.write(plaintext_bv.get_bitvector_in_ascii())


if sys.argv[1] == "-c":
    calculate_cracked()