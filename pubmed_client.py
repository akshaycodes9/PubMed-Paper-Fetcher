import time
import httpx
import logging
import xml.etree.ElementTree as ET
import csv
import argparse
from typing import Dict, List

# ✅ Configure logging for better debugging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ✅ PubMed API Client
class PubMedClient:
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    def safe_request(self, url: str, params: dict, retries: int = 3, delay: int = 2) -> httpx.Response:
        """
        Make a safe API request with retries.
        
        - retries: Number of retry attempts in case of failure.
        - delay: Time (in seconds) between retries.
        """
        for attempt in range(retries):
            try:
                response = httpx.get(url, params=params, timeout=10)
                response.raise_for_status()  # Raise an error for bad responses (e.g., 404, 500)
                return response
            except httpx.HTTPError as e:
                logging.warning(f"Request failed (attempt {attempt + 1}/{retries}): {e}")
                time.sleep(delay)

        raise RuntimeError("Failed to connect to PubMed API after multiple retries.")

    def search_papers(self, query: str, max_results: int = 10) -> List[str]:
        """
        Search for papers on PubMed and return a list of paper IDs.
        """
        if not query.strip():
            logging.error("Search query cannot be empty.")
            return []

        search_url = f"{self.BASE_URL}/esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json"
        }

        # ✅ Make the request
        response = self.safe_request(search_url, params)
        data = response.json()

        paper_ids = data.get("esearchresult", {}).get("idlist", [])

        if not paper_ids:
            logging.info("No papers found for the given query.")

        return paper_ids

    def fetch_paper_details(self, paper_id: str) -> Dict:
        """
        Fetch details of a specific paper using PubMed ID.
        """
        fetch_url = f"{self.BASE_URL}/efetch.fcgi"
        params = {"db": "pubmed", "id": paper_id, "retmode": "xml"}

        # ✅ Make a safe API request
        response = self.safe_request(fetch_url, params)

        try:
            root = ET.fromstring(response.content)
        except ET.ParseError as e:
            logging.error(f"Error parsing XML for paper {paper_id}: {e}")
            return {}

        # ✅ Extract paper details
        paper_details = {
            "id": paper_id,
            "title": root.findtext(".//ArticleTitle"),
            "date": root.findtext(".//PubDate/Year") or root.findtext(".//MedlineDate"),
            "authors": [],
            "affiliations": [],
            "corresponding_email": root.findtext(".//AffiliationInfo/Email"),
        }

        # ✅ Extract authors and affiliations
        for author in root.findall(".//Author"):
            collective_name = author.findtext("CollectiveName")
            last_name = author.findtext("LastName")
            fore_name = author.findtext("ForeName")

            if collective_name:
                paper_details["authors"].append(collective_name)
            elif last_name and fore_name:
                paper_details["authors"].append(f"{fore_name} {last_name}")

            affiliation = author.findtext(".//AffiliationInfo/Affiliation")
            if affiliation:
                paper_details["affiliations"].append(affiliation)

        return paper_details


# ✅ CSV Saving Function
def save_to_csv(papers: List[Dict], filename: str):
    """
    Save paper details to a CSV file.
    """
    if not papers:
        logging.warning("No paper details to save.")
        return

    headers = ["id", "title", "date", "authors", "affiliations", "corresponding_email"]

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for paper in papers:
            writer.writerow({
                "id": paper["id"],
                "title": paper["title"],
                "date": paper["date"],
                "authors": "; ".join(paper["authors"]),
                "affiliations": "; ".join(paper["affiliations"]),
                "corresponding_email": paper["corresponding_email"] or "N/A",
            })

    logging.info(f"Results saved to {filename}.")


# ✅ Argument Parsing Function
def parse_arguments():
    """
    Parse command-line arguments using argparse.
    """
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")

    # Required positional argument (query)
    parser.add_argument("query", help="Search query for PubMed (e.g., 'cancer treatment').")

    # Optional arguments
    parser.add_argument("-f", "--file", default="output.csv", help="Output CSV filename (default: output.csv).")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    parser.add_argument("--max-results", type=int, default=10, help="Max number of papers to fetch (default: 10).")

    return parser.parse_args()


# ✅ Main Program Execution
if __name__ == "__main__":
    args = parse_arguments()

    # Enable debug mode if requested
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # Create a PubMed client instance
    client = PubMedClient()

    # Step 1: Search for paper IDs
    paper_ids = client.search_papers(args.query, max_results=args.max_results)

    if not paper_ids:
        logging.info("No papers found. Exiting...")
        exit()

    # Step 2: Fetch paper details
    papers = [client.fetch_paper_details(paper_id) for paper_id in paper_ids]

    # Step 3: Save the results to a CSV file
    save_to_csv(papers, args.file)

