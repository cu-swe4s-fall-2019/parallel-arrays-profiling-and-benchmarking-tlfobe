# parallel-arrays-profiling-and-benchmarking
Parallel Arrays, Profiling, and Benchmarking

This is a repository where we will Benchmark datavisualization software based on the search method used to query arrays.

## Installation
This package depends on matplotlib and numpy, so please install those first before trying to run anything:

```
conda install matplotlib --yes
conda install numpy --yes
```

## Usage

There are two scripts with different implementations `plot_gtex.py` is the linear searching implementation of the data visualization and `plot_gtex_binary.py` is the binary searching implementation.

Both can be run as follows:

```
python plot_gtex.py --gene_reads GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz --sample_attributes GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt --gene ACTA2 --group_type SMTS --output_file ACTA2.png
```
This program requires a `gene_reads` for where the biological data is stored, `sample_attributes` lists all the genes possible, `gene` is the specific gene you'd like to visualize, `output_file` is the file you will output your visualization to.