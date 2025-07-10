📄 Paper Fetcher

This project helps you fetch and organize publicly available research papers (e.g., from PubMed) based on a search query. It extracts key information like authors, titles, publication dates, and more — and can export results to a CSV file for easy use.

📁 Project Structure

PAPER FETCHER

.mypy_cache/

  ->3.11
   
  ->gitignore

paper_fetcher/

  ->__init__.py

  ->main.py 

  ->fetcher.py 

  ->_pycache_

Tests

   ->test.py

pyproject.toml

README.md

results.csv

How to Install and Run

Step 1: Clone the Repository

  ->git clone https://github.com/krishnagund/Paper-Fetcher

  ->cd paper-fetcher


Step 2: Install Dependencies Using Poetry

  ->poetry install

Step 3: Run the Program

   poetry run get-papers-list "machine learning" --file papers.csv

#Replace the machine learning with the topic that u want 



Tools & Libraries Used

Typer	-  For building the CLI tool	                  Link - https://typer.tiangolo.com

Requests -	For making HTTP requests	                  Link - https://docs.python-requests.org

BeautifulSoup4	- For HTML parsing	                      Link - https://www.crummy.com/software/BeautifulSoup

lxml	- Fast XML/HTML parser	                          Link - https://lxml.de

Biopython -	For working with biological data              Link - https://biopython.org

Pandas - 	For organizing and exporting data	          Link - https://pandas.pydata.org

pyhton 3.11 is used

Output - 

this is the sample output of the on eof the paper which is in the csv form .


| Pubmed ID | Title                                                                                          | Publication Date | Non-academic Author(s)                                              | Company Affiliation(s) | Corresponding Author Email             |
|-----------|------------------------------------------------------------------------------------------------|------------------|----------------------------------------------------------------------|------------------------|----------------------------------------|
| 40634697  | Improved prediction of MAPKi response duration in melanoma patients using genomic data and machine learning. | 2025-Jul         | Sarah Dandou; Véronique D'Hondt; Jérôme Solassol; Peter J Coopman; Ovidiu Radulescu; Romain M Larive |                        | ovidiu.radulescu@umontpellier.fr      |





Package Availability
This package has been published to TestPyPI for testing purposes.

View on TestPyPI: https://test.pypi.org/project/krish-paper-fetcher/0.1.0/

