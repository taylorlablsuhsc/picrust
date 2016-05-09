#!/usr/bin/env python
import argparse

__author__ = "Gene Blanchard"
__email__ = "me@geneblanchard.com"

'''
Picrust SOP script
'''


def remove_xtons(fna, xton):
    outfile = "xton_{}_filtered.fna".format(xton)
    command = " echo 'Filtering {}-tons'\n".format(xton)
    command += "xton_remover.py -i {} -x {} -o {}\n".format(fna, xton, outfile)
    return outfile, command


def remove_chimeras(fna):
    outfile = "nonchimeric_{}".format(fna)
    command = " echo 'Removing Chimeras'\n"
    command += "vsearch --uchime_ref {} --db /media/nfs_opt/bin/gold.fa --nonchimeras {}\n".format(fna, outfile)
    return outfile, command


def create_params(method):
    param_name = "pick_closed_reference_otus_{}.params".format(method)
    with open(param_name, 'w') as paramsfile:
        if method == "uclust_usearch_ref":
            params = "pick_otus:otu_picking_method uclust\n"
            paramsfile.write(params)
        elif method == "usearch":
            params = "pick_otus:otu_picking_method usearch61_ref\n"
            paramsfile.write(params)
        elif method == "sortmerna":
            params = "pick_otus:otu_picking_method sortmerna\n"
            paramsfile.write(params)
    return param_name


def pick_closed_reference_otus(nonchimeras, threads, params):
    command = "echo 'Picking OTUs'\n"
    command += "pick_closed_reference_otus.py -i {} -o . -f -a -O {} -p {}".format(nonchimeras, threads, params)
    return command


def main():
    # Argument Parser
    parser = argparse.ArgumentParser(description='Create a picrust SOP shell script')

    # Input file
    parser.add_argument('-i', '--input', dest='input', required=True, help='The filtered.fna file')
    # The Xton to discard
    parser.add_argument('-x', '-xton', dest='xton', type=int, default=1, help='the number less than or equal to how many times to see a sequence before filtering. i.e. singletons are <= 1, therefore -x == 1 DEFAULT=1')
    # Threads
    parser.add_argument('-t', '--threads', dest='threads', type=int, default=32, help='Threads to use')
    # Method
    parser.add_argument('-m', '--method', dest='method', choices=['uclust', 'usearch', 'sortmerna'], help='OTU Picking Method: Valid choices are sortmerna, usearch61, and uclust')

    # Parse arguments
    args = parser.parse_args()
    infile = args.input
    xton = args.xton
    threads = args.threads
    method = args.method

    with open("pictust_pipeline.sh", 'w') as outfile:
        # XTon filter
        fna, command = remove_xtons(infile, xton)
        outfile.write(command)

        # Remove Chimeras
        nonchimeras, command = remove_chimeras(fna)
        outfile.write(command)

        # Create Parameters
        params = create_params(method)

        command = pick_closed_reference_otus(nonchimeras, threads, params)
        outfile.write(command)

if __name__ == '__main__':
    main()
