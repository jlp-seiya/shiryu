import itertools

def diff(a, b):
    aout = []
    bout = []
    diff_recursive(a, b, aout, bout)
    for ao, bo in itertools.izip_longest(aout, bout):
        print("%-20s  |  %-20s" % (ao, bo))

def diff_recursive(a, b, aout, bout):
    a_type = type(a)
    b_type = type(b)

    if a_type != b_type:
        aout.append("===DIFFTYPE===")
        bout.append("===DIFFTYPE===")
        aline = [0]
        bline = [0]
        to_string(a, aout, aline)
        to_string(b, bout, bline)
        if aline[0] > bline[0]:
            for i in range(0, aline[0] - bline[0]):
                bout.append('')
        else:
            for i in range(0, bline[0] - aline[0]):
                aout.append('')
        aout.append("===DIFFTYPE===")
        bout.append("===DIFFTYPE===")
 
    elif isinstance(a, dict):
        a_keys = a.keys()
        b_keys = b.keys()
        all_keys = set().union(a_keys, b_keys)
        for key in all_keys:
            if key in a:
                if key in b:
                    aout.append('{"%s":' % key)
                    bout.append('{"%s":' % key)
                    diff_recursive(a[key], b[key], aout, bout)
                    aout.append('}')
                    bout.append('}')
                else:
                    aout.append("===ORIGINAL===")
                    bout.append("===BLANK===")
                    aout.append('{"%s":' % key)
                    bout.append('')

                    to_string2(a[key], aout, bout)               

                    aout.append('}')
                    bout.append('')
                    aout.append("===ORIGINAL===")
                    bout.append("===BLANK===")
            else:
                if key in b:
                    bout.append("===NEW===")
                    aout.append("===BLANK===")
                    bout.append('{"%s":' % key)
                    aout.append('')

                    to_string2(b[key], bout, aout)               

                    bout.append('}')
                    aout.append('')
                    bout.append("===NEW===")
                    aout.append("===BLANK===")
                else:
                    raise Exception("Unknow key:%s" % key)
    elif isinstance(a, list):
        a_size = len(a)
        b_size = len(b)
        max_size = max(a_size, b_size)
        min_size = min(a_size, b_size)
        for i in range(0, min_size):
            diff_recursive(a[i], b[i], aout, bout)
        if a_size > b_size:
            aout.append("===ORIGINAL===")
            bout.append("===BLANK===")
            for i in range(b_size, a_size):
                to_string2(a[i], aout, bout)
            aout.append("===ORIGINAL===")
            bout.append("===BLANK===")
        else:
            bout.append("===NEW===")
            aout.append("===BLANK===")
            for i in range(a_size, b_size):
                to_string2(b[i], bout, aout)
            bout.append("===NEW===")
            aout.append("===BLANK===")
    else:
        if a == b:
            aout.append(a)
            bout.append(b)
        else:
            aout.append("===DIFFVAR===")
            aout.append(a)
            aout.append("===DIFFVAR===")
            bout.append("===DIFFVAR===")
            bout.append(b)
            bout.append("===DIFFVAR===")

def to_string(a, aout, aline):
    if isinstance(a, dict):
        for key in a.keys():
            aout.append('{"%s":' % key)
            aline[0] += 1
            to_string(a[key], aout, aline)
            aout.append('}')
            aline[0] += 1
    elif isinstance(a, list):
        aout.append('[')
        aline[0] += 1
        for val in a:
            to_string(val, aout, aline)
        aout.append(']')
        aline[0] += 1
    else:
        aout.append(a)
        aline[0] += 1

def to_string2(a, aout, bout):
    if isinstance(a, dict):
        for key in a.keys():
            aout.append('{"%s":' % key)
            bout.append('===BLANK===')
            to_string2(a[key], aout, bout)
            aout.append('}')
            bout.append('===BLANK===')
    elif isinstance(a, list):
        for val in a:
            aout.append('[')
            bout.append('===BLANK===')
            to_string2(val, aout, bout)
            aout.append(']')
            bout.append('===BLANK===')
    else:
        aout.append(a)
        bout.append('')
