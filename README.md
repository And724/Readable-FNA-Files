# Readable-New-Genbank-Files
The included Python script can be used to make the names of FASTA files from NCBI easily readable and to include the species name. Best if used within a UNIX/UNIX-like environment as there are a couple steps that involve using bash. You may need to install some packages prior to running the script. Can be used on Windows but some manipulation of the input files must be done prior to passing it to the script. Note: this script was made for and tested with bacterial genome data. May require modification to work properly on other kingdoms. If interested let me know. 

# Downloading Genbank Files
First navigate to the following website: https://www.ncbi.nlm.nih.gov/datasets/genome/ 
From this website, make your query and proceed to download your desired files as a package. Feel free to download All files (GenBank and RefSeq) as the script can handle any duplicate genomes (those that have a GFA and GCA #). 

# Usage 
Move the downloaded package to TACC (Texas Advanced Computing Center) or a local server. This was done via rclone, linking google drive to TACC. 
Once file has been moved, unzip the file using: 

`cd {uploaded_dir}`

Enter the directory: <br />  
`cd {uploaded_dir}`  <br /> 
                                            
Move the metadata files from the sub-directory into it's parent:  

`cd {sub-directory}`  
`mv {metadata_files} ..`

Now the sub-directory will only contain sub-directories with a corresponding fasta file in each one. The files in each of these sub-directories need to be pulled out and moved into a single directory using the following command: 

`find {directory containing your GCA/GCF subdirectories} -type f -exec cp {} {path to your desired directory; ideally an empty one} \;`

After executing the previous command, all of the FASTA files will be in a single directory and ready for processing. 
The script takes three arguments in the following order: JSONL, Data Directory, Output Directory Name. 

JSONL: This is one of the metadata files that was moved in a previous command. It is usually named "assembly_data_report.jsonl" or something similar. 

Data Directory: This is the directory where you moved all of the individual FASTA files to. 

Output Directory Name: Simply write a name for a new (or existing) directory and the script will create the directory (if applicable) and your renamed files will be moved into it.

To invoke and run the script enter the following:  

`python {path_to_script/new_genbank.py} {path_to_JSONL} {path_to_previously_made_directory} {output_directory_name}`

# Usage: Windows
If you have your files locally on your Windows machine, the fasta files within the sub-directories will all need to be moved into a single directory first. 
The following command can be used via the command prompt:  

`forfiles /s /m * /c "cmd /c copy @file C:\path\to\destination"`

To run the script, enter the following: 

`python "{path_to_script\new_genbank.py}" "{path_to_JSONL}" "{path_to_previously_made_directory}" "{output_directory_name}"`
