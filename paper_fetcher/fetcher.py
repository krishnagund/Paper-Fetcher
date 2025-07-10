import requests
from typing import List, Dict
from bs4 import BeautifulSoup
import re

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

    soup = BeautifulSoup(response.content, "lxml-xml")  # safer for XML
    results = []

    ACADEMIC_KEYWORDS = ["university", "institute", "college", "school", "hospital", "academy","department"]
    COMPANY_KEYWORDS = ["pharma", "biotech", "inc", "corp", "ltd", "gmbh", "co."]

    for article in soup.find_all("PubmedArticle"):
        pmid = article.PMID.text if article.PMID else "N/A"
        title = article.Article.ArticleTitle.text if article.Article and article.Article.ArticleTitle else "N/A"

        # Date parsing
        pub_date_tag = article.find("PubDate")
        pub_date = "N/A"
        if pub_date_tag:
            year = pub_date_tag.find("Year")
            month = pub_date_tag.find("Month")
            pub_date = f"{year.text if year else ''}-{month.text if month else ''}"

        non_academic_authors = []
        company_affiliations = []
        corresponding_email = "N/A"

        authors = article.find_all("Author")

        for author in authors:
            last = author.find("LastName").text if author.find("LastName") else ""
            fore = author.find("ForeName").text if author.find("ForeName") else ""
            fullname = f"{fore} {last}".strip()

            affil_tag = author.find("AffiliationInfo")
            if not affil_tag:
                continue

            affil_text = affil_tag.text.lower()
            affil_orig = affil_tag.text.strip()

            # Heuristic: if none of the academic keywords appear, it's non-academic
            is_academic = any(keyword in affil_text for keyword in ACADEMIC_KEYWORDS)
            is_company = any(keyword in affil_text for keyword in COMPANY_KEYWORDS)

            if not is_academic:
                non_academic_authors.append(fullname)

                if is_company:
                    company_affiliations.append(affil_orig)

                # Email detection
                if "@" in affil_text and corresponding_email == "N/A":
                    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", affil_orig)
                    if match:
                        corresponding_email = match.group()

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
