"""Utility routines for working with WMT components."""

import os


# See https://stackoverflow.com/a/21499676/1563298
def commonpath(l):
    cp = []
    ls = [p.split(os.path.sep) for p in l]
    ml = min(len(p) for p in ls)

    for i in range(ml):
        s = set(p[i] for p in ls)
        if len(s) != 1:
            break
        cp.append(s.pop())

    return os.path.sep.join(cp)
