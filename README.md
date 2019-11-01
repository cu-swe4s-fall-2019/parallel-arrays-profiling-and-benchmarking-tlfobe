# parallel-arrays-profiling-and-benchmarking

[![Build Status](https://travis-ci.com/cu-swe4s-fall-2019/parallel-arrays-profiling-and-benchmarking-tlfobe.svg?branch=master)](https://travis-ci.com/cu-swe4s-fall-2019/parallel-arrays-profiling-and-benchmarking-tlfobe)

Parallel Arrays, Profiling, and Benchmarking

This is a repository where we will Benchmark datavisualization software based on the search method used to query arrays.

## Installation
This package depends on matplotlib and numpy, so please install those first before trying to run anything:

```
conda install matplotlib --yes
conda install numpy --yes
```

## Usage

There are two scripts with different implementations `plot_gtex.py` is the parallel array implementation of the data visualization and `plot_gtex_hash_tables.py` is the hash table implementation of the data visualization.

Both can be run as follows:

```
python plot_gtex.py --gene_reads GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz --sample_attributes GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt --gene ACTA2 --group_type SMTS --output_file ACTA2.png
```
This program requires a `gene_reads` for where the biological data is stored, `sample_attributes` lists all the genes possible, `gene` is the specific gene you'd like to visualize, `output_file` is the file you will output your visualization to.

