import struct

def _resolveFloat(asBytes):
    return round(struct.unpack("f", asBytes)[0], 2)

def _resolveDouble(asBytes):
    return round(struct.unpack("d", asBytes)[0], 2)

def _resolveInt(asBytes):
    return int.from_bytes(asBytes, byteorder="little")

def _mpsToKmh(mps):
    return round(mps * 3.6, 2)

def resolveSpeed(byteValues):
    asBytes = bytes(byteValues)
    asMps =  _resolveFloat(asBytes) # in m/s
    asKmh = _mpsToKmh(asMps)
    return asKmh

def resolveSpeedRound(byteValues):
    return round(resolveSpeed(byteValues))

def resolveIntValue(byteValues):
    asBytes = bytes(byteValues)
    asInt = _resolveInt(asBytes)
    return asInt

def resolveFloatValue(byteValues):
    asBytes = bytes(byteValues)
    asRpm = _resolveFloat(asBytes)
    return asRpm
    
def resolveFloatValueRound(byteValues):
    return round(resolveFloatValue(byteValues))

def resolveDoubleValue(byteValues):
    asBytes = bytes(byteValues)
    asRpm = _resolveDouble(asBytes)
    return round(asRpm)

def resolveDoubleValueRound(byteValues):
    return round(resolveDoubleValue(byteValues))

def resolveBoolean(byteValues):
    return bool(byteValues[0])
