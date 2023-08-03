"""
# Input
gene_list
filter name

# Output
items = []
item = ["HNGC". "ENTREZ", "RELATED GENE LIST"]
"""

# import necessary libraries and stuff
import pandas as pd
import supabase
from supabase import create_client, Client
from collections import Counter
from dotenv import load_dotenv
import os

load_dotenv()

# set up supabase connection
url: str = os.getenv("SUPABASE_URL")
key: str  = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

"""# # Check if valid file type; if valid -> return file and call gene_output, else -> return None
# def file_intake(file_name, file_type, symbol_type):
#     if file_type == 'csv':
#         if file_name.endswith(".csv"):
#             file = pd.read_csv(file_name, sep=",")
#             return gene_output(file, file.iloc[:,0], symbol_type, file_name)
#         elif file_name.endswith(".tsv"):
#             file_type = 'tsv'
#             file = pd.read_csv(file_name, sep="\t")
#             return gene_output(file, file.iloc[:,0], symbol_type, file_name)
#         else:
#             return wrong_type()
#     elif file_type == 'tsv':
#         if file_name.endswith(".tsv"):
#             file = pd.read_csv(file_name, sep="\t")
#             return gene_output(file, file.iloc[:,0], symbol_type, file_name)
#         elif file_name.endswith(".csv"):
#             file = pd.read_csv(file_name, sep=",")
#             return gene_output(file, file.iloc[:,0], symbol_type, file_name)
#         else:
#             return wrong_type()
#     else:
#         return wrong_type()

# # handle unsuccessful file upload
# def wrong_type():
#     print("Unsuccessful submission.")
#     return None"""

# Make a function to filter genes and return a filtered list
def filter_path(filt):
    if filt == 'Metabolic':
        # Query the "Filters" table to get the gene list for the selected filter
        response = supabase.table('Filters').select('Gene List').eq('List Name', filt).execute()
        # if response.get_error():
        #     print(f"Error fetching data: {response.get_error()['message']}")
        #     return None
        
        # Extract the gene list from the response data
        gene_list_data = response.data
        if len(gene_list_data) > 0:
            gene_list = gene_list_data[0]['Gene List']
            # Assuming the gene_list is a string representation of a list, convert it to an actual list
            gene_list = eval(gene_list)
            return gene_list
        else:
            print("No data found for the selected filter.")
            return None
    else:
        print("Invalid filter type.")
        return None


# Make relevant columns of supabase into readable lists
tf_list_HGNC = supabase.table('tfs').select("HGNC symbol", "Related Genes HGNC").neq("Related Genes HGNC", "").execute()
tf_list_HGNC_data = tf_list_HGNC.data
# tf_list_HGNC_data = tf_list_HGNC_data[:50]
# tf_list_ENTREZ = supabase.table('tfs').select("EntrezGene ID").execute()
# tf_list_ENTREZ_data = tf_list_ENTREZ.data
# tf_list_ENTREZ_data = tf_list_ENTREZ_data[:5]

#initialize variables necessary for tracking data
tf_list_HGNC_output = []
tf_list_ENTREZ_output = []
related_genes_hgnc_list = []
related_genes_entrez_list = []

# Get relevant data from supabase, store it in pre-initialized variables
def gene_output(gene_list, filt):
    output = []

    # tf_count = 0
    # if symbol_type == "HGNC symbol":

    #remove all genes that don't appear in filter list
    if filt != "":
        filter_list = filter_path(filt)
        for i in gene_list:
            if gene_list[i] not in filter_list:
                gene_list.pop(i)
    
    #retrieve and organize all relevant data into table
    for gene in tf_list_HGNC_data:
        item = {"TF": gene['HGNC symbol'], "hits": 0, "gene_list":[]}
        for gene2 in gene_list:
            coexpression_list = gene['Related Genes HGNC'].split(",")
            if (gene2 in coexpression_list):
                item['hits'] += 1 
                item['gene_list'].append(gene2)
                # tf_list_HGNC_output.append(gene.get("HGNC symbol"))
                # tf_list_ENTREZ_output.append(gene.get("EntrezGene ID"))
                # related_genes_hgnc_list.append(gene.get("Related Genes HGNC"))
                # related_genes_entrez_list.append(gene.get("Related Genes Entrez"))
        output.append(item)
    
    #organize table into dataframe and sort based on # of TF hits
    output = pd.DataFrame(output)
    output.drop(output[output['hits'] < 1].index, inplace=True)
    output.sort_values(by=['hits'], ascending=False, inplace=True)
    jsonthingy = output.to_json()
    #print(output)
    return(jsonthingy)   
            # tf_count += 1
            # print("HGNC: ", tf_list_HGNC_output, " Related Genes: ", related_genes_hgnc_list)
         

    """# else:
        # for gene in tf_list_ENTREZ_data:
        #     for gene2 in gene_list:
        #         coexpression_list = gene["Related Genes Entrez"].split(",")    
        #         if gene_list[gene[symbol_type]] in gene.get("Related Genes Entrez"):
        #             tf_list_HGNC_output.append(gene.get("HGNC symbol"))
        #             tf_list_ENTREZ_output.append(gene.get("EntrezGene ID"))
        #             related_genes_hgnc_list.append(gene.get("Related Genes HGNC"))
        #             related_genes_entrez_list.append(gene.get("Related Genes Entrez"))
        #             tf_count += 1

    # tf_hit_counts = Counter(tf_list_HGNC_output)
    # print(tf_hit_counts)
    # sorted_tfs = sorted(tf_hit_counts.items(), key=lambda item: item[1], reverse=True)
    # print(sorted_tfs)
    # sorted_tfs, tf_counts = zip(*sorted_tfs)

    # return file_output(sorted_tfs, tf_list_ENTREZ_output, related_genes_hgnc_list, related_genes_entrez_list, tf_counts, file_name)

# Make df and csv file out of data in order to return to the user
# def file_output(sorted_tfs, tf_list_ENTREZ_output, related_gene_hgnc_list, related_genes_entrez_list, tf_counts, file_name):
#     final_output = pd.DataFrame({"HGNC": sorted_tfs,
#         #  "Entrez": tf_list_ENTREZ_output,
#         #  "Related Genes HGNC": related_gene_hgnc_list,
#         #  "Related Genes Entrez": related_genes_entrez_list,
#          "TF Hits": tf_counts})
    

#     final_output.sort_values(by="TF Hits", ascending=False, inplace=True)
#     print(final_output)

#     print("HGNC: %d, Related Genes: %d, TF Hits: %d", len(sorted_tfs), len(related_gene_hgnc_list), len(tf_counts))

    # return final_output
"""