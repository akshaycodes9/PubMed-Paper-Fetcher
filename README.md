# 📚 PubMed Paper Fetcher

A powerful Python tool to fetch research papers from **PubMed**, filter by author affiliations, and save results to a **CSV** file.

---

## 🚀 Features

- Fetch papers using the **PubMed API**.
- Save paper details to a **CSV** file.
- Supports **advanced PubMed queries** (e.g., "cancer AND treatment").
- **Filter** papers with non-academic authors (e.g., pharmaceutical or biotech affiliations).
- Handles **API errors** and retries automatically.

---

## 🛠️ Installation

### 1. Clone the repository:

```bash
git clone https://github.com/yourusername/PubMed-Paper-Fetcher.git
cd PubMed-Paper-Fetcher
```

### 2. Set up a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows
```

### 3. Install dependencies:

```bash
pip install -r requirements.txt
```

*Alternatively, you can use [Poetry](https://python-poetry.org) to manage dependencies:*

```bash
pip install poetry
poetry install
```

---

## 📊 Usage

### 1. **Basic Search**

```bash
python main.py "cancer treatment"
```

### 2. **Save Results to a CSV**

```bash
python main.py "cancer treatment" -f output.csv
```

### 3. **Enable Debug Mode**

```bash
python main.py "diabetes" -d
```

### 4. **Fetch More Papers (e.g., 50 results)**

```bash
python main.py "machine learning" --max-results 50
```

### 5. **Filter Non-Academic Authors**

```bash
python main.py "COVID-19 vaccine" --filter-company -f covid_papers.csv
```

*Using Poetry:*

```bash
poetry run main.py "cancer treatment" -f output.csv
```

---

## 📋 CSV Output Format

| Column                  | Description                                      |
|-------------------------|--------------------------------------------------|
| **id**                  | Unique PubMed Paper ID                           |
| **title**               | Paper Title                                      |
| **date**                | Publication Date                                 |
| **authors**             | Author Names (Multiple Separated)                |
| **affiliations**        | Author Affiliations (if available)               |
| **corresponding_email** | Email of the corresponding author (if available) |
| **company_affiliations**| Names of pharmaceutical/biotech companies (if any)|

---

## 🔍 Command-Line Options

| Option             | Description                                        |
|--------------------|----------------------------------------------------|
| `query`            | PubMed search query (e.g., "cancer treatment").    |
| `-f`, `--file`     | Save results to a CSV file (e.g., output.csv).      |
| `-d`, `--debug`    | Enable debug mode for detailed logging.             |
| `--max-results`    | Number of papers to fetch (default: 20).            |
| `--filter-company` | Filter papers with non-academic authors.            |

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🙌 Acknowledgments

Special thanks to **ChatGPT** for assistance in refining this tool.

