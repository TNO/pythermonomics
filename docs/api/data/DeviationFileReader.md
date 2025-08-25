# DeviationFileReader

**Module:** `pythermonomics.data.read_deviation_file`

Reads deviation files for wells and extracts well name and coordinates.

## Purpose

- Parses well deviation files to obtain well trajectory and coordinate data.
- Handles errors in file format and missing data robustly.

## Main Methods

- `read_deviation_file()`: Returns well name and coordinate data as a tuple.

## Usage

```python
from pythermonomics.data.read_deviation_file import DeviationFileReader

reader = DeviationFileReader(filename="well1.dev")
well_name, coords = reader.read_deviation_file()
```