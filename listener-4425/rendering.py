# Printing the GraphViz graph

def render_sequence(s):
    """
    Given an enumerable s of integers, return a compressed readable
    form of that list of numbers as a string, e.g. [1,2,3] = "1-3", etc
    """
    if len(s) == 0:
        return ""
    s=list(sorted(s))
    startidx = 0
    curridx = 1
    retval = str(s[0])

    while curridx < len(s):
        if s[curridx-1]+1 == s[curridx]:
            # numbers are sequential
            pass
        elif curridx - startidx == 1:
            retval += "," + str(s[curridx])
            startidx = curridx
        elif curridx - startidx == 2:
            retval += "," + str(s[curridx-1]) + "," + str(s[curridx])
            startidx = curridx
        else:
            retval += "-" + str(s[curridx-1]) + "," + str(s[curridx])
            startidx = curridx
        curridx += 1

    if (len(s)-1) - startidx == 0:
        pass
    elif (len(s)-1) - startidx == 1:
        retval += "," + str(s[-1])
    else:
        retval += "-" + str(s[-1])

    return retval


def print_graph(connections, possibles):
    """Prints the GraphViz formatted graph"""
    # print header
    print("""\
digraph N {
    rankdir=RL;
""")

    # print connections
    for key in sorted(connections):
        for connection in sorted(connections[key]):
            print("""\
    {} -> {};""".format(key, connection))

    # print labels
    for key in sorted(possibles):
        if len(possibles[key]) == 1:
            completed_style = "style=filled"
        else:
            completed_style = ""
        print("""\
    {key} [label="{key}\\n{values}" {completed_style}]""".format(
            key=key,
            values=render_sequence(sorted(possibles[key])),
            completed_style=completed_style))

    print("""\
}""")
