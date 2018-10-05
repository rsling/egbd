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
  positions = [(i - 1, get_tipa_end(line, i)) for i in positions]
  return positions


# I don't care if the implementation is inefficient. We're talking abt a few seconds per file.
def handle_replacements(line, pos, repl, log):

  # Start with prefix before first match.
  out = line[0:pos[0][0]]
  for i in range(0, len(pos)):
    log.write(line[pos[i][0] : pos[i][1]].encode('utf-8') + '\t')
    match = line[pos[i][0]+9 : pos[i][1]-1]

    # Handle Silbengelenk.
    match = re.sub(r'\\Sgel\{(.)\}', u'\\1\u0323', match, re.UNICODE)

    # Do the actual replacements.
    for r in repl:
        match = match.replace(r[0], r[1])

    # Ligature and ungespannt handling – assuming all macros have been reduced to simple characters!
    match = re.sub(r'\\t\{(.)(.)\}', u'\\1\u0361\\2', match, re.UNICODE)
    match = re.sub(r'\\u\{(.)\}', u'\\1\u0306', match, re.UNICODE)
    match = re.sub(r'\\s\{(.)\}', u'\\1\u0329', match, re.UNICODE)

    # Clean up spaces.
    match = match.replace(' ', '')

    log.write(match.encode('utf-8') + '\n')

    if i == len(pos)-1:
      suffix = line[pos[i][1]:len(line)]
    else:
      suffix = line[pos[i][1]:pos[i+1][0]]
    out = out + match + suffix
  #print out.encode('utf-8')
  return out 


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='input UTF-8 TeX file')
  parser.add_argument('outfile', help='output UTF-8 TeX file')
  parser.add_argument('replacements', help='file (UTF-8) with replacement table')
  parser.add_argument('logfile', help='log file name (gzip)')
  parser.add_argument("--interactive", action='store_true', help="interactive mode")
  parser.add_argument("--erase", action='store_true', help="erase existing output files")
  args = parser.parse_args()


  # Check input files.
  infiles = [args.infile, args.replacements]
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

  # Read replacements.
  with open(args.replacements, 'r') as repl:
    replstrings = repl.read().splitlines()
  replacements = [(l[0].decode('utf-8'), l[-1].decode('utf-8')) for l in (line.split() for line in replstrings)]

  # Open output files.
  ofh = open(args.outfile, 'wb')
  lfh = open(args.logfile, 'wb')

  linenumber = 1
  for line in open(args.infile, 'r'):
    line = line.decode('utf-8').strip('\n') # Do not strip whitespace b/o indentation.
    
    pos = find_tipa_positions(line)
    # print pos

    if len(pos) == 0:
      ofh.write(line.encode('utf-8') + '\n')
    else:
      lfh.write(str(linenumber) + '\n')
      newline = handle_replacements(line, pos, replacements, lfh)
      ofh.write(newline.encode('utf-8') + '\n')

    linenumber = linenumber + 1

  ofh.close()
  lfh.close()

if __name__ == "__main__":
    main()
