import data_viz
import gzip
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import argparse
import random

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

    for i  in range(len(L)):
        curr =  L[i]
        if key == curr:
            return i
    return -1

def binary_serach(key, L):
    pass


def main():

    parser = argparse.ArgumentParser(description="A program for plotting boxplots from a set of genetic data")
    parser.add_argument("--gene_reads",
                        type = str,
                        default="GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz",
                        help="file to read genes from",
                        )
    parser.add_argument("--sample_attributes",
                        type = str,
                        default = 'GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt',
                        help = "file that contains samples",
                        )
    parser.add_argument("--gene",
                        required=True,
                        type = str,
                        help = "name of gene to pull groups from"
                        )
    parser.add_argument("--group_type",
                        required=True,
                        type = str,
                        help = "name of group to pull samples from",
                        )
    parser.add_argument("--output_file",
                            type = str,
                            help = "name of output file",
                            default="gtex.out",
                            )

    args = parser.parse_args()
    
    data_file_name = args.gene_reads
    sample_info_file_name= args.sample_attributes

    group_col_name = args.group_type
    sample_id_col_name = 'SAMPID'

    gene_name = args.gene

    samples = []
    sample_info_header = None
    for l in open(sample_info_file_name):
        if sample_info_header == None:
            sample_info_header = l.rstrip().split('\t')
        else:
            samples.append(l.rstrip().split('\t'))

    group_col_idx = linear_search(group_col_name, sample_info_header)
    sample_id_col_idx = linear_search(sample_id_col_name, sample_info_header)

    groups = []
    members = []

    for row_idx in range(len(samples)):
        sample = samples[row_idx]
        sample_name = sample[sample_id_col_idx]
        curr_group = sample[group_col_idx]

        curr_group_idx = linear_search(curr_group, groups)

        if curr_group_idx == -1:
            curr_group_idx = len(groups)
            groups.append(curr_group)
            members.append([])

        members[curr_group_idx].append(sample_name)

    version = None
    dim = None
    data_header = None

    gene_name_col = 1


    group_counts = [ [] for i in range(len(groups)) ]

    for l in gzip.open(data_file_name, 'rt'):
        if version == None:
            version = l
            continue

        if dim == None:
            dim = [int(x) for x in l.rstrip().split()]
            continue

        if data_header == None:
            data_header = []
            i = 0
            for field in l.rstrip().split('\t'):
                data_header.append(field)
                # data_header.append([field, i])
                i += 1
            # data_header.sort(key=lambda tup: tup[0])

            continue

        A = l.rstrip().split('\t')

        if A[gene_name_col] == gene_name:
            for group_idx in range(len(groups)):
                for member in members[group_idx]:
                    member_idx = linear_search(member, data_header)
                    if member_idx != -1:
                        group_counts[group_idx].append(int(A[member_idx]))
            break 

    data_viz.boxplot(group_counts, out_file_name = args.output_file, names=groups, x_label=group_col_name, y_label="Gene Read Counts", title=gene_name)

if __name__ == '__main__':
    main()
