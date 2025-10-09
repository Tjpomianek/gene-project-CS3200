"""
Author: Teddy Pomianek
File: gene_plot.py
Description: Visualizes total cancer-linked gene associations per chromosome
"""

import pandas as pd
import matplotlib.pyplot as plt

# Create dataframe from csv
df = pd.read_csv("cancer_genes.csv")

# Creates dataframe that displays gene counts for each chromosome
gene_count = df.groupby("chromosome")["gene_count"].sum().sort_index()

# Create plot
plt.figure(figsize=(12, 6))
bars = plt.bar(
    gene_count.index.astype(str), 
    gene_count.values, 
    color="seagreen", 
    alpha=0.8, 
    edgecolor="black"
)

# Add value labels for chromosomes with higher gene counts
for bar in bars:
    y = bar.get_height()
    if y > 400:  
        plt.text(bar.get_x() + bar.get_width()/2, 
                 y + 10, f"{int(y)}", 
                 ha="center", va="bottom", 
                 fontweight="bold")

plt.title("Cancer-linked Gene Count by Chromosome")
plt.xlabel("Chromosome")
plt.ylabel("Gene Count")

plt.tight_layout()
plt.savefig("gene_count.png")
plt.show()