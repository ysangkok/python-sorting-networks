#!/usr/bin/env python3
from itertools import takewhile, count
from copy import copy
import webbrowser, os, sys

def bitonic_merge(lo, cnt, di):
    if cnt <= 1: return
    k = cnt // 2;
    for i in range(lo, lo + k):
        yield (i, i + k) if di else (i + k, i)
    yield from bitonic_merge(lo, k, di);
    yield from bitonic_merge(lo + k, k, di);

def bitonic_sort(lo, cnt, di):
    if cnt <= 1: return
    k = cnt // 2;
    yield from bitonic_sort(lo, k, True);
    yield from bitonic_sort(lo + k, k, False);
    yield from bitonic_merge(lo, cnt, di);

def imperative_bitonic_sort(N):
  for k in takewhile(lambda x: x <= N, (2 ** x for x in count(1))):
    for j in takewhile(lambda x: x > 0, (k >> x for x in count(1))):
      for i in range(N):
        ij = i ^ j
        if ij > i:
          yield (ij, i) if (i & k) else (i, ij)

def oddeven_merge(lo, hi, r):
    step = r * 2
    if step < hi - lo:
        yield from oddeven_merge(lo, hi, step)
        yield from oddeven_merge(lo + r, hi, step)
        yield from [(i, i + r) for i in range(lo + r, hi - r, step)]
    else:
        yield (lo, lo + r)
 
def oddeven_merge_sort_range(lo, hi):
    if (hi - lo) < 1: return
    mid = lo + ((hi - lo) // 2)
    yield from oddeven_merge_sort_range(lo, mid)
    yield from oddeven_merge_sort_range(mid + 1, hi)
    yield from oddeven_merge(lo, hi, 1)
 
def compare_and_swap(x, a, b):
    if x[a] > x[b]:
        x[a], x[b] = x[b], x[a]

import random
orgdata = [random.randrange(1000) for i in range(2**int(sys.argv[1]))]
lens = []
for j, pairs_to_compare in enumerate([imperative_bitonic_sort(len(orgdata)), bitonic_sort(0, len(orgdata), True), oddeven_merge_sort_range(0, len(orgdata)-1)]):
    data = copy(orgdata)
    pairs_to_compare = list(pairs_to_compare)
    lens.append(len(pairs_to_compare))
    filename = "{}.svg".format(j)
    st = ""
    for k, i in enumerate(pairs_to_compare):
      st += '<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" />\n'.format(x1=(k+1), y1=(i[0]+1), x2=(k+1), y2=(i[1]+1))
      compare_and_swap(data, *i)
    with open(filename, "w") as f:
      print(pairs_to_compare)
      ma = max(pairs_to_compare, key=lambda x: x[0])[0]+2
      f.write('<svg viewBox="0 0 {} {}" version="1.1" xmlns="http://www.w3.org/2000/svg"><g stroke="black" stroke-width="0.5">'.format(len(pairs_to_compare)+1, ma))
      f.write(st)
      f.write("</g></svg>")
    #webbrowser.open_new_tab(filename)
    
    assert sorted(orgdata) == data, data

print(lens)
os.system("google-chrome ?.svg")
