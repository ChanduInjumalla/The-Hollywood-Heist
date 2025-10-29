import pandas as pd
import sqlite3
import re

DB_FILE = 'movies.db'
CSV_FILE = 'imdb_raw.csv'

def clean_duration(duration_str):
    """'142 min' lanti text ni 142 ane number ga marchali."""
    match = re.findall(r'\d+', str(duration_str))
    if match:
        return int(match[0])
    return None

def clean_year(year_str):
    """'(1994)' lanti text ni 1994 ane number ga marchali."""
    match = re.findall(r'\d{4}', str(year_str)) 
    if match:
        return int(match[0])
    return None

def clean_votes(votes_str):
    """'1,777,722' lanti text ni 1777722 ane number ga marchali."""
    if pd.isna(votes_str):
        return None
    return int(str(votes_str).replace(',', ''))

def get_primary_genre(genre_str):
    """'Drama, Crime' lanti text nunchi 'Drama' (first item) matrame teskovali."""
    if pd.isna(genre_str):
        return None
    return str(genre_str).split(',')[0].strip()

print(f"PHASE 1: Starting 'The Purification Engine'...")
print(f"Loading raw data from '{CSV_FILE}'...")

try:
    df = pd.read_csv(CSV_FILE)
    
    df = df.rename(columns={
        'Series_Title': 'Title',
        'Released_Year': 'Year',
        'Runtime': 'Duration',
        'Genre': 'Genre',
        'IMDB_Rating': 'Rating',
        'Director': 'Director',
        'No_of_Votes': 'Votes'
    })
    
    columns_to_keep = ['Title', 'Year', 'Duration', 'Genre', 'Rating', 'Director', 'Votes']
    df = df[columns_to_keep]
    
    print("Data loaded. Cleaning chestunnanu...")

    df['Year'] = df['Year'].apply(clean_year)
    df['Duration_Minutes'] = df['Duration'].apply(clean_duration)
    df['Votes'] = df['Votes'].apply(clean_votes)
    
    df['Primary_Genre'] = df['Genre'].apply(get_primary_genre)
    
    df = df.drop(columns=['Duration', 'Genre'])
    
    df = df.dropna()
    
    df['Year'] = df['Year'].astype(int)
    df['Duration_Minutes'] = df['Duration_Minutes'].astype(int)
    df['Votes'] = df['Votes'].astype(int)
    df['Rating'] = df['Rating'].astype(float)

    print("Cleaning Complete.")
    print("Clean chesina tarvata data (first 5 rows):")
    print(df.head())

    print(f"\nSaving clean data to SQLite database ({DB_FILE})...")
    conn = sqlite3.connect(DB_FILE)
    
    df.to_sql('movies', conn, if_exists='replace', index=False)
    conn.close()
    
    print(f"Success! Data antha '{DB_FILE}' file lo save ayindi.")
    print("PHASE 1 COMPLETE.")

except FileNotFoundError:
    print(f"ERROR: '{CSV_FILE}' file dorakaledu.")
    print(f"Please check: File ni '{CSV_FILE}' ga rename chesava?")
except Exception as e:
    print(f"An unexpected error occurred: {e}")