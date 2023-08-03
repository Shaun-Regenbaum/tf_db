"""
# Input
gene_list
filter name

# Output
json file of list of {TF: , #Hits: , Coexpression List: }
"""

#import necessary libraries and stuff
import pandas as pd
import supabase
from supabase import create_client, Client
from collections import Counter
from dotenv import load_dotenv
import os

load_dotenv()

#set up supabase connection
url: str = os.getenv("SUPABASE_URL")
key: str  = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

#make a function to filter genes and return a filtered list
def filter_path(filt):
    if filt == 'Metabolic':
        #query the "Filters" table to get the gene list for the selected filter
        response = supabase.table('Filters').select('Gene List').eq('List Name', filt).execute()
        
        #extract the gene list from the response data
        gene_list_data = response.data
        if len(gene_list_data) > 0:
            gene_list = gene_list_data[0]['Gene List']

            #convert the string representation of a list to an actual list
            gene_list = eval(gene_list)
            return gene_list
        else:
            print("No data found for the selected filter.")
            return None
    else:
        print("Invalid filter type.")
        return None


#make relevant columns of supabase into readable lists
tf_list_HGNC = supabase.table('tfs').select("HGNC symbol", "Related Genes HGNC").neq("Related Genes HGNC", "").execute()
tf_list_HGNC_data = tf_list_HGNC.data

#initialize variables necessary for tracking data
tf_list_HGNC_output = []
tf_list_ENTREZ_output = []
related_genes_hgnc_list = []
related_genes_entrez_list = []

#get relevant data from supabase, store it in pre-initialized variables
def gene_output(gene_list, filt):
    output = []

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

        output.append(item)
    
    #organize table into dataframe and sort based on # of TF hits
    output = pd.DataFrame(output)
    output.drop(output[output['hits'] < 1].index, inplace=True)
    output.sort_values(by=['hits'], ascending=False, inplace=True)
    jsonthingy = output.to_json()

    return(jsonthingy)   
            