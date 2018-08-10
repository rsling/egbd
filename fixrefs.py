# -*- coding: utf-8 -*-

import argparse
import os.path
import sys
import gzip
import re
import glob

RE_SEC=r'\\(?:(?:|sub|subsub)section|chapter)(?:\*{0,1}){(.+)$'
RE_SLA=r'\\label\{(sec:[^}]+)\}'
RE_LAB=r'\\label\{(fig|tab|ex|it|abs):([^}]+)\}'
RE_REF=r'\\(?:ref|pageref)\{((?:sec|subsec|subsubsec|fig|tab|ex|it|abs):[^}]+)\}'

def extract_label(s):
  r = u''
  opened=0
  for c in range(0, len(s)):
    if s[c] == u'{': opened = opened + 1
    elif s[c] == u'}': opened = opened - 1
    if opened < 0:
      r = s[:c]
      break
  return r

def labelify(s):
  s = re.sub(r'\\[^{]+\{([^}]+)\}', r'\1', s)
  s = s.lower()
  s = s.replace(u'ä',u'ae').replace(u'ö',u'oe').replace(u'ü',u'ue').replace(u'ß',u'ss').replace(u' ',u'')
  s = re.sub(r'[^a-z]+', '', s)
  return s


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('infiles', help='TeX input file mask (put in quotes!)')
  parser.add_argument('outfile', help='TeX output file prefix')
  parser.add_argument("--erase", action='store_true', help="erase outout files if present")
  args = parser.parse_args()

  listing = glob.glob(args.infiles)

  # Check input files.
  for fn in listing:
    if not os.path.exists(fn):
      sys.exit("Input file does not exist: " + fn)

  # We record all changed keys in this.
  changes = dict()

  # First pass: make changes to keys.
  seen_sec = set()
  for fn in listing:
    with open(fn) as f:
      intex = f.read().splitlines()
    intex = [x.decode('utf-8') for x in intex]
 
    # Determine which section we are in and set new sec name.
    this_sec = u''
    maxi = len(intex)
    i = 0
    cnt_labs = 1
    while i < maxi:
      l = intex[i]
      the_match=re.search(RE_SEC, l, re.UNICODE)
      if the_match:
        this_sec = 'sec:' + labelify(extract_label(the_match.group(1)))
        while this_sec in seen_sec:
          this_sec = this_sec + '0'
        seen_sec.add(this_sec)
        intex.insert(i+1, '\\label{' + this_sec + '}')
        i = i + 1
        maxi = maxi + 1
      else:

        # Remove old section labels.
        old_lab = re.search(RE_SLA, l, re.UNICODE)
        if old_lab:
          intex[i] = re.sub(RE_SLA, r'', l, re.UNICODE)

          # Add to replacement table.
          changes[old_lab.group(1)] = this_sec

        # Replace old other (fig, tab, ex, it, abs) labels.
        the_matches = re.findall(RE_LAB, l, re.UNICODE)
        if the_matches:
          for ma in the_matches:
            the_old = ma[0] + ':' + ma[1]
            the_new = ma[0] + ':' + this_sec[4:] + format(cnt_labs, '03d')
            changes[the_old] = the_new
            intex[i] = l.replace(the_old, the_new)
            cnt_labs += 1
  
      # Next round of loop.
      i = i + 1

    with open(fn, 'w') as the_file:
      lastli = False
      for li in intex:
        if not (lastli and not li):
          the_file.write((li + '\n').encode('utf-8'))
        if not li: lastli = True
        else: lastli = False

  with open('__debug.txt', 'w') as debug:
    for k, v in changes.items():
      debug.write((k + '\t' + v + '\n').encode('utf-8'))

 
  # Second pass: fix the references.
  for fn in listing:
    with open(fn) as f:
      intex = f.read().splitlines()
    intex = [x.decode('utf-8') for x in intex]

    for i in range(0,len(intex)):
      l = intex[i]
      the_matches = re.findall(RE_REF, l, re.UNICODE)
      if the_matches:
        for ma in the_matches:
          the_old = ma
          the_new = changes[the_old]
          intex[i] = intex[i].replace(the_old, the_new)

    with open(fn, 'w') as the_file:
      for li in intex:
        the_file.write((li + '\n').encode('utf-8'))

if __name__ == "__main__":
  main()

