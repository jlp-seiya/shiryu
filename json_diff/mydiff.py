import itertools
import logging

INDENT = "&emsp;"
def diff(a, b):
    aout = []
    bout = []
    diff_recursive(a, b, aout, bout, 0)

    output = []
    print("aout len:%d" % len(aout))
    print("bout len:%d" % len(bout))
    for ao, bo in itertools.izip_longest(aout, bout):
        a_len = len(ao["lines"])
        b_len = len(bo["lines"])
        max_len = max(a_len, b_len)
        min_len = min(a_len, b_len)
#        output.append("%-20s   |  %-20s" % (ao["type"], bo["type"]))
        for i in range(0, min_len):
            output.append("%-20s   |  %-20s" % (ao["lines"][i], bo["lines"][i]))
        if a_len >= b_len:
            for i in range(b_len, max_len):
                output.append("%-20s   |  %-20s" % (ao["lines"][i], ""))
        else:
            for i in range(a_len, max_len):
                output.append("%-20s   |  %-20s" % ("", bo["lines"][i]))

    for o in output:
        print(o)

    return output

def diff_html(a, b):
    aout = []
    bout = []
    diff_recursive(a, b, aout, bout, 0)

    left_output = []
    right_output = []
    for ao, bo in itertools.izip_longest(aout, bout):
        a_len = len(ao["lines"])
        b_len = len(bo["lines"])
        max_len = max(a_len, b_len)
        min_len = min(a_len, b_len)

        print("working on ao:%s" % ao)
        print("working on bo:%s" % bo)
        if ao["type"].startswith("same"):
            for i in range(0, max_len):
                left_output.append(ao["lines"][i])
                right_output.append(bo["lines"][i])
        else:
            if a_len >= b_len:
                for i in range(0, a_len):
                    left_output.append(ao["lines"][i])
                for i in range(0, b_len):
                    right_output.append(bo["lines"][i])
                for i in range(b_len, a_len):
                    right_output.append("")
            else:
                for i in range(0, a_len):
                    left_output.append(ao["lines"][i])
                for i in range(0, b_len):
                    right_output.append(bo["lines"][i])
                for i in range(a_len, b_len):
                    left_output.append("")
    
    print("\n".join(left_output))
    print("\n".join(right_output))
    return (left_output, right_output)
    

def diff_recursive(a, b, aout, bout, indent):
    a_type = type(a)
    b_type = type(b)

    space = INDENT * indent
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
                    add_key_block(key, aout, indent + 1, "same")
                    add_key_block(key, bout, indent + 1, "same")
                    diff_recursive(a[key], b[key], aout, bout, indent + 1)
                else:
                    add_key_block(key, aout, indent + 1, "diff")
                    add_block(a[key], aout, indent + 1)
                    add_empty_block(bout)
                    add_empty_block(bout)

            else:
                if key in b:
                    add_key_block(key, bout, indent + 1, "diff")
                    add_block(b[key], bout, indent + 1)
                    add_empty_block(aout)
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

    else:
        add_block(a, aout, indent + 1)
        add_block(b, bout, indent + 1)

def add_begin_block(sym, aout, indent):
    space = INDENT * indent
    block = {}
    lines = []
    block["lines"] = lines
    block["type"] = "same-begin"
    lines.append('%s%s' % (sym, space))
    aout.append(block)

def add_end_block(sym, aout, indent):
    space = INDENT * indent
    block = {}
    lines = []
    block["lines"] = lines
    block["type"] = "same-end"
    lines.append('%s%s' % (sym, space))
    aout.append(block)

def add_empty_block(aout):
    block = {}
    block["type"] = "diff-empty"
    block["lines"] = []
    aout.append(block)

def add_key_block(key, aout, indent, same):
    space = INDENT * indent
    block = {}
    lines = []
    block["lines"] = lines
    block["type"] = same + "-key"
    lines.append('%s"%s" :' % (space, key))
    aout.append(block)

def add_block(a, aout, indent):
    block = {}
    lines = []
    block["lines"] = lines
    block["type"] = "diff-regular"
    to_string(a, lines, indent)
    aout.append(block)

def to_string(a, lines, indent):
    space = INDENT * indent
    if isinstance(a, dict):
        lines.append('%s{' % space)
        first = True
        for key in a.keys():
            if not first:
                lines[-1] += ','
            lines.append('%s%s"%s" : ' % (space, INDENT, key))
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
            lines.append('%s"%s"' % (space, a))
        else:
            lines.append('%s%s' % (space, str(a)))

 
