# File Storage System

A flexible file storage system that allows you to store, search, and retrieve files with metadata and tagging capabilities.

## Features

- Store files with metadata (size, creation date, modification date)
- Search files by name, tags, or file extension
- Tag files for better organization
- Retrieve file content or file paths
- Add/remove tags from existing files
- Delete files from storage

## Usage

### Initialize the storage system

```python
from filestorage import FileStorage

# Create a storage instance (defaults to /workspace/storage)
storage = FileStorage("/path/to/storage")
```

### Store a file

```python
# Store a file with tags
stored_path = storage.store_file(
    "/path/to/source/file.txt", 
    filename="my_file.txt",  # Optional: custom filename
    tags=["document", "important", "work"]  # Optional: tags
)
```

### Search for files

```python
# Search by tags
results = storage.search_files(tags=["important"])

# Search by filename query
results = storage.search_files(query="report")

# Search by file extension
results = storage.search_files(extension=".pdf")

# Combine search criteria
results = storage.search_files(query="report", tags=["important"], extension=".pdf")
```

### Load file content

```python
# Get file content as bytes
content = storage.load_file_content("my_file.txt")

# Get file path
path = storage.get_file_path("my_file.txt")
```

### Manage tags

```python
# Add tags to an existing file
storage.add_tags("my_file.txt", ["new_tag", "another_tag"])

# Get all tags in the storage
all_tags = storage.get_all_tags()
```

### List all files

```python
# Get information about all stored files
all_files = storage.list_all_files()
```

### Delete a file

```python
# Delete a file from storage
success = storage.delete_file("my_file.txt")
```

## File Index

The system maintains a JSON file (`file_index.json`) that stores metadata for each file, including:

- Original name
- Stored name
- File size
- Creation and modification dates
- File path
- Associated tags

This enables fast searching without having to scan the filesystem each time.