from habanero import Crossref
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

# Initialize Crossref client
cr = Crossref()

# Function to fetch DOI based on the citation title
def fetch_doi(entry):
    try:
        res = cr.works(query=entry['title'], limit=1)
        items = res['message']['items']
        if items:
            return items[0].get('DOI', None)
    except Exception as e:
        print(f"Error fetching DOI: {e}")
        return None

# Function to update BibTeX file with DOIs
def update_bib_with_doi(bib_file, output_file):
    with open(bib_file, encoding='utf-8') as bibtex_file:
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        bib_database = bibtexparser.load(bibtex_file, parser=parser)

    for entry in bib_database.entries:
        if 'doi' not in entry:
            doi = fetch_doi(entry)
            if doi:
                entry['doi'] = doi

    with open(output_file, 'w', encoding='utf-8') as bibtex_file:
        bibtexparser.dump(bib_database, bibtex_file)

# Replace these filenames with your own
input_bib = 'sample.bib'
output_bib = 'your_references_with_dois.bib'

update_bib_with_doi(input_bib, output_bib)
