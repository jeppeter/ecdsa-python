

class File:

    @classmethod
    def read(cls, path, mode="r"):
        with open(path, mode) as blob:
            content = blob.read()
        return content

def dump_bytes(inb,note=''):
    rets = '%s'%(note)
    idx = 0
    lastidx = 0
    for b in inb:
        if (idx % 16) == 0:
            if idx > 0:
                rets += '    '
                while lastidx != idx:
                    curv = inb[lastidx]
                    if curv >= ord(' ') and curv <= ord('~'):
                        rets += '%c'%(curv)
                    else:
                        rets += '.'
                    lastidx += 1
            rets += '\n0x%08x'%(idx)
        rets += ' 0x%02x'%(b)
        idx += 1

    if idx != lastidx:
        while (idx % 16) != 0:
            rets += '     '
            idx += 1
        rets += '    '
        while lastidx < len(inb):
            curv = inb[lastidx]
            if curv >= ord(' ') and curv <= ord('~'):
                rets += '%c'%(curv)
            else:
                rets += '.'
            lastidx += 1
        rets += '\n'
    return rets

def dump_int(intv, note=''):
    sarr = []
    lastv = intv
    while lastv > 0:
        curv = lastv & 0xff
        sarr.insert(0,curv)
        lastv = lastv >> 8

    rets = '%s'%(note)
    idx = 0
    lastidx = 0
    while idx < len(sarr):
        if (idx % 16) == 0:
            if idx > 0:
                rets += '    '
                while lastidx != idx:
                    curv = sarr[lastidx]
                    if curv >= ord(' ') and curv <= ord('~'):
                        rets += '%c'%(curv)
                    else:
                        rets += '.'
                    lastidx += 1
            rets += '\n0x%08x'%(idx)
        rets += ' 0x%02x'%(sarr[idx])
        idx += 1

    if idx != lastidx:
        while (idx % 16) != 0:
            rets += '     '
            idx += 1
        rets += '    '
        while lastidx < len(sarr):
            curv = sarr[lastidx]
            if curv >= ord(' ') and curv <= ord('~'):
                rets += '%c'%(curv)
            else:
                rets += '.'
            lastidx += 1
        rets += '\n'
    return rets