# paper_fetcher/main.py
import typer
import pandas as pd
from paper_fetcher.fetcher import fetch_pubmed_ids, fetch_details

app = typer.Typer()

@app.command()
def fetch(
    query: str,
    file: str = typer.Option(None, "-f", "--file", help="Output CSV file"),
    debug: bool = typer.Option(False, "-d", "--debug", help="Enable debug mode")
):
    if debug:
        typer.echo(f"Fetching PubMed IDs for query: {query}")
    try:
        ids = fetch_pubmed_ids(query)
        if debug:
            typer.echo(f"Found {len(ids)} papers.")

        data = fetch_details(ids)
        df = pd.DataFrame(data)

        if file:
            df.to_csv(file, index=False)
            typer.echo(f"Saved {len(df)} papers to {file}")
        else:
            typer.echo(df.to_string(index=False))
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)

if __name__ == "__main__":
    app()
