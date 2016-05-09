#!/usr/bin/env python
import argparse
import collections
from itertools import groupby

__author__ = "Gene Blanchard"
__email__ = "me@geneblanchard.com"

'''
Find and remove xtons in fasta file
'''


def fasta_iter(fasta_name):
    with open(fasta_name, 'r') as fasta_handle:
        # ditch the boolean (x[0]) and just keep the header or sequence since we know they alternate.
        fasta_iter = (x[1] for x in groupby(fasta_handle, lambda line: line[0] == ">"))
        for header in fasta_iter:
            # drop the ">"
            name = header.next()[1:].strip()
            # join all sequence lines to one.
            seq = "".join(s.strip() for s in fasta_iter.next())
            yield name, seq


def fasta_writer(name, seq, handle):
    handle.write(">{}\n{}\n".format(name, seq))


def main():
    # Argument Parser
    parser = argparse.ArgumentParser(description='Find and remove x-ton from a filtered.fna file')

    # Input file
    parser.add_argument('-i', '--input', dest='input', required=True, help='The filtered.fna file')
    # Output file
    parser.add_argument('-o', '--output', dest='output', required=True, help='The output file')
    # The Xton to discard
    parser.add_argument('-x', '-xton', dest='xton', type=int, default=1, help='the number less than or equal to how many times to see a sequence before filtering. i.e. singletons are <= 1, therefore -x == 1 DEFAULT=1')

    # Parse arguments
    args = parser.parse_args()
    infile = args.input
    outfile = args.output
    xton = args.xton

    print "Step 1: Compiling Sequence Dictionary"
    seq_dict = collections.defaultdict(list)
    for name, seq in fasta_iter(infile):
        seq_dict[seq].append(name)

    print "Step 2: Counting Sequences"
    valid_seqs = [key for key in seq_dict.keys() if len(seq_dict[key]) > xton]
    print "Step 3: Writing Output"
    with open(outfile, 'w') as fasta_out:
        [fasta_writer(name, seq, fasta_out) for seq in valid_seqs for name in seq_dict[seq]]

if __name__ == '__main__':
    main()
