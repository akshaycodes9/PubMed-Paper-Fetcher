import argparse
from get_papers_list.pubmed_client import PubMedClient
from get_papers_list.paper_filter import PaperFilter
from get_papers_list.csv_writer import CSVWriter

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", help="Search query for PubMed.")
    parser.add_argument("-f", "--file", help="Output CSV filename.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    args = parser.parse_args()

    client = PubMedClient()
    filter = PaperFilter()
    writer = CSVWriter()

    # Fetch paper IDs
    paper_ids = client.search_papers(args.query)
    if args.debug:
        print(f"Found {len(paper_ids)} papers.")

    # Fetch details for each paper
    papers = []
    for paper_id in paper_ids:
        paper_details = client.fetch_paper_details(paper_id)
        papers.append(paper_details)

    # Filter papers
    filtered_papers = filter.filter_papers(papers)
    if args.debug:
        print(f"Filtered {len(filtered_papers)} papers.")

    # Write to CSV or print to console
    if args.file:
        writer.write_to_csv(filtered_papers, args.file)
        print(f"Results saved to {args.file}.")
    else:
        for paper in filtered_papers:
            print(paper)

if __name__ == "__main__":
    main()