# Zohar's PhD Projects

## Bulk RNA Sequencing Pipeline

After sending the samples to sequencing and getting the results:

1. Genome indexing and annotation.
2. Salmon Algorithm -
   A tool to quantify transcripts expression in RNA-seq data.  
   We ran jobs in the cluster to quantify transcript from the sequencing results files.
3. We generated a matrix of counts per gene (quants files) for all samples (all animals).
4. We ran R script (edgeR) to generate filtered data (DE) for all samples.
5. After filteration, we generated the files of DE genes for all samples.
   Genes that went up in the treatment group compared to the control group and that their p-values were less than 0.05 were selected to a new csv file.
6. After we got the significant upregulated genes, we ran a Python script to compare them with the orthologs genes from Ensembl.

## Single Cell RNA Sequencing Pipeline

Roey sent me his pipeline for the single cell RNA sequencing analysis he did in the lab (named QC_pipeline_c_and_lf.ipynb).
We went toghether over the things he looks at after the first raw data he gets.

## Gene Gain and Loss Pipeline

The first goal -
We took a `.csv` file and outputed two CSVs which counted the changes in each gene. One for `'+'` changes and one for `'-'` changes.

What I did -

1. Created a list of reptiles we are currently interested in.

2. Initialization of the main DFs. Reads the main DF containing the gene change type and count gene change type is one of `{'+', '-', '0'}`.

3. `df_change` will contain all 'change' values, one of `{'+', '-', '0'}`.

4. `df_count` will contain all 'count' values.

5. Plus & Minus DataFrames -

   Used the previous created DFs in order to create 2 new DFs, each will contain the count from either `{'+', '-'}`.

   The explanation of the proccess for `'+'` (the same can be applied for `'-'`):

   1. Replaced `'+'` with `None`

   2. Used `first_df.combine_first(other_df)` , which does the following:
      - Replaces `None` values from `first_df` with the corresponding value from the `other_df`

            if first_df[i, j] is None:

               first_df[i, j] = other_df[i, j]

   3. Replaces `'0'` and `'-'` values with `np.NaN`.

   4. Drops each row which doesn't have any values in it.

   5. Merges the two `df_gene_names` and the newly created DF.

   6. `df_gene_names` has just two columns, `'Gene Id'` and `'Gene Name'`.

   7. This is basically appending to the leftmost side of the new DF one new column (`'Gene Name'`).

  
6. Export the two new DFs to CSVs.

7. df_plus.to_csv(f'../output/{ref}/df_plus.csv')

8. df_minus.to_csv(f'../output/{ref}/df_minus.csv')
## Other Projects
