import os 
import sys 
import shutil
import json 

def process_json_data(infile_json, infile_dir, outfile_dir):
    """
    Takes a file in json format and a directory that contains
    the matching FNA files. Reads the data in the json and
    initializes a dictionary that will hold the GFA accession:data
    value pairs. Constructs the dictionary and calls match_name()
    to find the matching FNA file to the dictionary.
    """

    genome_dict = {}

    # Opens JSON file and iterates trough each line of the JSON. Try/except is to
    # handle instances where someone used isoalte instead of strain. 
    with open(infile_json, "r") as json_file:
        for line in json_file:
            data = json.loads(line)
            accession_num = data["currentAccession"]
            organism_name = data["organism"]["organismName"]
            if "infraspecificNames" in data["organism"]: 
                try:
                    organism_strain = data["organism"]["infraspecificNames"]["strain"] 
                except:
                    organism_strain = data["organism"]["infraspecificNames"]["isolate"]
            else:
                organism_strain = " "
            
            assembly_level = data["assemblyInfo"]["assemblyLevel"]
            
            if organism_strain in organism_name:
                final_name = organism_name + "_" + assembly_level
            else:
                final_name = organism_name + "_" + organism_strain + "_" + assembly_level
            
            # Filters out genomes that have already been added to the dictionary to filter out duplicates.
            # Necessary for genomes that have GCA and GCF number 
            GCA_accession_num = "GCA" + accession_num[3:]
            GCF_accession_num = "GCF" + accession_num[3:]
            if GCA_accession_num not in genome_dict and GCF_accession_num not in genome_dict:
                genome_dict[accession_num] = final_name

    match_and_rename(genome_dict, infile_dir, outfile_dir)

def match_and_rename(genome_dict, infile_dir, outfile_dir):
    """
    Iterates through the infile directory and matches the fna
    file name to the appropriate GFA accession number in the 
    genome dictionary. Calls rename_files() to produce a more
    readable name.
    """

    outfile_dir = new_dir(outfile_dir)

    for filename in os.listdir(infile_dir):
        if filename.endswith(".fna"):
            file_key = filename[:15] # Extract the key from the filename
            if file_key in genome_dict:
                new_name = genome_dict[file_key] + ".fasta"
                new_name = replace_special_chars(new_name)
                new_path = os.path.join(outfile_dir, new_name)
                old_path = os.path.join(infile_dir, filename)
                shutil.move(old_path, new_path)

def replace_special_chars(string):
    """
    Iterates through the passed string and removes any special
    characters that are going to screw with the path. What monster 
    puts a / in the strain name????
    """

    replacements = {
        "/"  :  "_",
        "\\" :  "_",
        "'"  :  " ",
        '"'  :  ' ',
        "["  :  " ",
        "]"  :  " ",
        "{"  :  " ",
        "}"  :  " ",
        ":"  :  " ",
        ";"  :  " ",
        "."  :  " ",
    }

    for old_char, new_char in replacements.items():
        if old_char in string:
            string = string.replace(old_char, new_char)
    string = string.replace(" ", "_")
    return string
    

def new_dir(directory):
    """
    Creates a new directory with passed name if it does not
    already exist.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory 

infile_json = sys.argv[1]
infile_dir = sys.argv[2]
outfile_dir = sys.argv[3]
process_json_data(infile_json, infile_dir, outfile_dir)

   