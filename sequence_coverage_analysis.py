'''
Rebecca Fuchs
Analysis of sequence coverage
Bioinformatics tools you will need: Samtools, BWA, Bedtools

Usage: 
This script will align fastq files to a reference, get fractional coverage of 
each sample to the reference. 

This one script has the sample names hard coded in. I chose to do this 
instead of having them be typed into the command line because I thought there were 
many samples. If I was making a more general alignment script I might have the sample 
names be input in the commandline. 


Samples are in the same sample_data folder
Output files are labeled with the sample it came from, including sam, bam, and other output files
Plots are also saved to the folder.

'''
import sys
import subprocess
import pandas as pd
import decimal
#____________________________________________________________

'''
First an index is made for mecA.fa to be used as refrence
bwa_mem_alignment funtion will run alignment and output sam file
samtool funtion will use samtools to output bamfiles
Both funtions ran in a loop with list of sample names for inputs
'''

#list of sample names below
list_of_samplefiles=['sample0.1','sample0.2','sample1.1','sample1.2','sample2.1','sample2.2','sample3.1', 'sample3.2' ]

#make the index with bwa
subprocess.run(['bwa','index','-p','mecAindex2','-a', 'bwtsw', 'mecA.fa'])
#mecAindex2 is the name of the index

#funtion to run bwa alignment for each sample and samtools to make bam 
def bwa_mem_alignment(samplename, sam_outputname):
  samfile=open(sam_outputname,'w')
  subprocess.run(('bwa mem -t 8 -M mecAindex2 sample_data/'+samplename), stdout=samfile, shell=True)
  samfile.close()

#samtools for sam to bam
def samtool(sam_outputname,bam_outputname) : 
  bamfile=open(bam_outputname,'w')
  p1=subprocess.run(('samtools view -bT mecA.fa '+sam_outputname), stdout=bamfile, shell=True)
  bamfile.close()


#running both funtions on sample names
for filename in list_of_samplefiles:
  bwa_mem_alignment(filename+'.fastq',filename+'.sam')
  samtool(filename+'.sam', filename+'.bam')
#outputs are in the folder


#_________________________________________________________________


'''
Use bedtools to run genecov funtion, genecov will output a table of position
and depth over the refrence 
Feature_coverage is the funtion created to run genecov and will get the fractional 
coverage from the genecov output, it intakes the samples bam file, the name you 
want for output, and depth input threshold
Depth_input is the user-specified threshold for depth, input into the function
The last bit for this question runs a loop to run feature_coverage for each
sample and puts them into a list. Then the list of fractions and sample names are
written into a csv file using a loop
'''


def feature_coverage(bam_input,name_genecov_output,depth_input):
    min_depth=str(depth_input)
    
    #running genomecov in the commandline
    genecov_output=open(name_genecov_output, 'w')
    cmd = "bedtools genomecov -ibam "+bam_input+" -bg | awk '$4 >'"+min_depth
    print(cmd)
    p2 = subprocess.run(cmd, stdout=genecov_output, shell=True)
    genecov_output.close()
    
    #below is just to get the lenght of the refrence
    mecA='mecA.fa'
    meca=open(mecA,'r')
    ref_seq=meca.read()
    len_ref=len(ref_seq) 
   #print(len(seq))
    
    df=pd.read_csv(name_genecov_output, sep='\t', header=None)
    #use pandas
    #df[column][row]

    rowtot=0
    total=0

    #subract end position from begining position to get length covered
    for i in range(0,len(df)):
        rowtot=(df[2][i]-df[1][i])
        total=rowtot+total
        #print(rowtot, total)
    #print(total)

    fractional_coverage=total/len_ref
    #print(fractional_coverage)
    return(fractional_coverage)

#run feature_coverage funtion for all samples
#list_of_samplefiles=['sample0.1','sample0.2','sample1.1']
frac_covs_list=[]
for bamfile in list_of_samplefiles:
  frac_cov=(round(feature_coverage(bamfile+'.bam',bamfile+'genecov',3),5))
  frac_covs_list.append(frac_cov)
print (frac_covs_list)


