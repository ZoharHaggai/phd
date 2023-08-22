library(edgeR)
library(ggplot2)
library(limma)

# Path to location of the counts matrix (txt)
COUNTS_FILE = "data/bulk_rna/animals/chicken_grcg6a/edge_r/filtered/count_lps_4h.txt"

# Path to sample info file (csv)
SAMPLE_INFO_FILE = "data/bulk_rna/animals/chicken_grcg6a/edge_r/filtered/info_lps_4h.csv"

# Parameters to function:
# samples_info = table of samples info
# count_values =  matrix of count values
# pair = pair of 2 groups to comapre. i.e pair =c("ctrl", "sick")
#     values in pair must be in the sample info file.
#      FC values in the results - potive FC means up in the second group of the pair.
# out_filename -  path to out file. if FALSE return the result as a table
calculate_fc = function(samples_info, count_values, pair, out_filename = FALSE) {
  
  # create DGE objects
  de_obj = DGEList(counts=count_values, group=samples_info$type) # group needs to be the column in samples_info to compare according to
  de_obj = calcNormFactors(de_obj, method = "TMM")
  de_obj = estimateDisp(de_obj)
  
  # run exact test
  et = exactTest(de_obj, pair = pair)
  
  # add QValue
  et$table$QValue = p.adjust(et$table$PValue, "BH")
  
  # order by FDR
  et$table = et$table[order(et$table$QValue),]
  
  # write output
  if (out_filename == FALSE) {
    return(et$table)
  }
  write.table(et$table, file = out_filename, sep = ",")
}


#COUNTS_FILE =  "C:/Users/TzachiHNB6/Documents/yarden_ichilov/counts/GSE121212_readcount.txt"
#SAMPLE_INFO_FILE = "C:/Users/TzachiHNB6/Documents/yarden_ichilov/sample_info/sample_info.csv"
#read sample data
samples_data = read.csv(SAMPLE_INFO_FILE, header = TRUE)
#read count matrix
count_data = read.table(COUNTS_FILE, header = TRUE)

p = c("CTRL", "lps_4") # In this case positive FC will mean - up in AD

# set results file path
out = sprintf("data/bulk_rna/animals/komodo/edge_r/filtered/output_lf/lf_4_filtered.csv")

#run EdgeR function
table = calculate_fc(samples_data, count_data, p)

#write results (csv)
write.csv(table, out, quote=FALSE)
print("I'm finished")
