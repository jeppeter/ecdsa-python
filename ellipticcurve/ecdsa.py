from hashlib import sha256
from .signature import Signature
from .math import Math
from .utils.integer import RandomInteger
from .utils.binary import numberFromByteString
from .utils.compatibility import *
from .utils.file import dump_bytes, dump_int
import logging
import struct


def encrypt_value(numberMessage, curve,publicKey):
    r , s , randSignPoint = 0, 0, None
    while r == 0 or s == 0:
        randNum = RandomInteger.between(1, curve.N - 1)
        randSignPoint = Math.multiply(curve.G, n=randNum, A=curve.A, P=curve.P, N=curve.N)
        r = randSignPoint.x % curve.N
        s = ((numberMessage + r * publicKey.point.x) * (Math.inv(randNum, curve.N))) % curve.N
    return r,s


class Ecdsa:

    @classmethod
    def sign(cls, message, privateKey, hashfunc=sha256):
        byteMessage = hashfunc(toBytes(message)).digest()
        logging.info('%s'%(dump_bytes(byteMessage,'byteMessage')))
        numberMessage = numberFromByteString(byteMessage)
        logging.info('%s'%(dump_int(numberMessage,'numberMessage')))
        curve = privateKey.curve

        r, s, randSignPoint = 0, 0, None
        while r == 0 or s == 0:
            randNum = RandomInteger.between(1, curve.N - 1)
            randSignPoint = Math.multiply(curve.G, n=randNum, A=curve.A, P=curve.P, N=curve.N)
            r = randSignPoint.x % curve.N
            s = ((numberMessage + r * privateKey.secret) * (Math.inv(randNum, curve.N))) % curve.N
        recoveryId = randSignPoint.y & 1
        if randSignPoint.y > curve.N:
            recoveryId += 2

        logging.info('%s'%(dump_int(r,'r')))
        logging.info('%s'%(dump_int(s,'s')))
        return Signature(r=r, s=s, recoveryId=recoveryId)

    @classmethod
    def encrypt(cls,message,publicKey):
        retb = b''
        rlen = 0
        inbytes = toBytes(message)
        curve = publicKey.curve
        while rlen < len(inbytes):
            steplen = curve.length()
            if (rlen + steplen) > len(inbytes):
                steplen = len(inbytes) - rlen
            partbytes = inbytes[rlen:(rlen + steplen)]
            if len(partbytes) < curve.length():
                pb = curve.length() - len(partbytes)
                while len(partbytes) < curve.length():
                    partbytes += struct.pack('B',pb)
            numberMessage = numberFromByteString(partbytes)
            r , s = encrypt_value(numberMessage,curve,publicKey)
            retb += byteStringFromHex(hexFromInt(r))
            retb += byteStringFromHex(hexFromInt(s))
            rlen += steplen
            if rlen == len(inbytes) and steplen == curve.length():
                # because is so align,
                partbytes = b''
                pb = curve.length()
                while len(partbytes) < curve.length():
                    partbytes += struct.pack('B',pb)
                numberMessage = numberFromByteString(partbytes)
                r,s = encrypt_value(numberMessage,curve,publicKey)
                retb += byteStringFromHex(hexFromInt(r))
                retb += byteStringFromHex(hexFromInt(s))
        return retb

    @classmethod
    def decrypt(cls,encmsg,privateKey):
        retb = b''
        rlen = 0
        curve = privateKey.curve

        if len(encmsg) % (curve.length() * 2) != 0:
            return None

        while rlen < len(encmsg):
            rv = encmsg[rlen:(rlen + curve.length())]
            sv = encmsg[(rlen + curve.length()) : (rlen + curve.length() * 2)]
            r = numberFromByteString(rv)
            s = numberFromByteString(sv)
            if not 1 <= r <= (curve.N -1) :
                return None

            if not 1 <= s <= (curve.N - 1):
                return None

            inv = Math.inv(s,curve.N)
            u1 = 

        return retb




    @classmethod
    def verify(cls, message, signature, publicKey, hashfunc=sha256):
        byteMessage = hashfunc(toBytes(message)).digest()
        numberMessage = numberFromByteString(byteMessage)
        curve = publicKey.curve
        r = signature.r
        s = signature.s
        if not 1 <= r <= curve.N - 1:
            return False
        if not 1 <= s <= curve.N - 1:
            return False
        inv = Math.inv(s, curve.N)
        u1 = Math.multiply(curve.G, n=(numberMessage * inv) % curve.N, N=curve.N, A=curve.A, P=curve.P)
        u2 = Math.multiply(publicKey.point, n=(r * inv) % curve.N, N=curve.N, A=curve.A, P=curve.P)
        v = Math.add(u1, u2, A=curve.A, P=curve.P)
        if v.isAtInfinity():
            return False
        return v.x % curve.N == r
