import requests
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import re

PUBMED_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def search_pubmed(query: str, max_results: int = 50) -> List[str]:
    
   # Sends a query to the PubMed database and returns a list of article IDs.
    
    search_url = f"{PUBMED_BASE}esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json"
    }
    res = requests.get(search_url, params=params)
    res.raise_for_status()
    return res.json().get("esearchresult", {}).get("idlist", [])


def extract_article_data(pmids: List[str]) -> List[Dict[str, str]]:

    #Given a list of PubMed IDs, fetch and parse article metadata including non-academic authors, company links, and contact emails.

    
    fetch_url = f"{PUBMED_BASE}efetch.fcgi"
    response = requests.get(fetch_url, params={
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml"
    })
    response.raise_for_status()

    xml = BeautifulSoup(response.content, "lxml-xml")
    final_data: List[Dict[str, str]] = []

    academic_terms = ["university", "institute", "college", "school", "hospital", "academy", "department"]
    business_terms = ["pharma", "biotech", "inc", "corp", "ltd", "gmbh", "co."]

    for entry in xml.find_all("PubmedArticle"):
        pmid = entry.PMID.text if entry.PMID else "N/A"

        title_tag = entry.find("ArticleTitle")
        article_title = title_tag.text if title_tag else "N/A"

        # Try to get the publication date (year and month)
        date_block = entry.find("PubDate")
        pub_date = "N/A"
        if date_block:
            y = date_block.find("Year")
            m = date_block.find("Month")
            pub_date = f"{y.text if y else ''}-{m.text if m else ''}"

        non_academic: List[str] = []
        companies: List[str] = []
        contact_email: str = "N/A"

        authors = entry.find_all("Author")

        for auth in authors:
            first = auth.find("ForeName")
            last = auth.find("LastName")
            full_name = f"{first.text if first else ''} {last.text if last else ''}".strip()

            affil_info = auth.find("AffiliationInfo")
            if not affil_info or not affil_info.text:
                continue

            affil = affil_info.text.strip()
            affil_lower = affil.lower()

            # Determine if author is academic or company-affiliated
            is_academic = any(term in affil_lower for term in academic_terms)
            is_industry = any(term in affil_lower for term in business_terms)

            if not is_academic:
                non_academic.append(full_name)

                if is_industry:
                    companies.append(affil)

                if "@" in affil_lower and contact_email == "N/A":
                    email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", affil)
                    if email_match:
                        contact_email = email_match.group()

        if non_academic:
            final_data.append({
                "PubmedID": pmid,
                "Title": article_title,
                "Publication Date": pub_date,
                "Non-academic Author(s)": "; ".join(non_academic),
                "Company Affiliation(s)": "; ".join(companies),
                "Corresponding Author Email": contact_email
            })

    return final_data
