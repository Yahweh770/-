# File Storage System

The File Storage System provides functionality to store, search, and retrieve files with metadata and tagging capabilities.

## Overview

The system allows you to:
- Store files with automatic metadata collection
- Search files by name, tags, or extension
- Tag files for better organization
- Load file content programmatically
- Manage files through a persistent index

## Architecture

```
/workspace/src/kskapp/filestorage/
├── __init__.py           # Package initialization
├── file_storage.py       # Main FileStorage class
```

## Usage

### Direct Import (from within the kskapp package):

```python
from .filestorage import FileStorage

# Initialize storage
storage = FileStorage("/workspace/storage")

# Store a file
storage.store_file("/path/to/file.txt", tags=["document", "important"])

# Search for files
results = storage.search_files(tags=["important"], extension=".txt")

# Load file content
content = storage.load_file_content("filename.txt")
```

### External Import (from outside the package):

```python
import sys
from pathlib import Path

# Add the src directory to the path so we can import modules
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from kskapp.filestorage import FileStorage

# Now use the storage system as above
```

### Using the Package Import:

```python
import sys
from pathlib import Path

# Add the src directory to the path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from kskapp import FileStorage

# Initialize and use
storage = FileStorage("/workspace/storage")
```

## Main Interaction Script

The `interact_filestorage.py` script in the main workspace directory provides an interactive command-line interface to the file storage system. Run it with:

```bash
python interact_filestorage.py
```

## API Reference

### FileStorage Class

#### `__init__(storage_path="/workspace/storage", index_file="file_index.json")`
Initialize the file storage system.

#### `store_file(source_path, filename=None, tags=None)`
Store a file in the system with optional custom filename and tags.

#### `search_files(query=None, tags=None, extension=None)`
Search for files by query, tags, or extension.

#### `get_file_path(filename)`
Get the path to a stored file by its name.

#### `load_file_content(filename)`
Load the content of a stored file as bytes.

#### `list_all_files()`
List all files in the storage with their metadata.

#### `delete_file(filename)`
Delete a file from storage.

#### `add_tags(filename, tags)`
Add tags to an existing file.

#### `get_all_tags()`
Get all unique tags in the storage system.

## Examples

Check out the example files:
- `/workspace/src/kskapp/filestorage_demo.py` - Complete demonstration
- `/workspace/src/kskapp/use_filestorage.py` - Practical usage example
- `/workspace/interact_filestorage.py` - Interactive command-line interface