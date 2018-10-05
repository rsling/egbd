# -*- coding: utf-8 -*-


import argparse
import sys
import re


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input from SMOR (gzip)')
  parser.add_argument('outfile', help='output file name (gzip)')
  parser.add_argument('logfile', help='log file name (gzip)')
  parser.add_argument("--interactive", action='store_true', help="interactive mode")
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
    line = ifh.readline().decode('utf-8').strip()
    
    
    ofh.write(line.encode('utf-8') + '\n')


  ofh.close()
  lfh.close()

if __name__ == "__main__":
    main()
