#!/usr/bin/env python
# coding: utf-8

# ## A few tips for more efficient coding

# In[48]:


# Unless otherwise stated, from now on we're going to eliminate spaces from our plaintext and only
# work with continuous strings of characters in the {a, b, ..., z} range.

# A simple way to eliminate spaces from a string is to use the replace() method
s = 'My PlainText String'
s = s.replace(' ','')
print(s)

# note that "replace" can be used for replacing any character with another character in a string
# Other useful methods for use on string variables are upper() and lower() methods which convert all characters in a string 
# to uppercase or lowercase, respectively
print(s.lower())


# In[49]:


# We also showed in class how Python's list comprehensions can be used to efficiently convert strings to indices
s = 'myplaintextstring'
s_ind_list = [ord(c)-97 for c in s]
print(s_ind_list)


# In[50]:


# The reverse operation is also possible
char_list = [chr(ind+97) for ind in s_ind_list]
print(char_list)
# The join method creates a string by "joining" all elements of the given list together using the provided character
# In this case the provided character is null so all elements are just directly attached together to give us s
s = ''.join(char_list)
print(s)


# In[51]:


# Another tip is for when we need to work on chunks of a list (for example in Hill 3x3 cipher we need
# to select the elements of the plaintext in chunks of 3)
# we can use the range function with the step of 3
for i in range(0,len(char_list),3):  # it means integers from 0 to len(char_list)-1 with step 3
    sublist = char_list[i:i+3]  # it means elements i,i+1,i+2 (the last element -1)
    print(sublist)


# ## Finding mod-26 inverse of a matrix

# ### We mentioned that the modulo 26 inverse of a matrix may noit exists. But if it does, we can make use
# ### of the normal inverse and determinent of a matrix calculations given by some math packages to find the
# ### mod-26 inverse of a matrix
# ### Our Notation (We focus on 3x3 matrices, but this logic works for larger matrices as well):
# ### R: set of all real numbers
# ### M: original matrix with elements in range 0-25 (a 3x3 matrix)
# ### Minv: real inverse of M (a 3x3 matrix, values in R)
# ### Mdet: real determinant of M (a number, in R)
# ### Madj: real adjoint matrix of M (3x3 matrix, values in R)
# 
# ### Similarly, we use a 26 suffix to show the equivalent of the above values in mod-26 space i.e.,
# ### Minv26: mod-26 inverse of M (a 3x3 matrix, values in 0-25)
# ### Mdet26: mod-26 determinant of M (a number in 0-25)
# ### Mdetinv26: mod-26 inverse Mdet26 (a number in 0-25)
# ### Madj26: mod-26 adjoint matrix of M (3x3 matrix, values in 0-25)
# 
# ### For real matrices we have the following equation for finding the inverse matrix:
# ### Minv = (1/Mdet) * Madj     (Eq. 2)
# 
# ### But for mod-26 matrices:
# ### Minv26 = (Mdetinv26 *  Madj26)%26     (Eq. 1)
# 

# In[2]:


# Let's first see how Mdetinv26 is defined for equation (1) above. The mod-26 inverse of a number m between 0-25 is another number n 
# in that range such that
# m*n mod 26 = 1
# For example the inverse of 3 is 9 since 3*9 mod 26 = 27 mod 26 = 1.
# Not all 0-25 numbers have a mod-26 inverse. Let's try to find those that have inverses
Mod26invTable = {}
for m in range(26):
    for n in range(26):
        if (m*n)%26==1:
            Mod26invTable[m] = n
            print(m,n)
# Let's now see how we can compute Madj26 for equatin (1).
# Madj26 is actually Madj mod 26 so we need to find Madj
# The numpy module in Python has functions for Minv and Mdet and we can always find Madj form Minv and Mdet 
# using equation (2) above:
# Madj = Mdet * Minv, therefore
# Madj26 = (Mdet*Minv)%26
import numpy as np
from pprint import pprint

M = np.array([[17,17,5],[21,18,21],[2,2,19]])
print("M: ")
print(M)
Minv = np.linalg.inv(M)
Mdet = np.linalg.det(M)

