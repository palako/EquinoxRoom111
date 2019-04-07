from math import gcd 
import argparse

arg_parser = argparse.ArgumentParser(description='Calculates the Greatest Common Denominator of two integers')
arg_parser.add_argument('n1', type=str, help='First integer expected in hexadecimal format')
arg_parser.add_argument('n2', type=str, help='Second integer, expected in hexadecimal format')
arg_parser.add_argument('--labels', action='store_true', help='Show results as name=value (true) or just value (false)')
arg_parser.add_argument('--gcd', action='store_true', help='Output the value of the greatest common denominator')
arg_parser.add_argument('--p1', action='store_true', help='Output the value of factorised value from n1 and the gcd')
arg_parser.add_argument('--p2', action='store_true', help='Output the value of factorised value from n2 and the gcd')
args = arg_parser.parse_args()
n1 = int(args.n1, 16)
n2 = int(args.n2, 16)
print_labels = args.labels
print_p1 = args.p1
print_p2 = args.p2
print_gcd = args.gcd

#if no output is explicitly requested, print out all
if not print_p1 and not print_p2 and not print_gcd:
	print_p1 = True
	print_p2 = True
	print_gcd = True


q=gcd(n1,n2)
p1 = n1//q
p2 = n2//q


if print_p1:
	if print_labels: print ("p1=", end='')
	print(p1, end=' ')

if print_p2:
	if print_labels: print ("p2=", end='')
	print(p2, end=' ')

if print_gcd:
	if print_labels: print("gcd=", end='')
	print(q, end=' ')
