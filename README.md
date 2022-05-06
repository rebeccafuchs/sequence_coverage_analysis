
## Summary
sequence_coverage_analysis.py is a script that will give each samples 
fractional coverage of a reference sequece. This fraction is calculated by depth,
with a user input minimum depth. The data is put into a single csv file, and a bar 
graph shows the fractional coverage graphically for eaach sample. In the last part 
of the script I download a refrence genome from ncbi, and re-align the samples. Instead
of graphing each samples fractional coverage, I created a line plot. The plot shows the 
coverage for each sample in all position of the reference.


## Usage
commandline input: python sequence_coverage_analysis.py 
Sample data should be in folder names sample_data, samples should be fastq files
Bioinformatics tools you will need, samtools, bedtools, bwa
For my own analysis of 8 samples, look at Analysis.md (graphs are here)

I chose to use BWA for alignment. This software is good for mapping low divergent sequeces against large reference genomes. I used BWA-MEM, the algorithm recommended on the website because it is faster and more accurate then other algorithms. The website this algorithm has the best performance with illumina reads.
http://bio-bwa.sourceforge.net/
Alignment files were output as sam files, then samtools is used to convert them into bam files

I define fractional coverage as
the fraction of reference sequence (here, the mecA gene) covered by reads to depth greater than or 
equal to some user-specified threshold (e.g., 5). user imput in script

The inputs for this question are the bam files, and a user-defined depth 
threshold. Bedtools funtion genomecov is used to get fractional coverage.
The outputs of each file are put into a csv file.

To create a bar graph the csv file is read with pandas. The data is plot as a bar plot 
and saved with matplotlib.

Finally, the last part of the script, downloades the *S. aureus* reference genome `GCF_000013425` and re-align
the samples to this reference. I wanted to compute coverage/ depth for each position along 
this reference for each sample, using `bedtools` again. Then to visualize I used a 
line plot for position coverage for each sample. 
