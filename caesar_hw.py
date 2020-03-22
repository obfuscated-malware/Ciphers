# Ankush Jain, 116806909

#!/usr/bin/python

import sys

def caesar_str_enc(plaintext,K):

        ciphertext = ""

        for ch in plaintext:

                if ch == " ":

                        ciphertext = ciphertext + ch

                else:

                        encch = caesar_ch_enc(ch,K)

                        ciphertext = ciphertext + encch

        return ciphertext



def caesar_ch_enc(ch,K):

        p = ord(ch)-97

        codedp = (p+K)%26

        encch=chr(codedp+97)

        return encch



def caesar_str_dec(encstr,K):

        plaintext = ""

        for ch in encstr:

                if ch == " ":

                        plaintext = plaintext + ch

                else:

                        decch = caesar_ch_dec(ch, K)

                        plaintext = plaintext + decch

        return plaintext



def caesar_ch_dec(ch,K):

        p = ord(ch)-97

        decodedp = (p-K)%26

        decch = chr(decodedp+97)

        return decch



def test_module():

        K =int(sys.argv[1])

        input_str = sys.argv[2]

        print(input_str)

        encstr=caesar_str_enc(input_str, K)

        print(encstr)

        decstr=caesar_str_dec(encstr, K)

        print(decstr)



if __name__=="__main__":

      test_module()