# Let's find Mdet26 and Mdetinv26
Mdet26 = Mdet%26
if Mdet26 in Mod26invTable:
    Mdetinv26 = Mod26invTable[Mdet26]
else:
    Mdetinv26 = None # This should be an exit point since we can't find an inverse for M in mod-26

#print(Mdet,Mdetinv26)

# Now, Let's find Madj26
Madj = Mdet*Minv
Madj26 = Madj%26


#print(np.matmul(M,Minv))

#So, The mod-26 inverse of M from equation (1) will be
Minv26 = (Mdetinv26*Madj26)%26
# We need to convert it to pure integers. So we round the elments and then do mod-26 again
Minv26 = np.matrix.round(Minv26, 0)%26

print("Minv26:")
# So, if we are lucky and Mdet26 is one of the above integers, it has an inverse and we can find it from the 
# above table we just constructed.
# For example, inverse of 3 is stored in Mod26invTable[3]

# In other words, if a python function, gives us the real determinant Mdet of M, we can find Mdetinv26 from:
# Mdetinv26 = Mod26invTable[Mdet%26]  (provided that Mdet%26 has an inverse)


# In[3]:


# Let's now see how we can compute Madj26 for equatin (1).
# Madj26 is actually Madj mod 26 so we need to find Madj
# The numpy module in Python has functions for Minv and Mdet and we can always find Madj form Minv and Mdet 
# using equation (2) above:
# Madj = Mdet * Minv, therefore
# Madj26 = (Mdet*Minv)%26
import numpy as np
from pprint import pprint

M = np.array([[17,17,5],[21,18,21],[2,2,19]])
print("M: ")
print(M)
Minv = np.linalg.inv(M)
Mdet = np.linalg.det(M)

# Let's find Mdet26 and Mdetinv26
Mdet26 = Mdet%26
if Mdet26 in Mod26invTable:
    Mdetinv26 = Mod26invTable[Mdet26]
else:
    Mdetinv26 = None # This should be an exit point since we can't find an inverse for M in mod-26

#print(Mdet,Mdetinv26)

# Now, Let's find Madj26
Madj = Mdet*Minv
Madj26 = Madj%26


#print(np.matmul(M,Minv))

#So, The mod-26 inverse of M from equation (1) will be
Minv26 = (Mdetinv26*Madj26)%26
# We need to convert it to pure integers. So we round the elments and then do mod-26 again
Minv26 = np.matrix.round(Minv26, 0)%26

print("Minv26:")
print(Minv26)

# Let's check and see if we did right:
# M x Minv26 should be I (we need some rounding and %26 operations)
MMinv26 = np.matmul(M,Minv26)%26
MMinv26 = np.matrix.round(MMinv26,0)

print("M x Minv26: ")
print(MMinv26)
# If we wish to convert a matrix back from numpy format to basic list-of-lists format, 
# we can use the tolist() method:
print(MMinv26.tolist())


# # Homework 2- Part 1: Vigenere Cipher
# ## Write an encryption and a decryption function for Vigenere cipher as described below

# In[70]:


# Hint: You can use your homework1 caesar encryption and decryption functions but you need to copy them
#       here and avoid importing that homework since we won't be able to do the same thing for grading.
# We will be importing this python file and call its functions in another grading script. So we don't need any
# command line argument support like what we did for the caesar cipher.
#Ankush Jain, 116806909

# Vigenere encryption function
def vigenere_enc(keyword, plaintext):
    if len(keyword)<len(plaintext):
        diff = len(plaintext)-len(keyword)
        i = 0
        while i< diff:
            keyword=keyword + keyword[i]
            i=i+1
    
    plaintext_list = [ord(c)-97 for c in plaintext]
    #print(plaintext_list)
    keyword_list = [ord(a)-97 for a in keyword]
    #print (keyword_list)
    result_list = []
    for z in range(0,len(plaintext_list)):
        result_list.append((plaintext_list[z] + keyword_list[z])%26)
    
    enc_string_list = [chr(ind+97) for ind in result_list]
    #print(enc_string_list)
    c = ''.join(enc_string_list)
    print(c) 
          
    # keyword is a string of arbitrary length
    # plaintext is the plaintext string of arbitrary length
    # Both strings will be from {a,b,...,z}
    
    # perform the encryption of given plaintext using the given keyword
    # according to the Vigenere cipher. You need to repeat the keyword 
    # enough times if needed to make it the same length as plaintext
    
    # c will be the resulting ciphertext
    #c = ...
    
    return c


