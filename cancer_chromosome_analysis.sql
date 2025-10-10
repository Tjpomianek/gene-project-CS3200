-- Project: Cancer Gene–Chromosome Association Analysis
-- Author: Teddy Pomianek | Northeastern University
--
-- This project looks at the connection between human chromosomes
-- and cancer-related genes using data from the Genetic Association Database (GAD).
-- The goal is to find which chromosomes have higher concentrations
-- of genes linked to cancer.
--
-- Data Source:
-- Genetic Association Database (GAD), NCBI (Becker KG et al., Nucleic Acids Research, 2004)
-- https://geneticassociationdb.nih.gov/


-- Create and select the database
CREATE DATABASE IF NOT EXISTS gad;
USE gad;

-- Create the GAD table
DROP TABLE IF EXISTS gad;

CREATE TABLE gad (
  gad_id            INT,
  association       TEXT,
  phenotype         TEXT,
  disease_class     TEXT,
  chromosome        TEXT,
  chromosome_band   TEXT,
  dna_start         INT,
  dna_end           INT,
  gene              TEXT,
  gene_name         TEXT,
  reference         TEXT,
  pubmed_id         INT,
  year              INT,
  population        TEXT
);

-- Load the gad data
LOAD DATA LOCAL INFILE 'gad.csv'
INTO TABLE gad
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
IGNORE 1 ROWS;

-- Aggregate cancer-linked genes by chromosome

-- This query counts the number of cancer-associated genes
-- per chromosome to identify potential genomic “hotspots.”
SELECT gene AS gene_symbol, chromosome, gene_name, COUNT(*) AS gene_count
FROM gad
WHERE disease_class = 'CANCER'
  AND chromosome IS NOT NULL
  AND chromosome <> ''
GROUP BY chromosome, gene, gene_name
ORDER BY chromosome, gene_count DESC;
