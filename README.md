# Excel to PostgreSQL DB

A simple script to transfers data on Excel to PostgreSQL database.

## Table of Contents
- [Setup](#setup)
- [Usage](#usage)
- [Config Documentation](#config-documentation)

---

## Setup
To set up the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/project-name.git
2. Create a virtual environment and activate it
   - <details> <summary>Linux/MacOS </summary>
  
        ```bash
        # create virtual env
        python -m venv yourvenv
        # activate env
        source yourvenv\Scripts\activate
        ```
    </details>

   - <details> <summary>Windows CMD </summary>
        
        ```bash
        # create virtual env
        python -m venv yourvenv
        # activate virtual env
        venv\Scripts\activate
        ```
    </details>

3. Install dependencies from requirements.txt
    ```bash
   # Windows CMD/MacOS/Linux
    pip install -r requirements.txt
    ```
4. Run pyinstaller to create executable
   ```bash
   pyinstaller --onefile path/to/excel_to_postgres.py
   ```

## Usage
Fill out the information in the [config.json](#config-documentation) file and pass the path to the excel_to_postgres executable. Alternatively you can also use the excel_to_postgres.py script directly.

Using the executable
```bash
.\excel_to_postgres.exe -p path/to/config.json  # can rename config.json
```
Using script
```bash
python excel_to_postgres.py -p path/to/config.json # can rename config.json
```

## Config Documentation
For detailed information, refer to the config_schema.json. The following is a config example.
```json
{
    "Excel": {
        "source": "my_excel.xlsx",
        "sheet_names": ["example_sheet"]
    },
    "Postgres-DB": {
        "username": "postgres",
        "password": "secret",
        "db_name": "my_db",
        "server": "localhost",
        "port": "5432"
    },
    "name_map": {
        "example_sheet" : "product_prices"
    }
}
```
### Required Configurations
- ### Excel
  - **source** *(sting)* : Path to the Excel workbook. If source Excel is in other folder, use absolute path.
  - **sheet_names** *(array)* : Name of the sheet to replicate. Must include at least one sheet. 
- ### Postgres-DB
  - **username** *(string)* : Username of the PostgreSQL user
  - **password** *(string)* : Password of the PostgreSQL user
  - **db_name** *(string)* : Name of the database user is trying to connect to.
  - **server** *(string)* : Name of the server the database is hosted on, e.g. localhost, host.docker.interal
  - **port** *(string)* : The port the database is listening on. If the DB is hosted on Docker, then port will be the machine port that is mapped to the container port
  
### Optional Configurations
- **name_map** *(object)* : Maps the name of the sheet in the source to the new name. When a table is created from that sheet, the new name will be assigned to the table. E.g. source: example_sheet ---- table name: product_prices