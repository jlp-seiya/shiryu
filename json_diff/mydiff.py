import itertools

def diff(a, b):
    aout = []
    bout = []
    diff_recursive(a, b, aout, bout, 0)

    output = []
    for ao, bo in itertools.izip_longest(aout, bout):
        output.append("%-20s  |  %-20s" % (ao, bo))

    for o in output:
        print(o)

def diff_recursive(a, b, aout, bout, indent):
    a_type = type(a)
    b_type = type(b)

    space = ' ' * indent
    if a_type != b_type:
        add_block(a, aout, indent + 1)
        add_block(b, bout, indent + 1)
 
    elif isinstance(a, dict):
        a_keys = a.keys()
        b_keys = b.keys()
        all_keys = set().union(a_keys, b_keys)
        first = True
        add_begin_block("{", aout, indent)
        add_begin_block("{", bout, indent)
        for key in all_keys:
            if key in a:
                if key in b:
                    diff_recursive(a[key], b[key], aout, bout, indent + 1)
                else:
                    add_block(a[key], aout, indent + 1)
                    add_empty_block(bout)

            else:
                if key in b:
                    add_block(b[key], bout, indent + 1)
                    add_empty_block(aout)
                else:
                    raise Exception("Unknow key:%s" % key)
            first = False
        add_end_block("}", aout, indent)
        add_end_block("}", bout, indent)
    elif isinstance(a, list):
        a_size = len(a)
        b_size = len(b)
        max_size = max(a_size, b_size)
        min_size = min(a_size, b_size)
        for i in range(0, min_size):
            diff_recursive(a[i], b[i], aout, bout, indent + 1)

        first = (min_size == 0)
        if a_size > b_size:
            aout.append("===ORIGINAL===")
            bout.append("===BLANK===")

            for i in range(b_size, a_size):
                to_string2(a[i], aout, bout, first)
                first = False
            aout.append("===ORIGINAL===")
            bout.append("===BLANK===")
        else:
            bout.append("===NEW===")
            aout.append("===BLANK===")
            for i in range(a_size, b_size):
                to_string2(b[i], bout, aout, first)
                first = False
            bout.append("===NEW===")
            aout.append("===BLANK===")
    else:
        if a != b:
            aout.append("===DIFFVAR===")
            bout.append("===DIFFVAR===")
        if isinstance(a, str):
            aout.append('%s "%s"' % (space, a))
            bout.append('%s "%s"' % (space, b))
        else:
            aout.append('%s %s' % (space, a))
            bout.append('%s %s' % (space, b))

        if a != b:
            aout.append("===DIFFVAR===")
            bout.append("===DIFFVAR===")

def add_begin_block(sym, aout, indent):
    space = ' ' * indent
    block = {}
    lines = []
    block["lines"] = lines
    lines.append('%s%s' % (sym, space))

def add_end_block(sym, aout, indent):
    space = ' ' * indent
    block = {}
    lines = []
    block["lines"] = lines
    lines.append('%s%s' % (sym, space))

def add_empty_block(aout):
    block = {}
    block["type"] = "empty"
    block["lines"] = []
    aout.append(block)

def add_block(a, aout, indent):
    block = {}
    lines = []
    block["lines"] = lines
    to_string(a, lines, indent)
    aout.append(block)

def to_string(a, lines, indent):
    space = ' ' * indent
    if isinstance(a, dict):
        lines.append('%s{' % space)
        first = True
        for key in a.keys():
            if not first:
                lines[-1] += ','
            lines.append('%s "%s" : ' % (space, key))
            to_string(a[key], lines, indent + 1)
            first = False
        lines.append('%s}' % space)
    elif isinstance(a, list):
        lines.append('%s[' % space)

        first = True
        for val in a:
            if not first:
                lines[-1] += ','
            to_string(val, lines, indent + 1)
            first = False
        lines.append('%s]' % space)
    else:
        if isinstance(a, str) or isinstance(a, unicode):
            lines.append('%s "%s"' % (space, a))
        else:
            lines.append('%s %s' % (space, str(a)))

 

def to_string2(a, aout, bout, indent):
    space = ' ' * indent
    if isinstance(a, dict):
        aout.append('%s{' % space)
        bout.append('===BLANK===')
        first = True
        for key in a.keys():
            if not first:
                aout[-1] += ","
            aout.append('%s "%s" : ' % (space, key))
            bout.append('')
            to_string2(a[key], aout, bout, indent + 1)
            first = False
        aout.append('%s}' % space)
        bout.append('===BLANK===')
    elif isinstance(a, list):
        aout.append('%s[' % space)
        bout.append('===BLANK===')
        first = True
        for val in a:
            if not first:
               aout[-1] += ","
            to_string2(val, aout, bout, indent + 1)
            first = False
        aout.append('%s]' % space)
        bout.append('===BLANK===')
    else:
        if isinstance(a, str):
            aout.append('%s "%s"' % (space, a))
        else:
            aout.append('%s %s' % (space, str(a)))
        bout.append('')
