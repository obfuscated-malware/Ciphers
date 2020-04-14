#<Ankush Jain, 116806909>
from bitstring import BitArray
# We previously showed how to extract the bits from 6bit blocks and find the row and column indices for
# use in the s-box operation. Each S-box can be represented as a list of lists to allow row-column access
# and we can put all s-boxes in a parent list SBOX for easy addressing. Remember that Sbox-1 is SBOX[0]
# and sbox-2 is SBOX[1] and sbox-8 is SBOX[7]

SBOX = [
	[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
	 [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
	 [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
	 [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
	],
	
	[[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
	 [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
	 [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
	 [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
	],
	
	[[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
	 [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
	 [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
	 [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
	],
	
	[[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
	 [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
	 [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
	 [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
	],  
	
	[[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
	 [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
	 [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
	 [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
	], 
	
	[[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
	 [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
	 [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
	 [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
	], 
	
	[[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
	 [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
	 [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
	 [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
	],
	   
	[[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
	 [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
	 [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
	 [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
	]
	]
# Let's define a table for quick conversion of sbox decimals to 4 bit binary
DECtoBIN4 = {0: '0000',
            1: '0001',
            2: '0010',
            3: '0011',
            4: '0100',
            5: '0101',
            6: '0110',
            7: '0111',
            8: '1000',
            9: '1001',
            10: '1010',
            11: '1011',
            12: '1100',
            13: '1101',
            14: '1110',
            15: '1111'}

#print(DECtoBIN4[12])

# we can now implement the sbox operations by combining the above material


def sbox_lookup(input6bitstr, sboxindex):
    # find the row index (0-3)
    # find the col index (0-7)
    #print("input6bitstrinsbox: ",input6bitstr)
    #print("Sboxindex: ",sboxindex)
    row = int(input6bitstr[0]+input6bitstr[5],base=2)
    col = int(input6bitstr[1:5],base=2)
    sbox_value = SBOX[sboxindex][row][col]
    #print(row,col)
    #print(DECtoBIN4[sbox_value])
    # Need to convert to 4 bits binary string
    return DECtoBIN4[sbox_value]

# Initial Permutation and inverse permutaion operatoins can be easily performed 
# using lists and proper indexing of the elements of the lists in Python 

# Let's define the order of the elements at the output of the Initial Permutation (IP) stage
# in the following list (we subtract the values in the book by 1 since we always
# index array elements from 0 upward) 
BookInitPermOrder = [58,50,42,34,26,18,10,2,
                   60,52,44,36,28,20,12,4,
                   62,54,46,38,30,22,14,6,
                   64,56,48,40,32,24,16,8,
                   57,49,41,33,25,17,9,1,
                   59,51,43,35,27,19,11,3,
                   61,53,45,37,29,21,13,5,
                   63,55,47,39,31,23,15,7]

BookPermOrderkey = [57,49,41,33,25,17,9,
                    1,58,50,42,34,26,18,
                    10,2,59,51,43,35,27,
                    19,11,3,60,52,44,36,
                    63,55,47,39,31,23,15,
                    7,62,54,46,38,30,22,
                    14,6,61,53,45,37,29,
                    21,13,5,28,20,12,4]

BookpermOrderkeych2 = [14,17,11,24,1,5,3,28,
                        15,6,21,10,23,19,12,4,
                        26,8,16,7,27,20,13,2,
                        41,52,31,37,47,55,30,40,
                        51,45,33,48,44,49,39,56,
                        34,53,46,42,50,36,29,32]

shift = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

PI_1 = [40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25]



# EXPANSION (E)
# The E operation involves inserting additional bits inside the input 32 bits sequence
# We can start with an empty output bit string and then take proper bits from the input 
# according to the E_TABLE below and add the bits one by one to the end of the output
# string

E_TABLE = [32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,
16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,28,29,30,31,32,1]

etable2 = [a-1 for a in E_TABLE]

def Expansion(inputbitstr32, e_table):
    # the input string is 32 bits long and the output string will be 48 bits long or
    # to be more exact, it will be as long as the e_table (which is 48 bits for DES)
    
    # create output empty string
    outputbitstr48 = ''
    for u in e_table:
        outputbitstr48 = outputbitstr48 + inputbitstr32[u]


    # add proper elements from the inputbitstr32 according to the e_table
    
    return outputbitstr48


def functionF(bitstr32, keybitstr48):
    outbitstr32 = ''
    expandedrbit = Expansion(bitstr32,etable2)
    #print("expandedrbit: ",expandedrbit)
    firstxorbit = XORbits(expandedrbit,keybitstr48)
    #print("xor key and right: ",firstxorbit)
    bitfirstxor6 = [firstxorbit[i:i+6] for i in range(0,len(firstxorbit), 6)]
    #print("6bitfirstxor: ", bitfirstxor6)
    sbox_out=''
    for n in range(len(bitfirstxor6)):
        sbox_out=sbox_out+sbox_lookup(bitfirstxor6[n],n)
    #print("Sboxout: ",sbox_out)
    outbitstr32 = Permutation(sbox_out,P)
    #print("Outbitstr32: ",outbitstr32)
    # return the result
    return outbitstr32


def XORbits(bitstr1,bitstr2):
    xor_result = None
    xorbit = int(bitstr1,2) ^ int(bitstr2,2)
    xor_result = bin(xorbit)[2:].zfill(len(bitstr1))
    #print("XORresult: ",xor_result)
    # Both bit strings should be the same length
    # output will be a string with the same length
    
    
    return xor_result

# Permutation (P)
# the P operation is exactly like the permutation operation we perfomred before for initial permutation (IP)
# and the Permutation function we implemented before can be used here as well

def Permutation(bitstr, permorderlist):
    permedbitstr = ""
    for i in permorderlist:
        permedbitstr = permedbitstr + bitstr[i-1]
       
    #....
    return permedbitstr

def des_keygen(C_inp, D_inp, roundindex):
    bits = shift[roundindex]
    # Implement Figure 6
    C_out = C_inp[bits:] + C_inp[:bits]
    D_out = D_inp[bits:] + D_inp[:bits]
    inputtopermcond2 = C_out+D_out
    key_48 = []
    if inputtopermcond2 != "":
        key_48 = Permutation(inputtopermcond2,BookpermOrderkeych2)
    #key48 = "".join(key_48)
    #print ("key48: ",key_48)
    return key_48, C_out, D_out
 
def des_round(LE_inp32, RE_inp32, key48):
    outofFuncF = functionF(RE_inp32,key48)
    #print("outofFuncF: ",outofFuncF)
    RE_out32 = XORbits(LE_inp32,outofFuncF)
    LE_out32 = RE_inp32
    
    # LEinp and REinp are the outputs of the previous round
    # k is the key for this round which usually has a different 
    # value for different rounds
    #print("LE_out32: ",LE_out32)
    #print("RE_out32: ",RE_out32)
    #print("----------------------------------------------------------------------------------")
    return LE_out32, RE_out32

    # even though DES is strictly 16 rounds, we keep the number of rounds as a parameter for
    # easier extension and also for better testing (setting rounds to 1).

def des_enc(inputblock, num_rounds, inputkey64):
    
    # This is the function that accepts one bloc of plaintext
    # and applies all rounds of the DES cipher and returns the
    # cipher text block. 
    # Inputs:
    # inputblock: byte sequence representing input block
    # num_rounds: integer representing number of rounds in the feistel 
    # key: byte sequence (8 bytes)
    # Output:
    # cipherblock: byte sequence  
    bits_list = [bin(int(b))[2:].zfill(8) for b in inputblock]
    #print("bitslist: ",bits_list)
    bitlist = "".join(bits_list)
    #print(bitlist)
    bitlist2 = list(bitlist)
    #print(bitlist2)
    bit_list_after_perm = Permutation(bitlist2,BookInitPermOrder)
    #print (bit_list_after_perm)
    left_bits = bit_list_after_perm[:32]
    right_bits = bit_list_after_perm[32:]
    #print("left bits: ",left_bits)
    #print("Right bits: ",right_bits)
    keyinbit = [bin(int(b))[2:].zfill(8) for b in inputkey64]
    #print("keyinbit: ",keyinbit)
    keyallbits = "".join(keyinbit)
    #print(keyallbits)
    permkeys = Permutation(keyallbits,BookPermOrderkey)
    #print(permkeys)
    
    key_left = (permkeys[:28])
    key_right = (permkeys[28:])
    #print(key_left)
    #print(key_right)
    key48list = []
    for i in range(0,16):
        key48,key_left,key_right = des_keygen(key_left,key_right,i)
        key48list.append(key48)
    for a in range(0,len(key48list)):
        #print("k: ",key48list[a])
        left_bits,right_bits = des_round(left_bits,right_bits,key48list[a])

    #print ("key in fucntion enc_String: ",key48list)
        
    #print("Leftbits: ,Rightbits: ",left_bits,right_bits)
    cipherblockinv = right_bits + left_bits
    #print("Cipherblockinv: ",cipherblockinv)
    cipherblockperm = Permutation(cipherblockinv,PI_1)
    #print("perm Cipher Block: ",cipherblockperm)
    bitconvcipher = BitArray('0b'+cipherblockperm)
    cipherblock = bitconvcipher.bytes
    print("FInal Final Cipher Block: ",cipherblock)
    return cipherblock
    
def des_enc_test(input_fname, inputkey64,num_rounds, output_fname):
    
    # inputkey64: byte sequence (8 bytes)
    # numrounds: asked since your feistel already has it but we always use 16 for DES
    
    # First read the contents of the input file as a byte sequence
#    finp = open(input_fname, 'rb')
#    inpbyteseq = finp.read()
#   print(inpbyteseq)
#    finp.close()
    sublist = []
    length = len(input_fname)
    for a in range(0,length,8):
        subinpbyteseq = input_fname[a:a+8]
        sublist.append(subinpbyteseq)
    print ("sublist: ",sublist)
    if len(sublist[-1])<8:
        sub = 8-len(sublist[-1])
        i =0
        while(i<sub):
            sublist[-1]=sublist[-1]+b'\x20'
            i = i+1
    print(sublist)
    
    cipher_byte_seq = b''
    for u in range(0,len(sublist)):
        enc_string = des_enc(sublist[u],num_rounds,inputkey64)
    cipher_byte_seq = enc_string
    print("Cipher byte seq: ",cipher_byte_seq)
    # Then break the inpbyteseq into blocks of 8 bytes long and 
    # put them in a list
    # Pad the last element with spaces b'\x20' until it is 8 bytes long
    # blocklist = [list of 8 byte long blocks]
    
    # Loop over al blocks and use the dec_enc to generate the cipher block
    # append all cipherblocks together to form the outut byte sequence
    # cipherbyteseq = b''.join([list of cipher blocks])
    
    # write the cipherbyteseq to output file
#    fout = open(output_fname, 'wb')
#    fout.write(cipher_byte_seq)
#    fout.close()


def des_dec(inputblock, num_rounds, inputkey64):

    bits_list = [bin(int(b))[2:].zfill(8) for b in inputblock]
    #print("bitslist: ",bits_list)
    bitlist = "".join(bits_list)
    #print(bitlist)
    bitlist2 = list(bitlist)
    #print(bitlist2)
    bit_list_after_perm = Permutation(bitlist2,BookInitPermOrder)
    #print (bit_list_after_perm)
    left_bits = bit_list_after_perm[:32]
    right_bits = bit_list_after_perm[32:]
    #print("left bits: ",left_bits)
    #print("Right bits: ",right_bits)
    keyinbit = [bin(int(b))[2:].zfill(8) for b in inputkey64]
    #print("keyinbit: ",keyinbit)
    keyallbits = "".join(keyinbit)
    #print(keyallbits)
    permkeys = Permutation(keyallbits,BookPermOrderkey)
    #print(permkeys)
    
    key_left = (permkeys[:28])
    key_right = (permkeys[28:])
    #print(key_left)
    #print(key_right)
    key48list = []
    for i in range(0,16):
        key48,key_left,key_right = des_keygen(key_left,key_right,i)
        key48list.append(key48)
    key48list.reverse()
    for a in range(0,len(key48list)):
        #print("k: ",key48list[a])
        left_bits,right_bits = des_round(left_bits,right_bits,key48list[a])

    #print ("key in fucntion enc_String: ",key48list)
        
    #print("Leftbits: ,Rightbits: ",left_bits,right_bits)
    decipherblockinv = right_bits + left_bits
    #print("Cipherblockinv: ",decipherblockinv)
    decipherblockperm = Permutation(decipherblockinv,PI_1)
    #print("perm Cipher Block: ",decipherblockperm)
    bitconvdecipher = BitArray('0b'+ decipherblockperm)
    plainblock = bitconvdecipher.bytes
    print("FInal Final Cipher Block: ",plainblock)
    
    

    # This is the function that accepts one bloc of ciphertext
    # and applies all rounds of the DES cipher and returns the
    # plaintext text block. 
    # Inputs:
    # inputblock: byte sequence representing ciphertext block
    # num_rounds: integer representing number of rounds in the feistel 
    # key: byte sequence (8 bytes)
    # Output:
    # plainblock: byte sequence    
    
    
    return plainblock

    
def des_dec_test(input_fname, inputkey64,num_rounds, output_fname):
#    finp = open(input_fname, 'rb')
#    inpbyteseq = finp.read()
    #   print(inpbyteseq)
#    finp.close()
    sublist = []
    length = len(input_fname)
    for a in range(0,length,8):
        subinpbyteseq = input_fname[a:a+8]
        sublist.append(subinpbyteseq)
    print ("sublist: ",sublist)
    if len(sublist[-1])<8:
        sub = 8-len(sublist[-1])
        i =0
        while(i<sub):
            sublist[-1]=sublist[-1]+b'\x20'
            i = i+1
    print(sublist)
    
    deciphered_byte_seq = b''
    for u in range(0,len(sublist)):
        dec_string = des_dec(sublist[u],num_rounds,inputkey64)
    deciphered_byte_seq = dec_string
    print("deciphered_byte_seq: ",deciphered_byte_seq)
#    fout = open(output_fname, 'wb')
#    fout.write(deciphered_byte_seq)
#    fout.close()

    # inputkey64: byte sequence (8 bytes)
    # numrounds: asked since your feistel already has it but we always use 16 for DES
        
    # First read the contents of the input file as a byte sequence
    #finp = open(input_fname, 'rb')
    #cipherbyteseq = finp.read()
    #finp.close()
    
    # do the decryption rounds

    # write the plainbyteseq to output file
    #fout = open(output_fname, 'wb')
    #fout.write(plainbyteseq)
    #fout.close()


#input_fname3 = b'\x02\x46\x8a\xce\xec\xa8\x64\x20'
#output_fname = ""
#inputkey64 = b'\x0f\x15\x71\xc9\x47\xd9\xe8\x59'
#input_fname = b'\xda\x02\xce\x3a\x89\xec\xac\x3b'
#input_fname = "inp.txt"
#output_fname = "out.txt"
#num_rounds = 16
#plaintext = des_dec_test(input_fname,inputkey64,num_rounds,output_fname)
#print(input_fname)
#print(input_fname3)
#inputkey64 = b'\x0f\x15\x71\xc9\x47\xd9\xe8\x59'
#encrypted = des_enc_test(input_fname,inputkey64,num_round,output_fname)
#print(cipher_block_)
#print("encrypted final output: ",encrypted)
    

    

