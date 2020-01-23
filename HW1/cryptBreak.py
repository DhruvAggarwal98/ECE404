import sys
from BitVector import *  

def cryptBreak(ciphertextFile,key_bv):
	BLOCKSIZE = 16
	numbytes = BLOCKSIZE // 8
	PassPhrase = "Hopes and dreams of a million years" 
	bv_iv = BitVector(bitlist = [0]*BLOCKSIZE)
	for i in range(0,len(PassPhrase) // numbytes):
		textstr = PassPhrase[i*numbytes:(i+1)*numbytes]
		bv_iv ^= BitVector( textstring = textstr ) 
	file = open(ciphertextFile,"r")
	en_code= file.read().strip()
	encrypted_bv = BitVector( hexstring = en_code)
	
	for key in range(25000,26000):
		key_bv = BitVector(intVal = key,size = 16)
		msg_decrypted_bv = BitVector (size = 0)
		previous_decrypted_block = bv_iv
		for i in range(0, len(encrypted_bv) // BLOCKSIZE):
			bv = encrypted_bv[i*BLOCKSIZE:(i+1)*BLOCKSIZE]
			temp = bv.deep_copy()
			bv ^=  previous_decrypted_block
			previous_decrypted_block = temp
			bv ^=  key_bv
			msg_decrypted_bv += bv
		if 'Mark Twain' in msg_decrypted_bv.get_text_from_bitvector():
			return str(msg_decrypted_bv.get_text_from_bitvector())

	

if __name__ == '__main__':

	final = cryptBreak("/Users/DhruvMac/Documents/College/GitHub/ECE404/HW1/cipher.txt",2)
	print(final)
