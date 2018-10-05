# -*- coding: utf-8 -*-


import argparse
import sys
import os
import re


def get_tipa_end(line, start):
  stack = 0
  for i in range(start + 7, len(line)):
    if line[i] == u'{': stack = stack + 1
    elif line[i] == u'}': stack = stack - 1
    if stack == 0: break
  return i + 1


def find_tipa_positions(line):
  positions = list()
  for m in re.finditer(u'textipa', line, re.UNICODE):
    positions.append(m.start())
  positions = [(i-1, get_tipa_end(line, i)) for i in positions]
  return positions


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input from SMOR (gzip)')
  parser.add_argument('outfile', help='output file name (gzip)')
  parser.add_argument('logfile', help='log file name (gzip)')
  parser.add_argument("--interactive", action='store_true', help="interactive mode")
  parser.add_argument("--erase", action='store_true', help="erwase existing output files")
  args = parser.parse_args()


  # Check input files.
  infiles = [args.infile]
  for fn in infiles:
    if not os.path.exists(fn):
      sys.exit("Input file does not exist: " + fn)


  # Check (potentially erase) output files.
  outfiles = [args.outfile, args.logfile]
  for fn in outfiles:
    if fn is not None and os.path.exists(fn):
      if args.erase:
        try:
          os.remove(fn)
        except:
          sys.exit("Cannot delete pre-existing output file: " + fn)
      else:
        sys.exit("Output file already exists: " + fn)

  ofh = open(args.outfile, 'wb')
  lfh = open(args.logfile, 'wb')

  for line in open(args.infile, 'r'):
    line = line.decode('utf-8').strip('\n') # Do not strip whitespace b/o indentation.
    
    pos = find_tipa_positions(line)
    matches = [line[start:end] for (start,end) in pos]
    
    print matches
    
    ofh.write(line.encode('utf-8') + '\n')


  ofh.close()
  lfh.close()

if __name__ == "__main__":
    main()
