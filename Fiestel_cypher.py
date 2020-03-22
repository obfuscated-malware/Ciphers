#!/usr/bin/env python
# coding: utf-8

# # Feistel Cipher

# ![feistel_cipher.JPG](attachment:feistel_cipher.JPG)

# ### Encryption involves running the input plaintext block through multiple rounds of processing.
# ### All rounds have the same structure and only differ in the key used.

# ### Round $i$:
# 
# ![feistel_block.JPG](attachment:feistel_block.JPG)

# In[103]:


# bitwise XOR function operating on two byte sequences (multiple Bytes each)
# If the argument have different number of bytes, it will return a result that 
# is as long as the shorter argument. 
#<Ankush Jain, 116806909>
import random
import hmac
import hashlib
import codecs
def xor(byteseq1, byteseq2):
    # First we convert each byte to its int value
    l1 = [b for b in byteseq1]
    l2 = [b for b in byteseq2]

    # Then we use the xor ^ operator to xor the integer values
    # At the same time, we convert the resulting intergers back to byte form
    # Note that the zip function automatically picks the size of the shorter of l1,l2
    # so l1xorl2 is the same size as the shorter of l1 and l2. This allows us to 
    # select our F function to always give a long output even if we need part of it.
    l1xorl2 = [bytes([elem1^elem2]) for elem1,elem2 in zip(l1,l2)]
    
    # finally, we convert the list of individual XOR results into a byte sequence
    # by concatenating all of them together
    result = b''.join(l1xorl2)

    return result

# As discussed, round function F can be any arbitrary function but it's usually a shuffling function
# such as a hash function. Here we use the SHA1 hash (we'll study the details of it later)
# to create a function that returns a 32bit string (since we assume 32 bit byteseq input)
def F(byteseq, k):
    # create a hmac sha1 
    h = hmac.new(k, byteseq, hashlib.sha1)
    # Return first 8 bytes of the calculated hmac sha1 hash
    return h.digest()[:8]

# main block processing
def feistel_block(LE_inp, RE_inp, k):
    # LEinp and REinp are the outputs of the previous round
    # k is the key for this round which usually has a different 
    # value for different rounds
    LE_out = RE_inp
    RE_out = xor(LE_inp,F(RE_inp,k))
    return LE_out, RE_out
    

# In a real Feistel implementation, different keys are used in different rounds. Here
# we use 64bit keys so for 16 rounds, we need 16 random 8byte keys. We can just generate
# 16 random 8 byte numbers we use the random.randint() function to be able to set the seed
# value and create the same keys for both the encoder and the decoder
def gen_keylist(keylenbytes, numkeys, seed):
    # We need to generate numkeys keys each being keylen bytes long
    keylist = []
    random.seed(seed)
    for x in range(0,16):
        keylist.append(random.randint(0,255))
        
    # Use the random.randint(min,max) function to generate individual
    # random integers in range [min, max]. Generate a list of 16
    # random byte sequences each of the 4 bytes long to be used as 
    # keys for 16 stages of the feistel encoder. To make sure we have control over
    # the generated random numbers meaning that the same sequence is 
    # generated in different runs of our program, 
    
    # keylist = [16 elements of 'bytes' type and 4 bytes long each]
    
    return keylist


def feistel_enc(inputblock, num_rounds, seed):
    
    # This is the function that accepts one bloc of plaintext
    # and applies all rounds of the feistel cipher and returns the
    # cipher text block. 
    # Inputs:
    # inputblock: byte sequence representing input block
    # num_rounds: integer representing number of rounds in the feistel 
    # seed: integer to set the random number generator to defined state
    # Output:
    # cipherblock: byte sequence
    keylist = gen_keylist(8, num_rounds, seed)
    sub_inp_list=[]
    for a in range(0,(len(inputblock)),4):
        sub_input= inputblock[a:a+4]
        sub_inp_list.append(sub_input)
    #print(sub_inp_list)
    #lef = sub_inp_list[0]
    #rig = sub_inp_list[1]
    ef = inputblock[:4]
    ig = inputblock[4:8]
    for x in range(num_rounds):
        key = keylist[x]
        #lef,rig=feistel_block(lef,rig,bytes([key])) 
        ef,ig=feistel_block(ef,ig,bytes([key])) 
    cipherblock = ig + ef
    return cipherblock
    
    
    
    #print (Lef)
    #print (rig)
    
    # first generate the required keys
   
       
