import random
import argparse
import matplotlib.pyplot as plt
import data_viz
import gzip
import matplotlib
import time
import sys
sys.path.insert(1, "hash-tables-tlfobe")  # noqa: E402
import hash_tables
import hash_functions
matplotlib.use("Agg")


def linear_search(key, L):
    """
    linearly search for a value in an array

    Arguments
    ---------
    key : anything
    L : list of anythings
        list to search over

    Returns
    -------
    i : int
        index of matching value
    """

    for i in range(len(L)):
        curr = L[i]
        if key == curr:
            return i
    return -1


def main():

    parser = argparse.ArgumentParser(
        description="A program for plotting boxplots from a " +
                    "set of genetic data"
    )
    parser.add_argument("--gene_reads",
                        type=str,
                        default="GTEx_Analysis_2017-06-05_" +
                        "v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz",
                        help="file to read genes from",
                        )
    parser.add_argument("--sample_attributes",
                        type=str,
                        default='GTEx_Analysis_v8_Annotations' +
                        '_SampleAttributesDS.txt',
                        help="file that contains group_to_ID_hash_map",
                        )
    parser.add_argument("--gene",
                        required=True,
                        type=str,
                        help="name of gene to pull groups from"
                        )
    parser.add_argument("--group_type",
                        required=True,
                        type=str,
                        help="name of group to pull group_to_ID_hash_map from",
                        )
    parser.add_argument("--output_file",
                        type=str,
                        help="name of output file",
                        default="gtex.png",
                        )

    parser.add_argument("--benchmarking",
                        type=str,
                        help="whether or not to benchmark performance",
                        default="False",
                        )

    args = parser.parse_args()

    if eval(args.benchmarking):
        t0 = time.time()

    data_file_name = args.gene_reads
    sample_info_file_name = args.sample_attributes

    group_col_name = args.group_type
    sample_id_col_name = 'SAMPID'

    gene_name = args.gene

    header_to_group = hash_tables.ChainedHash(hash_functions.h_rolling, 50)
    groups_unique = []
    sample_info_header = None

    # map from headers to sample of specific column
    try:
        for l in open(sample_info_file_name):
            # print('loop 1')
            if sample_info_header is None:
                sample_info_header = l.rstrip().split('\t')
            else:
                data_array = l.rstrip().split('\t')
                for header_name, value in zip(sample_info_header, data_array):
                    if header_name != group_col_name \
                            and header_name != sample_id_col_name:
                        continue
                    else:
                        # print('loop 1.1')
                        if header_name not in header_to_group.keys:
                            header_to_group.add(header_name, [value])
                        else:
                            if header_name == group_col_name \
                                    and value not in groups_unique:
                                groups_unique.append(value)
                            loc = header_to_group.search(header_name)
                            loc.append(value)
    except FileNotFoundError:
        print("Please supply a valid sample attributes file!", file=sys.stderr)
        exit(1)
    except IsADirectoryError:
        print(sample_info_file_name + " is a directory! Please supply a " +
              " valid sample attributes file!", file=sys.stderr)
        exit(1)

    sample_ids = header_to_group.search(sample_id_col_name)

    # map of groups of specific header to samp_ids

    try:
        groups = header_to_group.search(group_col_name)
    except KeyError:
        print("Please supply a valid group_col_name!", file=sys.stderr)
        exit(1)
    groups_to_samp_ids = hash_tables.ChainedHash(
        hash_functions.h_rolling, 10000)

    for g_id, group in zip(sample_ids, groups):
        # print('loop 2')
        if group not in groups_to_samp_ids.keys:
            groups_to_samp_ids.add(group, [g_id])
        else:
            loc = groups_to_samp_ids.search(group)
            loc.append(g_id)

    # map of ids to genes

    version = None
    dim = None
    data_header = None
    gene_name_col = 1
    samp_id_to_gene_count = hash_tables.ChainedHash(
        hash_functions.h_rolling, 10000)

    try:
        for l in gzip.open(data_file_name, 'rt'):
            # print('loop 3')
            if version is None:
                version = l
                continue

            if dim is None:
                dim = [int(x) for x in l.rstrip().split()]
                continue

            if data_header is None:
                data_header = []
                i = 0
                data_header = l.rstrip().split('\t')
                continue
            A = l.rstrip().split('\t')

            if A[gene_name_col] == gene_name:
                for header, gene_data in zip(data_header[2:], A[2:]):
                    # print('loop 3.1')
                    if header not in samp_id_to_gene_count.keys:
                        samp_id_to_gene_count.add(header, gene_data)
                    else:
                        loc = samp_id_to_gene_count.search(header)
                        loc.append(gene_data)
                        # print(loc)
    except FileNotFoundError:
        print("Please supply a valid gene reads file!", file=sys.stderr)
        exit(1)
    except IsADirectoryError:
        print(data_file_name + " is a directory! Please supply a " +
              " valid gene reads file!", file=sys.stderr)
        exit(1)

    if samp_id_to_gene_count.capacity == 0:
        print("Gene supplied is not within dataset!" +
              " Please try with a valid gene!",
              file=sys.stderr)
        exit(1)
    group_counts = [[] for _ in range(len(groups_unique))]

    for i in range(len(groups_unique)):
        # print(groups_unique[i])
        # print(groups_to_samp_ids.search(groups_unique[i]))
        for id in groups_to_samp_ids.search(groups_unique[i]):
            if id in samp_id_to_gene_count.keys:
                # print(j)
                group_counts[i].append(int(samp_id_to_gene_count.search(id)))
            else:
                continue
    if eval(args.benchmarking):
        t1 = time.time()    # print(group_counts)
        print("DONE! Time =", t1 - t0)

    data_viz.boxplot(group_counts, out_file_name=args.output_file,
                     names=groups_unique, x_label=group_col_name,
                     y_label="Gene Read Counts", title=gene_name)
    if eval(args.benchmarking):
        t2 = time.time()
        print("IMAGE PRINTED! Time =", t2 - t1)
    print("COMPLETE!")


if __name__ == '__main__':
    main()