# Vionegere decryption function
def vigenere_dec(keyword, ciphertext):
    # keyword is a string of arbitrary length
    # ciphertext is the ciphertext string of arbitrary length
    # Both strings will be from {a,b,...,z}
    
    # perform the decryption of given ciphertext using the given keyword
    # according to the Vigenere cipher. You need to repeat the keyword 
    # enough times if needed to make it the same length as ciphertext
    
    # p will be the resulting plaintext
    # p = ...
    if len(keyword)<len(ciphertext):
        diff = len(ciphertext)-len(keyword)
        i = 0
        while i< diff:
            keyword=keyword + keyword[i]
            i=i+1
    ciphertext_list = [ord(c)-97 for c in ciphertext]
    print(ciphertext_list)
    keyword_list = [ord(a)-97 for a in keyword]
    #print (keyword_list)
    result_list_dec = []
   # print (len(ciphertext_list))
   # print (len(keyword_list))
    for z in range(0,len(ciphertext_list)):
        result_list_dec.append((ciphertext_list[z] - keyword_list[z])%26)
    dec_string_list = [chr(ind+97) for ind in result_list_dec]
    #print(dec_string_list)
    p = ''.join(dec_string_list)
    print(p) 
    
    return p



# # Homework 2- Part 2: Hill Cipher
# ## Write an encryption and a decryption function for Hill cipher as described below

# In[78]:


# Ankush Jain,116806909
def matinvmod26(M):
    
# Let's first see how Mdetinv26 is defined for equation (1) above. The mod-26 inverse of a number m between 0-25 is another number n 
# in that range such that
# m*n mod 26 = 1
# For example the inverse of 3 is 9 since 3*9 mod 26 = 27 mod 26 = 1.
# Not all 0-25 numbers have a mod-26 inverse. Let's try to find those that have inverses
    Mod26invTable = {}
    for m in range(26):
        for n in range(26):
            if (m*n)%26==1:
                Mod26invTable[m] = n
            print(m,n)
# Let's now see how we can compute Madj26 for equatin (1).
# Madj26 is actually Madj mod 26 so we need to find Madj
# The numpy module in Python has functions for Minv and Mdet and we can always find Madj form Minv and Mdet 
# using equation (2) above:
# Madj = Mdet * Minv, therefore
# Madj26 = (Mdet*Minv)%26
    import numpy as np
    from pprint import pprint

    print("M: ")
    print(M)
    Minv = np.linalg.inv(M)
    Mdet = np.linalg.det(M)

# Let's find Mdet26 and Mdetinv26
    Mdet26 = Mdet%26
    if Mdet26 in Mod26invTable:
        Mdetinv26 = Mod26invTable[Mdet26]
    else:
        Mdetinv26 = None # This should be an exit point since we can't find an inverse for M in mod-26

#print(Mdet,Mdetinv26)

# Now, Let's find Madj26
    Madj = Mdet*Minv
    Madj26 = Madj%26


#print(np.matmul(M,Minv))

#So, The mod-26 inverse of M from equation (1) will be
    Minv26 = (Mdetinv26*Madj26)%26
# We need to convert it to pure integers. So we round the elments and then do mod-26 again
    Minv26 = np.matrix.round(Minv26, 0)%26

    print("Minv26:")

    return(Minv26)# So, if we are lucky and Mdet26 is one of the above integers, it has an inverse and we can find it from the 
# above table we just constructed.
# For example, inverse of 3 is stored in Mod26invTable[3]

