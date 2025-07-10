import typer
import pandas as pd
from paper_fetcher.fetcher import search_pubmed, extract_article_data

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
        ids = search_pubmed(query)
        if debug:
            typer.echo(f"Found {len(ids)} papers.")

        data = extract_article_data(ids)
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
