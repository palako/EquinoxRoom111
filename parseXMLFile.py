import xml.etree.ElementTree as ET
import argparse
import base64

arg_parser = argparse.ArgumentParser(description='Parses an XML file created by the ransomware.')
arg_parser.add_argument('input_filename', type=str, help='input xml file to parse')
input_filename = arg_parser.parse_args().input_filename

xml_tree = ET.parse(input_filename)
xml_tree.getroot()

cert = xml_tree.find('Certificate').text

cert_filename = input_filename + '__cert.pem'
cert_file = open(cert_filename, "w")
cert_file.write('-----BEGIN CERTIFICATE-----')
cert_file.write(cert)
cert_file.write('-----END CERTIFICATE-----')
cert_file.close()

aes_key_b64 = xml_tree.find('FileEncryptionKey').text

aes_key = base64.b64decode(aes_key_b64)

encryption_key_filename = input_filename + '__aes.key'
encryption_key_file = open(encryption_key_filename, "wb")
encryption_key_file.write(bytearray(aes_key))
encryption_key_file.close()

encrypted_content_b64 = xml_tree.find('EncryptedFile').text

encrypted_content = base64.b64decode(encrypted_content_b64)

encrypted_file_filename = input_filename + '__encrypted_file.raw'
encrypted_file = open(encrypted_file_filename, "wb")
encrypted_file.write(bytearray(encrypted_content))
encrypted_file.close()