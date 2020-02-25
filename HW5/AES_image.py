#HW5
#DhruvAggarwal
#aggarw45 
#2/25/20

from BitVector import *
from Crypto.Cipher import AES
import base64

def ctr_aes_image(iv,image_file,out_file,key_file):
    #open file
    with open(key_file) as f:
        key_plaintext = f.read()
    b = bytes(key_plaintext, 'utf-8')
    final_output = open(out_file,"wb")
    test_file = open("test.ppm","wb")
    #open test file
    #use professors code to create a cipher block
    cipher = AES.new(b, AES.MODE_ECB)
    with open(image_file,"rb+") as whole:
        entire=whole.readlines()[0:3]
        final_output.writelines(entire[0:3])
    with open(image_file,"rb+") as whole:
        non_header = whole.readlines()[3::]
        test_file.writelines(non_header)
        #create a bit vector
    bv = BitVector(filename = 'test.ppm')
    #start badding
    while (bv.more_to_read):
        iv_bv = BitVector(intVal = iv) 
        bitvec = iv_bv.read_bits_from_file(128)
        if bitvec.length() > 0:
            if bitvec.length() < 128:
                bitvec.pad_from_right(128-bitvec.length())
        block = base64.b64encode(cipher.encrypt(bytes(iv)))
        #take ur current block and then xor and then increase iv 
        #not sure what im doing wrong
        new_bv = BitVector(rawbytes = block)
        new = new_bv ^ bitvec 
        new.write_to_file(final_output)
        iv= iv + 1

if __name__ == "__main__":
    iv = BitVector(textstring='computersecurity')
    ctr_aes_image(iv,'image.ppm','enc_image.ppm','keyCTR.txt')
    
