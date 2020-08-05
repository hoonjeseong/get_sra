# Get SRA data from BioProject 
#### __Get Sequence Read Archive (SRA) data from Bioproject__

- If you have any problems with downloading SRA data form NCBI BioProject (PRJNA) summary
- It helps to get SRA data from SRS (sample) ID using BeautifulSoup
- sra_result.csv (example: https://www.ncbi.nlm.nih.gov/bioproject/PRJNA552603/)
----
#### __Usage__
`python download.SRA.py -i [sra_result.csv] -l WGS -o [output folder] -f [prefetch path from sra tool]`

----
#### __Require__
- python3
- beautifulsoup4 
- sra tool kit (http://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/current/)
