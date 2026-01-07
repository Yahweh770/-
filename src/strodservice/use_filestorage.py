"""
Example of how to use the file storage system in your application
"""
import sys
from pathlib import Path

# Add the src directory to the path so we can import modules
src_dir = Path(__file__).parent.parent
sys.path.insert(0, str(src_dir))

from strodservice.filestorage.file_storage import FileStorage


def main():
    # Initialize the file storage system
    storage = FileStorage("/workspace/storage")
    
    print("File Storage System - Example Usage")
    print("=" * 40)
    
    # Example 1: Store some files
    print("\n1. Storing files...")
    
    # Store the example file we created
    stored_path = storage.store_file(
        "/workspace/example_file.txt",
        filename="project_document.txt",
        tags=["document", "project", "example"]
    )
    print(f"   Stored: {stored_path}")
    
    # Example 2: Search for files
    print("\n2. Searching for files...")
    
    # Find all documents
    documents = storage.search_files(extension=".txt")
    print(f"   Found {len(documents)} text files:")
    for doc in documents:
        print(f"     - {doc['stored_name']} ({doc['size']} bytes)")
    
    # Find files with specific tags
    project_files = storage.search_files(tags=["project"])
    print(f"   Found {len(project_files)} project-related files:")
    for pf in project_files:
        print(f"     - {pf['stored_name']} (tags: {pf['tags']})")
    
    # Example 3: Load a file
    print("\n3. Loading a file...")
    try:
        content = storage.load_file_content("project_document.txt")
        print(f"   Loaded content: {content[:100].decode('utf-8')}...")  # First 100 chars
    except Exception as e:
        print(f"   Error loading file: {e}")
    
    # Example 4: Add more tags
    print("\n4. Managing tags...")
    storage.add_tags("project_document.txt", ["important", "needs_review"])
    updated_file = storage.file_index.get("project_document.txt")
    print(f"   Updated tags for project_document.txt: {updated_file['tags']}")
    
    # Example 5: List all files
    print("\n5. All stored files:")
    all_files = storage.list_all_files()
    for file_info in all_files:
        print(f"   - {file_info['stored_name']}")
        print(f"     Size: {file_info['size']} bytes")
        print(f"     Tags: {file_info['tags']}")
        print(f"     Path: {file_info['path']}")
        print()


if __name__ == "__main__":
    main()