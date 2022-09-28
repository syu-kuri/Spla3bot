def hiraToKata(target):
    return ''.join([chr(n + 96) if (12352 < n and n < 12439) or n == 12445 or n == 12446 else chr(n) for n in [ord(c) for c in target]])