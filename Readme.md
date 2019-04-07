Since asymetric RSA private/public keys cryptography has limitations on the size of the contents to be encrypted, a common practice is to encrypt files using symetric cryptography, such as aes-cbc, using the same key to encrypt and decrypt, and then use asymetric cryptography, such as RSA, to encrypt the aes key used with a pair of public/private keys.

A public key consist of a large number n which is the product of two large primes, p and q. It is almost impossible to factorise p and q from n. 

However, if two public keys have been calculated from the same q, then n1 = p1 x q and n2 = p2 x q, and it is easy to calculate q as the greatest common divisor of n1 and n2.

From the p and q used to create the public key it is possible to obtain also the private key.

This write up explains the technique, math and history of the problem in great detail:

http://www.loyalty.org/~schoen/rsa/

#### Step 1: Extract the different parts of each XML challenge file into separate files for later processing.

(note: There's an XML problem with the input file, the EncryptedFile closing tag is missing a forward slash /)

    $python parseXMLFile.py Ransom_File_001.txt 
    $python parseXMLFile.py Ransom_File_002.txt 

#### Step 2: Extract the public keys from the certificate files into separate files:
 
    $openssl x509 -pubkey -noout -in Ransom_File_001.txt__cert.pem > Ransom_File_001.txt__pubkey.pem
    $openssl x509 -pubkey -noout -in Ransom_File_002.txt__cert.pem > Ransom_File_002.txt__pubkey.pem


#### Steps 3, 4 and 5 are all done in a one-linner

3. Get the n1 and n2 values from the public keys respectively and calculate the greatest common denominator
4. Calculate the greatest common denominator and factorise n1 into p1 and gcd and n2 into p2 and gcd
5. Generate private key files from p1 and gcd and from p2 and gcd


First, compile this binary from the source provided, which will create a private key file from the p and q values. The source code is kept in this repository as backup, and it's originally linked in the article mentioned above.

    $clang private-from-pq.c -I /usr/local/include /usr/local/opt/openssl/lib/libcrypto.a  -o private-from-pq


    $python gcd.py `openssl rsa -in Ransom_File_001.txt__pubkey.pem -pubin -modulus -noout | cut -d '=' -f 2` `openssl rsa -in Ransom_File_002.txt__pubkey.pem -pubin -modulus -noout|cut -d '=' -f 2` --p1 --gcd | xargs ./private-from-pq > Ransom_File_001.txt__privkey.key

    $python gcd.py `openssl rsa -in Ransom_File_001.txt__pubkey.pem -pubin -modulus -noout | cut -d '=' -f 2` `openssl rsa -in Ransom_File_002.txt__pubkey.pem -pubin -modulus -noout|cut -d '=' -f 2` --p2 --gcd | xargs ./private-from-pq > Ransom_File_002.txt__privkey.key


#### Step 6: Extract the private key pem to a different file.

    $grep -n  'BEGIN RSA PRIVATE KEY' Ransom_File_001.txt__privkey.key | cut -d ':' -f 1 | xargs -I{} tail -n +{} Ransom_File_001.txt__privkey.key > Ransom_File_001.txt__privkey.pem
    $grep -n  'BEGIN RSA PRIVATE KEY' Ransom_File_001.txt__privkey.key | cut -d ':' -f 1 | xargs -I{} tail -n +{} Ransom_File_002.txt__privkey.key > Ransom_File_002.txt__privkey.pem


#### Step 7: Decrypt the file encryption keys using the private keys

    $openssl rsautl -decrypt -inkey Ransom_File_001.txt__privkey.pem -in Ransom_File_001.txt__aes.key -out Ransom_File_001.txt__aes.pass
    $openssl rsautl -decrypt -inkey Ransom_File_002.txt__privkey.pem -in Ransom_File_002.txt__aes.key -out Ransom_File_002.txt__aes.pass

#### Step 8: Decrypt the encrypted files with encryption keys using the aes-256-cbc as indicated by the <FileEncryptionAlg> element

    $openssl enc -d -aes-256-cbc -in Ransom_File_001.txt__encrypted_file.raw -out Ransom_File_001.txt__original.txt -pass file:./Ransom_File_001.txt__aes.pass
    $openssl enc -d -aes-256-cbc -in encryptedFile2.raw -out file2.txt -pass file:./fileEncryptionKey2.txt 
