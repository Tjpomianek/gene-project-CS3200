# Cancer Gene–Chromosome Association Analysis  
**Author:** Teddy Pomianek  
**Course:** CS3200 – Introduction to Databases, Northeastern University  

---

## Project Overview
This project analyzes the relationship between human chromosomes and cancer-associated genes using data from the Genetic Association Database (GAD).  
The goal was to determine which chromosomes contain the most genes linked to cancer, using SQL for data management and Python for visualization.

---

## Objective
Identify chromosomes with higher concentrations of genes related to cancer by querying, aggregating, and visualizing data from the GAD dataset.

---

## Data Source
- Genetic Association Database (GAD), NCBI  
- Becker KG et al., *Nucleic Acids Research* (2004)  
- https://geneticassociationdb.nih.gov/

---

## Tools and Technologies
- MySQL for data storage, cleaning, and aggregation  
- Python (pandas, matplotlib) for analysis and visualization  
- Git and GitHub for version control  

---

## SQL Process
1. Created and populated the `gad` database using data from `gad.csv`.  
2. Removed null or blank chromosome values.  
3. Aggregated all cancer-related genes by chromosome using the following query:

   ```sql
   SELECT gene AS gene_symbol, chromosome, gene_name, COUNT(*) AS gene_count
   FROM gad
   WHERE disease_class = 'CANCER'
     AND chromosome IS NOT NULL
     AND chromosome <> ''
   GROUP BY chromosome, gene, gene_name
   ORDER BY chromosome, gene_count DESC;