# In other words, if a python function, gives us the real determinant Mdet of M, we can find Mdetinv26 from:
# Mdetinv26 = Mod26invTable[Mdet%26]  (provided that Mdet%26 has an inverse)
def hill_enc(M, plaintext):
    # M is the encryption matrix - Let's assume it's always 3x3 for now
    # M is in the list of lists format i.e.,
    # [[M11,M12,M13],[M21,M22,M23],[M31,M32,M33]]
    # plaintext is the plaintext string of arbitrary length
    # from {a,b,...,z}
    
    # perform the encryption of given plaintext using the given matrix M
    # according to the Hill cipher. Pad the plaintext with 'x' characters to 
    # make its length a multiple of 3.     
    
    # Some helpful funcitons:
    # len(plaintext) : gives the length of the plaintext string
    # one way of selecting chunks of 3 elements from a list:
    # 
    
    # c will be the resulting ciphertext
    #c = ...
    plaintext = plaintext.replace(" ","")
    #print (plaintext)
    plaintext_list = [ord(a)-97 for a in plaintext]
    #print (plaintext_list)
    i = len(plaintext_list)%3
    for a in range (0,i+1):
        plaintext_list.append(int("2"))
    #print (plaintext_list)
    #plaintext_m = np.matrix(plaintext_list)
    #print(plaintext_m)
    #b = int(len(plaintext_list)/3)
    #print(b)
    plaintext_m=[]
    for i in range(0,len(plaintext_list),3):  # it means integers from 0 to len(char_list)-1 with step 3
        sublist = plaintext_list[i:i+3]  # it means elements i,i+1,i+2 (the last element -1)
        plaintext_m.append(sublist)
    print (plaintext_m)
    #plaintextmatrix= np.matrix(plaintext_m)
    #print (plaintextmatrix)
    #print (M)
    enc_matrix = np.matmul(plaintext_m,M)%26
    #print (enc_matrix)
    enc_list =[]
    for lst in enc_matrix:
        for char in lst:
            enc_list.append(char)
    enc_list = [chr(ind+97) for ind in enc_list]
    #print(enc_list)
# The join method creates a string by "joining" all elements of the given list together using the provided character
# In this case the provided character is null so all elements are just directly attached together to give us s
    c = ''.join(enc_list)
    #print(c)
    return(c)
    
    #for i in range(0,len(enc_matrix)):
        #enc_array = enc_matrix(i:i+len(enc_matrix))
    #print (enc_array)
    
    
    


# 3- write the Hill decryption function
def hill_dec(M, ciphertext):
    # M is the encryption matrix - Let's assume it's always 3x3 for now
    # M is in the list of lists format i.e.,
    # [[M11,M12,M13],[M21,M22,M23],[M31,M32,M33]]
    # ciphertext is the ciphertext string of arbitrary length
    # from {a,b,...,z}
    
    # perform the decryption of given ciphertext using the given matrix M
    # according to the Hill cipher. 
    
    # p will be the resulting plaintext
    # p = ...
    #plaintext = plaintext.replace(" ","")
    #print (plaintext)
    ciphertext_list = [ord(a)-97 for a in ciphertext]
    #print (ciphertext_list)
    #i = len(p_list)%3
    #for a in range (0,i+1):
    #    plaintext_list.append(int("2"))
    #print (plaintext_list)
    #plaintext_m = np.matrix(plaintext_list)
    #print(plaintext_m)
    #b = int(len(plaintext_list)/3)
    #print(b)
    ciphertext_m=[]
    for i in range(0,len(ciphertext_list),3):  # it means integers from 0 to len(char_list)-1 with step 3
        sublist = ciphertext_list[i:i+3]  # it means elements i,i+1,i+2 (the last element -1)
        ciphertext_m.append(sublist)
    print (ciphertext_m)
    #plaintextmatrix= np.matrix(plaintext_m)
    #print (plaintextmatrix)
    #print (M)
    invM = matinvmod26(M)
   # print (invM)
    dec_matrix = np.matmul(ciphertext_m,invM)%26
   # print (dec_matrix)
    dec_list =[]
    for lst in dec_matrix:
        for char in lst:
            dec_list.append(char)
    dec_list = [chr(int(ind)+97) for ind in dec_list]
# The join method creates a string by "joining" all elements of the given list together using the provided character
# In this case the provided character is null so all elements are just directly attached together to give us s
    p = ''.join(dec_list)
    #print(p) 
    return p
    
    


# In[ ]:




