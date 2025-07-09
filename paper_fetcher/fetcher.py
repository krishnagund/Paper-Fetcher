# paper_fetcher/fetcher.py

import requests
from typing import List, Dict
from bs4 import BeautifulSoup

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def fetch_pubmed_ids(query: str, retmax: int = 50) -> List[str]:
    url = f"{BASE_URL}esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": retmax,
        "retmode": "json"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()["esearchresult"]["idlist"]

def fetch_details(pubmed_ids: List[str]) -> List[Dict]:
    url = f"{BASE_URL}efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "lxml")
    results = []

    for article in soup.find_all("pubmedarticle"):
        pmid = article.pmid.text
        title = article.articletitle.text if article.articletitle else ""
        pub_date_tag = article.find("pubdate")
        pub_date = "N/A"
        if pub_date_tag:
            year = pub_date_tag.find("year")
            month = pub_date_tag.find("month")
            pub_date = f"{year.text if year else ''}-{month.text if month else ''}"

        authors_info = article.find_all("author")
        non_academic_authors = []
        company_affiliations = []
        corresponding_email = "N/A"

        for author in authors_info:
            affiliation = author.find("affiliation")
            if affiliation and affiliation.text:
                affil_text = affiliation.text.lower()
                if any(company in affil_text for company in ["pharma", "biotech", "inc", "corp", "ltd", "gmbh"]):
                    last = author.find("lastname").text if author.find("lastname") else ""
                    fore = author.find("forename").text if author.find("forename") else ""
                    non_academic_authors.append(f"{fore} {last}".strip())
                    company_affiliations.append(affiliation.text)

                    # Email heuristic
                    if "@" in affil_text and corresponding_email == "N/A":
                        for word in affiliation.text.split():
                            if "@" in word:
                                corresponding_email = word.strip("().;,")  # clean punctuation

        if non_academic_authors:
            results.append({
                "PubmedID": pmid,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academic Author(s)": "; ".join(non_academic_authors),
                "Company Affiliation(s)": "; ".join(company_affiliations),
                "Corresponding Author Email": corresponding_email
            })

    return results