def feistel_enc_test(input_fname, seed, num_rounds, output_fname):
    # First read the contents of the input file as a byte sequence
    finp = open(input_fname,"rb")
    inpbyteseq = finp.read()
    #print (inpbyteseq)
    finp.close()
    sublist = []
    length = len(inpbyteseq)
    for a in range(0,length,8):
        subinpbyteseq = inpbyteseq[a:a+8]
       
        sublist.append(subinpbyteseq)
    #print("-------------")
    #print (sublist)
    if len(sublist[-1])<8:
        sub = 8-len(sublist[-1])
        i =0
        while(i<sub):
            sublist[-1]=sublist[-1]+b'\x20'
            i = i+1
    #print (sublist)
    cypher_byte_seq = []
    for u in range(0,len(sublist)):
        enc_string = feistel_enc(sublist[u],num_rounds,seed)
        cypher_byte_seq.append(enc_string)
    #print (cypher_byte_seq)
    cipherbyteseq = b''.join(cypher_byte_seq)
    
    # Then break the inpbyteseq into blocks of 8 bytes long and 
    # put them in a list
    # Pad the last element with spaces b'\x20' until it is 8 bytes long
    # blocklist = [list of 8 byte long blocks]
    
    # Loop over al blocks and use the feistel_enc to generate the cipher block
    # append all cipherblocks together to form the outut byte sequence
    # cipherbyteseq = b''.join([list of cipher blocks])
    
    # write the cipherbyteseq to output file
    #print("Life is good")
    #print(cipherbyteseq)
    fout = open(output_fname, 'wb')
    fout.write(cipherbyteseq)
    fout.close()
    
    
def feistel_dec(inputblock, num_rounds, seed):
    # This is the function that accepts one bloc of ciphertext
    # and applies all rounds of the feistel cipher decruption and returns the
    # plain text block. 
    # Inputs:
    # inputblock: byte sequence representing input block
    # num_rounds: integer representing number of rounds in the feistel 
    # seed: integer to set the random number generator to defined state
    # Output:
    # cipherblock: byte sequence
    
    
    # first generate the required keys
    keylist = gen_keylist(8, num_rounds, seed)
    
    
    
    #keylist = gen_keylist(8, num_rounds, seed)
    sub_inp_list=[]
    for a in range(0,(len(inputblock)),4):
        sub_input= inputblock[a:a+4]
        sub_inp_list.append(sub_input)
    #print(sub_inp_list)
    #left1 = 
    #lef = sub_inp_list[0]
    #rig = sub_inp_list[1]
    #print(lef)
    #print(rig)
    ef = inputblock[:4]
    ig = inputblock[4:8]
    
    for x in (reversed(range(num_rounds))):
        key = keylist[x]
        #lef,rig= feistel_block(lef,rig,bytes([key])) 
        ef,ig= feistel_block(ef,ig,bytes([key])) 
    plainblock = ig + ef
    
    
    return plainblock

def feistel_dec_test(input_fname, seed, num_rounds, output_fname):
    
    # First read the contents of the input file as a byte sequence
    #finp = open(input_fname, 'rb')
    #inpbyteseq = finp.read()
    #finp.close()
    
    finp = open(input_fname,"rb")
    inpbyteseq = finp.read()
    #print (inpbyteseq)
    finp.close()
    sublist = []
    length = len(inpbyteseq)
    for a in range(0,length,8):
        subinpbyteseq = inpbyteseq[a:a+8]
        #print (subinpbyteseq)
        sublist.append(subinpbyteseq)
    #print (sublist)
    if len(sublist[-1])<8:
        sub = 8-len(sublist[-1])
        i =0
        while(i<sub):
            sublist[-1]=sublist[-1]+b'\x20'
            i = i+1
            
    #print("after space---")
    #print (sublist)
    cypher_byte_seq = []
    for u in range(0,len(sublist)):
        dec_string = feistel_dec(sublist[u],num_rounds,seed)
        #print(dec_string)
        cypher_byte_seq.append(dec_string)
    #print (cypher_byte_seq)
    plainbyteseq = b''.join(cypher_byte_seq)
    #print(plainbyteseq)
    # Then break the inpbyteseq into blocks of 8 bytes long and 
    # put them in a list
    # Pad the last element with spaces b'\x20' until it is 8 bytes long
    # blocklist = [list of 8 byte long blocks]
    
    # Loop over al blocks and use the feistel_dec to generate the plaintext block
    # append all plainblocks together to form the output byte sequence
    # plainbyteseq = b''.join([list of plain blocks])
    
    # write the plainbyteseq to output file
    fout = open(output_fname, 'wb')
    fout.write(plainbyteseq)
    fout.close()
    
#if __name__=="__main__":
 #   feistel_enc_test('fiestel.txt',10,16,'fiestel_out.txt')
  #  feistel_dec_test('fiestel_out.txt',10,16,'fiestel_out2.txt')
    


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




