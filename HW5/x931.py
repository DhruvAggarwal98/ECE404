#HW5
#Dhruv Aggarwal
#aggarw45
#2/25/20
from BitVector import *
from Crypto.Cipher import AES
import base64

def x931(v0, dt, totalNum, key_file):
    final_list = []
    #read input
    with open(key_file) as f:
        key_plaintext = f.read()
    b = bytes(key_plaintext, 'utf-8')
    cipher = AES.new(b, AES.MODE_ECB)
    #create my first block
    first = base64.b64encode(cipher.encrypt(bytes(dt)))
    new_bv = BitVector(rawbytes = first)
    #keep xor ing by using x r v0 and dt again not sure what im doing wrong
    for each in range(totalNum):
        X = new_bv^v0
        R = base64.b64encode(cipher.encrypt(bytes(X)))
        R = BitVector(rawbytes= R)
        final_list.append(int(R.get_bitvector_in_hex(),16))
        v0 = R ^ dt
        v0 = base64.b64encode(cipher.encrypt(bytes(v0)))
        v0 = BitVector(rawbytes= v0)
        break
    print(final_list)
        #     v0 = base64.b64encode(cipher.encrypt(bytes(v0)))


if __name__ == "__main__":
   
    dt = BitVector(intVal=99, size=128)
    v0 = BitVector(textstring='computersecurity')
    totalNum = 3
    key_file = 'keyX931.txt'
    x931(v0,dt,totalNum,key_file)


