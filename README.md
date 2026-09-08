# Z-Reading TXT to Monthly PDF Converter

A Python script that automatically reads **daily Z-Reading text files (`.txt`)** and combines them into **monthly PDF reports**.

The script scans folders organized by **year and month**, collects the daily Z-Reading files, and creates one PDF for each month.

## Features

* Reads daily Z-Reading `.txt` files
* Combines daily records into one PDF
* Organizes reports by year and month
* Uses a two-column PDF layout
* Preserves daily file names
* Automatically creates the output folder
* Handles duplicate PDF file names
* Reports the number of files and pages created

## Folder Structure

The source folder should be organized by **year and month**:

```text
Z READING BIR/
│
├── 2025/
│   ├── January/
│   │   ├── January 01.txt
│   │   ├── January 02.txt
│   │   ├── January 03.txt
│   │   └── ...
│   │
│   ├── February/
│   │   ├── February 01.txt
│   │   ├── February 02.txt
│   │   └── ...
│   │
│   └── March/
│       └── ...
│
└── 2026/
    ├── January/
    ├── February/
    └── ...
```

Each `.txt` file represents the **Z-Reading for one day**.

## Output

The script creates one PDF for each month:

```text
CONVERTED/
│
├── January_2025.pdf
├── February_2025.pdf
├── March_2025.pdf
├── January_2026.pdf
├── February_2026.pdf
└── ...
```

For example, all daily Z-Readings inside the `January` folder are combined into:

```text
January_2025.pdf
```

## How It Works

### 1. Locate Text Files

The script searches the selected month folder for `.txt` files.

```python
paths = sorted(folder.glob("*.txt"))
```

### 2. Read Daily Z-Readings

Each text file is opened and its contents are read line by line.

```python
lines = path.read_text(encoding="utf-8").splitlines()
```

The file name is also added as a header to identify each daily Z-Reading.

### 3. Create PDF Content

The text is converted into PDF commands using a **Courier monospaced font**.

The PDF uses a two-column layout to fit more Z-Reading information on each page.

### 4. Create Monthly PDFs

The script checks each year folder and its month folders.

```python
create_year_month_pdfs(source_folder, output_folder)
```

It creates a separate PDF for every month containing `.txt` files.

### 5. Save the Reports

The generated PDFs are saved in the specified output folder.

If a PDF with the same name is already open or cannot be overwritten, the script automatically creates a new filename such as:

```text
January_2025_new.pdf
January_2025_new_2.pdf
```

## Configuration

Change these paths in the main section of the script:

```python
source_folder = r"E:\PROJECTS\Z READING BIR"
output_folder = r"E:\PROJECTS\CONVERTED"
```

### `source_folder`

Contains the folders with the daily Z-Reading text files.

### `output_folder`

Contains the generated monthly PDF reports.

## Requirements

* Python 3.x
* No external Python libraries are required

The script uses Python's built-in:

```python
from pathlib import Path
```

## Running the Program

Save the script as:

```text
zreading_converter.py
```

Then run:

```bash
python zreading_converter.py
```

The program will automatically scan the source folder and generate the monthly PDF reports.

## Example

If the folder contains:

```text
2026/
└── August/
    ├── August 01.txt
    ├── August 02.txt
    ├── August 03.txt
    ├── August 04.txt
    └── ...
```

The program will generate:

```text
August_2026.pdf
```

The PDF will contain the Z-Reading records from the daily `.txt` files.

## Purpose

This project helps reduce the time needed to manually edit, organize, and compile daily Z-Reading text files into monthly PDF reports.

Instead of creating PDF reports manually, the script automates the process.

## Author

Developed as a Python automation project for organizing and converting daily Z-Reading records into monthly PDF reports.
