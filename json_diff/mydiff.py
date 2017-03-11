import itertools
import logging

INDENT = "&emsp;"
def diff(a, b):
    aout = []
    bout = []
    diff_recursive(a, b, aout, bout, 0, True, True)

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
    diff_recursive(a, b, aout, bout, 0, True, True)

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
            if a_len == 0:
                left_output.append('<span style="background-color: #DAF7A6">')
                right_output.append('<span style="background-color: #DAF7A6">')
            elif b_len == 0:
                left_output.append('<span style="background-color: #F08080">')
                right_output.append('<span style="background-color: #F08080">')
            else:
                left_output.append('<span style="background-color: #f7dc6f">')
                right_output.append('<span style="background-color: #f7dc6f">')

            if a_len >= b_len:
                for i in range(0, a_len):
                    left_output.append(ao["lines"][i])
                for i in range(0, b_len):
                    right_output.append(bo["lines"][i])
                for i in range(b_len, a_len):
                    right_output.append(INDENT + "<br/>")
            else:
                for i in range(0, a_len):
                    left_output.append(ao["lines"][i])
                for i in range(0, b_len):
                    right_output.append(bo["lines"][i])
                for i in range(a_len, b_len):
                    left_output.append(INDENT + "<br/>")
            left_output.append('</span>')
            right_output.append('</span>')
    
    print("\n".join(left_output))
    print("\n".join(right_output))
    return (left_output, right_output)
    
def make_html_line(a, lines, block_type):
    if block_type.startswith("same"):
        lines.appennd(a)
    else:
        lines.append

def diff_recursive(a, b, aout, bout, indent, a_last, b_last):
    a_type = type(a)
    b_type = type(b)

    space = INDENT * indent
    if a_type != b_type:
        add_block(a, aout, indent + 1, a_last, "diff")
        add_block(b, bout, indent + 1, b_last, "diff")
 
    elif isinstance(a, dict):
        a_keys = a.keys()
        b_keys = b.keys()
        all_keys = set().union(a_keys, b_keys)
        add_begin_block("{", aout, indent)
        add_begin_block("{", bout, indent)
        a_i = 0
        b_i = 0
        a_len = len(a)
        b_len = len(b)
        for key in all_keys:
            if key in a:
                a_i += 1
                if key in b:
                    b_i +=1
                    add_key_block(key, aout, indent + 1, "same")
                    add_key_block(key, bout, indent + 1, "same")
                    diff_recursive(a[key], b[key], aout, bout, indent + 1,
                        a_i == a_len, b_i == b_len)
                else:
                    add_key_block(key, aout, indent + 1, "diff")
                    add_block(a[key], aout, indent + 1, a_i == a_len, "diff")
                    add_empty_block(bout)
                    add_empty_block(bout)

            else:
                if key in b:
                    b_i += 1
                    add_key_block(key, bout, indent + 1, "diff")
                    add_block(b[key], bout, indent + 1, b_i == b_len, "diff")
                    add_empty_block(aout)
                    add_empty_block(aout)
                else:
                    raise Exception("Unknow key:%s" % key)
        add_end_block("}", aout, indent, a_last)
        add_end_block("}", bout, indent, b_last)
    elif isinstance(a, list):
        a_size = len(a)
        b_size = len(b)
        max_size = max(a_size, b_size)
        min_size = min(a_size, b_size)
        add_begin_block('[', aout, indent)
        add_begin_block('[', bout, indent)
        i = 0
        while i < min_size:
            diff_recursive(a[i], b[i], aout, bout, indent + 1, i == a_size - 1, i == b_size - 1)
            i += 1
        if a_size >= b_size:
            while i < a_size:
                add_block(a[i], aout, indent + 1, i == a_size - 1, "diff")
                add_empty_block(bout)
                i += 1
        else:
            while i < b_size:
                add_block(b[i], bout, indent + 1, i == b_size - 1, "diff")
                add_empty_block(aout)
                i += 1
        add_end_block(']', aout, indent, a_last)
        add_end_block(']', bout, indent, b_last)

    else:
        if a == b:
            add_block(a, aout, indent, a_last, "same")
            add_block(b, bout, indent, b_last, "same")
        else:
            add_block(a, aout, indent, a_last, "diff")
            add_block(b, bout, indent, b_last, "diff")

def add_begin_block(sym, aout, indent):
    space = INDENT * indent
    block = {}
    lines = []
    block["lines"] = lines
    block["type"] = "same-begin"
    lines.append('%s%s<br/>' % (space, sym))
    aout.append(block)

def add_end_block(sym, aout, indent, is_last):
    space = INDENT * indent
    block = {}
    lines = []
    block["lines"] = lines
    block["type"] = "same-end"
    if is_last:
        lines.append('%s%s<br/>' % (space, sym))
    else:
        lines.append('%s%s,<br/>' % (space, sym))

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
    lines.append('%s"%s" :<br/>' % (space, key))
    aout.append(block)

def add_block(a, aout, indent, is_last, same):
    block = {}
    lines = []
    block["lines"] = lines
    block["type"] = same + "-regular"
    to_string(a, lines, indent, is_last)
    aout.append(block)

def to_string(a, lines, indent, is_last):
    space = INDENT * indent
    if isinstance(a, dict):
        lines.append('%s{<br/>' % space)
        i = 0
        a_len = len(a)
        for key in a.keys():
            i += 1
            lines.append('%s%s"%s" :<br/>' % (space, INDENT, key))
            to_string(a[key], lines, indent + 1, i == a_len)
        if is_last:
            lines.append('%s}<br/>' % space)
        else:
            lines.append('%s},<br/>' % space)
    elif isinstance(a, list):
        lines.append('%s[<br/>' % space)
        i = 0
        a_len = len(a)
        for val in a:
            i += 1
            to_string(val, lines, indent + 1, i == a_len)
        if is_last:
	    lines.append('%s]<br/>' % space)
        else:
	    lines.append('%s],<br/>' % space)
    else:
        if is_last:
            if isinstance(a, str) or isinstance(a, unicode):
                lines.append('%s"%s"<br/>' % (space, a))
            else:
                lines.append('%s%s<br/>' % (space, str(a)))
        else:
            if isinstance(a, str) or isinstance(a, unicode):
                lines.append('%s"%s",<br/>' % (space, a))
            else:
                lines.append('%s%s,<br/>' % (space, str(a)))

 
