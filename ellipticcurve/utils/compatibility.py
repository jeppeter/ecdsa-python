from sys import version_info as pyVersion
from binascii import hexlify, unhexlify


if pyVersion.major == 3:
    # py3 constants and conversion functions

    stringTypes = (str,)
    intTypes = (int, float)

    def toString(string, encoding="utf-8"):
        try:
            return string.decode(encoding)
        except:
            return string

    def toBytes(string, encoding="utf-8"):
        try:
            return string.encode(encoding)
        except:
            return string

    def safeBinaryFromHex(hexadecimal):
        if len(hexadecimal) % 2 == 1:
            hexadecimal = "0" + hexadecimal
        return unhexlify(hexadecimal)

    def safeHexFromBinary(byteString):
        return toString(hexlify(byteString))
else:
    # py2 constants and conversion functions

    stringTypes = (str, unicode)
    intTypes = (int, float, long)

    def toString(string, encoding="utf-8"):
        return string

    def toBytes(string, encoding="utf-8"):
        return string

    def safeBinaryFromHex(hexadecimal):
        return unhexlify(hexadecimal)

    def safeHexFromBinary(byteString):
        return hexlify(byteString)
