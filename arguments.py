# Python program to demonstrate
# command line arguments
 
 
import sys
 
# total arguments
n = len(sys.argv)
print("Total arguments passed:", n)
 
# Arguments passed
print("\nName of Python script:", sys.argv[0])
 
print("\nArguments passed:")
for i in range(1, n):
    print(str(sys.argv[i]) + " ")