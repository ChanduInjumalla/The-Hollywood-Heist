import pandas as pd
import sqlite3
import re

# Database file name
DB_FILE = 'movies.db'
# Raw CSV file name
CSV_FILE = 'imdb_raw.csv'

def clean_duration(duration_str):
    """'142 min' lanti text ni 142 ane number ga marchali."""
    # re.findall() returns a list of all matches. We take the first one [0].
    # '\d+' ante one or more digits
    match = re.findall(r'\d+', str(duration_str))
    if match:
        return int(match[0])
    return None # Data lekapothe None return chey

def clean_year(year_str):
    """'(1994)' lanti text ni 1994 ane number ga marchali."""
    match = re.findall(r'\d{4}', str(year_str)) # \d{4} ante exactly 4 digits
    if match:
        return int(match[0])
    return None

def clean_votes(votes_str):
    """'1,777,722' lanti text ni 1777722 ane number ga marchali."""
    if pd.isna(votes_str):
        return None
    # ',' (comma) ni remove chesi, number ga convert chey
    return int(str(votes_str).replace(',', ''))

def get_primary_genre(genre_str):
    """'Drama, Crime' lanti text nunchi 'Drama' (first item) matrame teskovali."""
    if pd.isna(genre_str):
        return None
    # ',' (comma) dagara split chesi, first item tesko
    return str(genre_str).split(',')[0].strip()

print(f"PHASE 1: Starting 'The Purification Engine'...")
print(f"Loading raw data from '{CSV_FILE}'...")

try:
    # 1. Load CSV file
    df = pd.read_csv(CSV_FILE)
    
    # 2. Columns ni manaki kavalsina vatiki Rename cheddam
    # Original column names chala messy ga unnai
    df = df.rename(columns={
        'Series_Title': 'Title',
        'Released_Year': 'Year',
        'Runtime': 'Duration',
        'Genre': 'Genre',
        'IMDB_Rating': 'Rating',
        'Director': 'Director',
        'No_of_Votes': 'Votes'
    })
    
    # 3. Manaki kavalsina columns matrame select cheskundam
    # Ee project ki Star1, Star2, Gross lanti columns avasaram ledu
    columns_to_keep = ['Title', 'Year', 'Duration', 'Genre', 'Rating', 'Director', 'Votes']
    df = df[columns_to_keep]
    
    print("Data loaded. Cleaning chestunnanu...")

    # 4. Cleaning Functions ni apply cheddam
    df['Year'] = df['Year'].apply(clean_year)
    df['Duration_Minutes'] = df['Duration'].apply(clean_duration)
    df['Votes'] = df['Votes'].apply(clean_votes)
    
    # Genre ni clean chesi, Primary_Genre ane kotta column create cheddam
    df['Primary_Genre'] = df['Genre'].apply(get_primary_genre)
    
    # 5. Palati columns remove cheddam
    df = df.drop(columns=['Duration', 'Genre'])
    
    # 6. Null values (blank cells) unna rows ni drop cheddam
    # Ee step chala important. Manaki Year or Votes lekapothe analysis kastam.
    df = df.dropna()
    
    # 7. Data types ni correct ga set cheddam (SQL kosam)
    df['Year'] = df['Year'].astype(int)
    df['Duration_Minutes'] = df['Duration_Minutes'].astype(int)
    df['Votes'] = df['Votes'].astype(int)
    df['Rating'] = df['Rating'].astype(float)

    print("Cleaning Complete.")
    print("Clean chesina tarvata data (first 5 rows):")
    print(df.head())

    # 8. DATABASE LO SAVE CHEYADAM
    print(f"\nSaving clean data to SQLite database ({DB_FILE})...")
    conn = sqlite3.connect(DB_FILE)
    
    # DataFrame ni 'movies' ane table lo save chestunam
    df.to_sql('movies', conn, if_exists='replace', index=False)
    conn.close()
    
    print(f"Success! Data antha '{DB_FILE}' file lo save ayindi.")
    print("PHASE 1 COMPLETE.")

except FileNotFoundError:
    print(f"ERROR: '{CSV_FILE}' file dorakaledu.")
    print(f"Please check: File ni '{CSV_FILE}' ga rename chesava?")
except Exception as e:
    print(f"An unexpected error occurred: {e}")