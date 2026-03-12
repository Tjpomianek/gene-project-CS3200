"""
Author: Teddy Pomianek
File: cancer_sankey.py
Description: 
Creates a 3 level Sankey diagram that maps the top 5 
chromosomes by cancer-linked gene count
to their top 20 most studied cancer-linked genes,
then mapped to the specific phenotypes of Cancer those genes are associated with in GAD.
"""

import pandas as pd
from sankey import show_sankey

# load in 'gad.csv' into df
gad_df = pd.read_csv("gad.csv")
cancer_genes_df = pd.read_csv("cancer_genes.csv")

# filter for rows connected to 'CANCER' disease class
cancer_df = gad_df[gad_df['disease_class'] == 'CANCER']

# get top 5 chromosomes by Cancer-linked genes
top_chromosomes = cancer_genes_df.groupby('chromosome')['gene_count'].sum().sort_values(ascending=False).reset_index()
top_5_chromosomes = top_chromosomes.head(5)


# get top 20 Cancer-linked genes 
top_20_genes = cancer_genes_df[cancer_genes_df['chromosome'].isin(top_5_chromosomes['chromosome'])].nlargest(20, 'gene_count')['gene_symbol']

# get a df that is filtered by top 5 chromosomes and top_20_genes
sankey_df = cancer_df[cancer_df['gene'].isin(top_20_genes)]
sankey_df = sankey_df[sankey_df['chromosome'].isin(top_5_chromosomes['chromosome'])]

# get top 10 most common cancer phenotypes
top_phenotypes = sankey_df.groupby('phenotype').size().sort_values(ascending=False).head(10).index
sankey_df = sankey_df[sankey_df['phenotype'].isin(top_phenotypes)]

# create sankey diagram
show_sankey(sankey_df, 'chromosome', 'gene', 'phenotype', width=1600)


