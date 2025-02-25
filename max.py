import sys

print(sys.maxsize)
# 9223372036854775807

print(type(sys.maxsize))
# <class 'int'>

print(sys.maxsize == 2**63 - 1)
# True
