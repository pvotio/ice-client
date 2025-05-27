# ICE CDS Pricing Data Pipeline

This project provides an automated pipeline for collecting and storing **Credit Default Swap (CDS) single-name settlement prices** published by the **Intercontinental Exchange (ICE)**. It scrapes structured pricing data from the ICE public pricing page, transforms the content into a standardized format, and loads it into a Microsoft SQL Server database.

## Overview

### Objective

This pipeline is designed to:

- Extract CDS settlement prices published by ICE.
- Parse and normalize the data into structured tabular form.
- Insert the clean dataset into a SQL Server table for consumption by internal systems.

This system is ideal for firms requiring reliable access to third-party CDS price curves to support trading, risk management, and compliance workflows.

## Data Source

The primary source for this pipeline is the ICE public data page:

https://www.ice.com/api/cds-settlement-prices/icc-single-names

This page contains structured tables covering:

- CDS Single Names
- Pricing curves by contract, tier, maturity
- Contractual reference entities and market conventions

The scraper dynamically pulls tabular data from this URL and processes it into a standardized form suitable for database ingestion.

## Pipeline Flow

The pipeline follows a straightforward execution flow:

1. **Scraper Initialization**  
   Configures a retry-enabled HTTP scraper with exponential backoff.

2. **Data Fetching**  
   Pulls the pricing table data from the ICE endpoint.

3. **Data Transformation**  
   Cleans, renames, and prepares the DataFrame using the `transformer.Agent`.

4. **Database Insertion**  
   Inserts the transformed records into a specified SQL Server table using `fast-to-sql`.

## Project Structure

```
ice-client-main/
├── main.py                   # Pipeline entrypoint
├── config/                   # Logger and environment config
│   └── settings.py
├── database/                 # Database connection and insertion modules
├── scraper/                  # ICE scraping engine
├── transformer/              # Data transformation logic
├── utils/                    # Inserter abstraction layer
├── .env.sample               # Configuration template
├── Dockerfile                # Containerization support
├── requirements.txt          # Python dependency list
```

## Configuration

Use the `.env.sample` file to create your `.env`. The following variables are required:

| Variable | Description |
|----------|-------------|
| `URL` | ICE data endpoint URL |
| `LOG_LEVEL` | Logging level (e.g., INFO, DEBUG) |
| `OUTPUT_TABLE` | SQL Server target table |
| `INSERTER_MAX_RETRIES` | Number of retry attempts for failed DB inserts |
| `REQUEST_MAX_RETRIES` | Retry attempts for failed HTTP requests |
| `REQUEST_BACKOFF_FACTOR` | Backoff multiplier between retries |
| `MSSQL_SERVER` | SQL Server address |
| `MSSQL_DATABASE` | Target database |
| `MSSQL_USERNAME` / `MSSQL_PASSWORD` | Authentication credentials |

## Docker Support

The pipeline can be containerized for consistent execution in CI/CD pipelines.

### Build the container
```bash
docker build -t ice-client .
```

### Run with configuration
```bash
docker run --env-file .env ice-client
```

## Installation

To install locally:

```bash
pip install -r requirements.txt
```

Primary dependencies:
- `requests`, `lxml`: HTML data scraping
- `pandas`: Data transformation
- `SQLAlchemy`, `pyodbc`: SQL Server integration
- `python-decouple`: Configuration loader

## Execution

Once the environment variables are configured:

```bash
python main.py
```

Logs will report:
- Status of HTTP request
- Number of rows processed
- Success/failure of data insertion

## License

This software is provided under the MIT License. Users must independently verify their right to access and use ICE-published data.
