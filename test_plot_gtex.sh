
#!/bin/bash
test -e ssshtest ||  wget -q http://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest


run test_hash_invalid_inputs python plot_gtex_hash_tables.py
assert_exit_code 2
assert_in_stderr usage:

run test_invalid_inputs python plot_gtex.py
assert_exit_code 2
assert_in_stderr usage:

run test_hash_incorrect_group_type_input python plot_gtex_hash_tables.py --gene_reads GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz --sample_attributes GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt --gene ACTA2 --group_type lmao
assert_exit_code 1
assert_in_stderr group_col_name

run test_hash_incorrect_gene_reads_input python plot_gtex_hash_tables.py --gene_reads not_a_file --sample_attributes GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt --gene ACTA2 --group_type SMTS
assert_exit_code 1
assert_in_stderr supply

run test_hash_incorrect_group_attributes_input python plot_gtex_hash_tables.py --gene_reads GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz --sample_attributes not_a_file.txt --gene ACTA2 --group_type SMTS
assert_exit_code 1
assert_in_stderr attributes

run test_incorrect_group_attributes_input python plot_gtex.py --gene_reads GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz --sample_attributes not_a_file.txt --gene ACTA2 --group_type SMTS
assert_exit_code 1
assert_in_stderr attributes

run test_incorrect_gene_reads_input python plot_gtex.py --gene_reads not_a_file --sample_attributes GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt --gene ACTA2 --group_type SMTS
assert_exit_code 1
assert_in_stderr supply

run test_incorrect_gene_inputs python plot_gtex.py --gene_reads GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz --sample_attributes GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt --gene haha --group_type SMTS
assert_exit_code 1
assert_in_stderr gene

run test_incorrect_group_type_input python plot_gtex.py --gene_reads GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz --sample_attributes GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt --gene ACTA2 --group_type lmao
assert_exit_code 1
assert_in_stderr group_col_name

run test_normal_plot_gtex python plot_gtex.py --gene_reads GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz --sample_attributes GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt --gene ACTA2 --group_type SMTS --output_file ACTA2.png
assert_exit_code 0
assert_in_stdout COMPLETE!

run test_hash_normal_plot_gtex python plot_gtex_hash_tables.py --gene_reads GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz --sample_attributes GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt --gene ACTA2 --group_type SMTS --output_file ACTA2.png
assert_exit_code 0
assert_in_stdout COMPLETE!

run test_benchmark_plot_gtex python plot_gtex.py --gene_reads GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz --sample_attributes GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt --gene ACTA2 --group_type SMTS --output_file ACTA2.png --benchmark True
assert_exit_code 0
assert_in_stdout Time

run test_hash_benchmark_plot_gtex python plot_gtex_hash_tables.py --gene_reads GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz --sample_attributes GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt --gene ACTA2 --group_type SMTS --output_file ACTA2.png --benchmark True
assert_exit_code 0
assert_in_stdout Time