#writing a csv file for meta data of each sample
import csv
with open('all_frac_coverage_outputs.csv', 'w', newline='')as csvfile:
  spamwriter=csv.writer(csvfile, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
  spamwriter.writerow(['samplename','fractional_coverage'])
  for i in range(0,len(list_of_samplefiles)):
    spamwriter.writerow([list_of_samplefiles[i],frac_covs_list[i] ])




#_________________________________________________________________


'''
All of the fractional coverage data is in a csv ('all_frac_coverage_outputs.csv')
from above,
I'll read it in with pandas and make a bar graph with plot.bar

'''

import matplotlib.pyplot as plt
#all_frac_coverage_outputs.csv has the meta data
fracs_df = pd.read_csv('all_frac_coverage_outputs.csv',sep=',', header=0)
#print(fracs_df)

d=fracs_df.plot.bar(x='samplename',y=('fractional_coverage'), rot=0)

#should save a picture of the figure
d.figure.savefig('fractional_coverage_plot.png')



#_________________________________________________________________


'''
use wget to download refrence genome from S. aureus (bacteria, archae, plant plastid)
make into an index
align with bwa funtion from above
samtools with funtion above
bedtools has a funtion to compute coverage/depth along sample and has way to plot
geneomecov -d will give you all position coverage
pandas to make a big dataset with all depths from samples
pandas to make a line plot
'''
#s_aureus_ref

#_________________________________________________________________

'''
steps
use wget to get refrence genome from S. aureus (bacteria, archae, plant plastid)
make into an index
align with bwa funtion from above
samtools with funtion above
bedtools has a funtion to compute coverage/depth along sample and has way to plot
'''
#s_aureus_ref

cmd3='wget ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/013/425/GCF_000013425.1_ASM1342v1/GCF_000013425.1_ASM1342v1_genomic.fna.gz`'
get_index=subprocess.run(cmd3, shell=True)

#gunzip
cmdgunzip='gunzip GCF_000013425.1_ASM1342v1_genomic.fna.gz'
gunzip=subprocess.run(cmdgunzip, shell=True)

#creating an index
subprocess.run(['bwa','index','-p','s_aureus_index','-a', 'bwtsw', 'GCF_000013425.1_ASM1342v1_genomic.fna'])
#s_aureus_index is the name of the index

#a funtion to run bwa alignment for each sample and samtools to make bam 
def bwa_mem_alignment(samplename, sam_outputname):
  samfile=open(sam_outputname,'w')
  subprocess.run(('bwa mem -t 8 -M s_aureus_index sample_data/'+samplename), stdout=samfile, shell=True)
  samfile.close()

#samtools for sam to bam
def samtool(sam_outputname,bam_outputname) : 
  bamfile=open(bam_outputname,'w')
  p1=subprocess.run(('samtools view -bT mecA.fa '+sam_outputname), stdout=bamfile, shell=True)
  bamfile.close()


def genomecov_positions(sample_file, output_positions_cov):

  genecov_out=open(output_positions_cov,'w')
  position_cov_cmd='bedtools genomecov -ibam '+sample_file+ '  -d'
  subprocess.run(position_cov_cmd, stdout=genecov_out, shell=True)
  genecov_out.close()
  

list_of_samplefiles=['sample0.1','sample0.2','sample1.1','sample1.2','sample2.1','sample2.2','sample3.1', 'sample3.2' ]
for filename in list_of_samplefiles:
  bwa_mem_alignment(filename+'.fastq',filename+'s_aureus.sam')
  samtool(filename+'s_aureus.sam', filename+'s_aureus.bam')
  genomecov_positions(filename+'s_aureus.bam', filename+'all_positions_gencov')
  

dataframe_gencov=pd.read_csv('sample0.1all_positions_gencov', sep='\t', header=None)
dataframe_gencov.columns=['ref','position','depth_samp0.1']

slist_of_samplefiles=['sample0.2','sample1.1','sample1.2','sample2.1','sample2.2','sample3.1', 'sample3.2' ]
for gencovfile in slist_of_samplefiles:
  dataframe_temp=pd.read_csv(gencovfile+'all_positions_gencov', sep='\t', header=None)
  dataframe_temp.columns=['ref','position','depth'+gencovfile]
  depth=(dataframe_temp['depth'+gencovfile])
  dataframe_gencov['depth'+gencovfile]=depth

del dataframe_gencov['ref']
print(dataframe_gencov)

import matplotlib.pyplot as plt
#lines=dataframe_gencov.plot.line()
lineplot=dataframe_gencov.set_index('position').plot.line()
lineplot.figure.savefig('2lineplot.png')








