# Zohar's PhD projects

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

## Gene Gain and Loss Pipeline

## Other pipelines
