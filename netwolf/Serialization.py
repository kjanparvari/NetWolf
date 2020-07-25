import traceback
from bitstring import BitArray
from typing import List


def serialize(obj):
    from netwolf.Members import Member
    _bytes: bytes
    if isinstance(obj, List):
        if len(obj) > 0 and isinstance(obj[0], Member):
            _bytes = bytes("mem", 'utf-8')
            for m in obj:
                _bytes += bytes('$$$' + str(bytes(m), 'utf-8').replace("mem$$$", ""), 'utf-8')
        else:
            return b''
    else:
        _bytes = bytes(obj)
    _bits = BitArray(_bytes)
    for i in range(0, len(_bits)):
        if i % 3 == 0:
            _bits[i] = not _bits[i]
    result = _bits.bytes
    return result


def deserialize(s):
    try:
        from netwolf.Members import Member
        _bits = BitArray(s)
        for i in range(0, len(_bits)):
            if i % 3 == 0:
                _bits[i] = not _bits[i]
        _bytes = _bits.bytes
        lst = str(_bytes, 'utf-8').split("$$$")
        if lst[0] == 'mem':
            res = []
            for i in range(1, len(lst)):
                info = lst[i].split(":")
                name = info[0]
                ip = info[1]
                res.append(Member(name, ip))
            if len(res) == 1:
                return res[0]
            else:
                return res
        elif lst[0] == 'dis':
            from netwolf.Discovery import DiscoveryMessage
            members: List[Member] = []
            for i in range(1, len(lst)):
                info = lst[i].split(':')
                members.append(Member(info[0], info[1]))
            return DiscoveryMessage(members)
        else:
            pass
    except Exception as e:
        traceback.print_exc()
