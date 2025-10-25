# Project 1: The Hollywood Heist - IMDb Movie Analysis

### 📊 [View My Interactive Dashboard Here]
*(You will add your published Power BI link here later)*

---

## Objective
The main goal of this project was to execute a complete data analysis workflow. I started with a messy, raw CSV file, cleaned it, built a database, analyzed it with SQL, and finally built a professional, interactive dashboard in Power BI.

---

## Project Workflow
I divided this project into 4 distinct phases:

### 🐍 Phase 1: Python - The Purification Engine
* **File:** `clean_movies.py`
* **Process:** I used the `pandas` library to load the `imdb_raw.csv` file.
* I wrote custom functions to clean messy columns like `Year`, `Duration`, `Votes`, and `Genre`.
* For example: '142 min' was converted to `142` (integer), and '(1994)' was converted to `1994`.
* I used the `sqlite3` library to save the final, clean DataFrame into a new database file named `movies.db`.

### 🔍 Phase 2: SQL - The Interrogation Chamber
* **File:** `analysis.sql`
* **Process:** I connected to the `movies.db` file in VS Code and used SQL to "interrogate" the data and find key insights.
* **Key Questions Answered:**
    1.  Who are the Top 10 Directors (based on average rating, with at least 2 movies)? (`GROUP BY`, `AVG`, `HAVING`)
    2.  How many movies are there in each Genre? (`COUNT`, `GROUP BY`)
    3.  How did the average movie duration change over the years? (`AVG`, `GROUP BY`)

### 📈 Phase 3: Excel - The Manager's Request
* **Process:** I exported the result of a SQL query ('Action' movies) into a `.csv` file.
* I opened this CSV in Excel and created a **PivotTable**.
* **Goal Achieved:** I built a simple report showing the average rating for *Action* movies, broken down by year.

###  dashboards Phase 4: Power BI - The Intelligence Briefing
* **File:** `Hollywood_Heist.pbix` (Your Power BI file name)
* **Process:** I loaded the exported CSV files (results from my SQL queries) into Power BI.
* I built a dynamic, professional, and interactive dashboard from scratch.
* **Dashboard Features:**
    1.  **5 KPI Cards** (Total Movies, Avg Duration, Genres, Oldest Year, Newest Year).
    2.  **3 Main Charts** (Top 10 Directors, Genre Distribution, Duration over Time).
    3.  **2 Interactive Slicers** (Filter by Year and Genre).
    4.  A professional dark theme with visual borders and shadows.
