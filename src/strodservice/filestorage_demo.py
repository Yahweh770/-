"""
Demo script for the file storage system
"""
import os
import sys
from pathlib import Path

# Add the src directory to the path so we can import modules
src_dir = Path(__file__).parent.parent
sys.path.insert(0, str(src_dir))

from kskapp.filestorage import FileStorage


def demo_file_storage():
    print("=== File Storage System Demo ===\n")
    
    # Create a file storage instance
    storage = FileStorage("/workspace/storage")
    print(f"Storage initialized at: {storage.storage_path}\n")
    
    # Store a file
    print("1. Storing a file...")
    stored_path = storage.store_file(
        "/workspace/example_file.txt", 
        filename="demo_file.txt",
        tags=["demo", "text", "example"]
    )
    print(f"   File stored at: {stored_path}\n")
    
    # Store another file with different tags
    print("2. Storing another file...")
    # Create a second example file
    with open("/workspace/another_file.txt", "w") as f:
        f.write("This is another example file with different content.")
    
    stored_path2 = storage.store_file(
        "/workspace/another_file.txt",
        filename="another_file.txt",
        tags=["demo", "text", "secondary"]
    )
    print(f"   File stored at: {stored_path2}\n")
    
    # List all files
    print("3. Listing all files in storage:")
    all_files = storage.list_all_files()
    for file_info in all_files:
        print(f"   - {file_info['stored_name']} ({file_info['size']} bytes)")
        print(f"     Tags: {file_info['tags']}")
        print(f"     Path: {file_info['path']}\n")
    
    # Search files by tag
    print("4. Searching files with tag 'demo':")
    demo_files = storage.search_files(tags=["demo"])
    for file_info in demo_files:
        print(f"   - {file_info['stored_name']} with tags: {file_info['tags']}")
    print()
    
    # Search files by query
    print("5. Searching files containing 'demo' in filename:")
    query_results = storage.search_files(query="demo")
    for file_info in query_results:
        print(f"   - {file_info['stored_name']}")
    print()
    
    # Load file content
    print("6. Loading content of 'demo_file.txt':")
    try:
        content = storage.load_file_content("demo_file.txt")
        print(f"   Content: {content.decode('utf-8')}")
    except Exception as e:
        print(f"   Error loading file: {e}")
    print()
    
    # Get specific file path
    print("7. Getting path for 'demo_file.txt':")
    path = storage.get_file_path("demo_file.txt")
    print(f"   Path: {path}\n")
    
    # Add more tags to a file
    print("8. Adding more tags to 'demo_file.txt':")
    success = storage.add_tags("demo_file.txt", ["important", "tutorial"])
    if success:
        file_info = storage.file_index.get("demo_file.txt")
        print(f"   Updated tags: {file_info['tags']}")
    print()
    
    # Show all available tags
    print("9. All available tags in storage:")
    all_tags = storage.get_all_tags()
    print(f"   {all_tags}\n")
    
    # Search with multiple criteria
    print("10. Searching files with tag 'demo' AND query 'demo':")
    multi_results = storage.search_files(query="demo", tags=["demo"])
    for file_info in multi_results:
        print(f"    - {file_info['stored_name']} with tags: {file_info['tags']}")
    print()
    
    # Clean up demo files
    print("11. Cleaning up demo files...")
    os.remove("/workspace/another_file.txt")
    print("   Demo files cleaned up.\n")
    
    print("=== Demo completed successfully! ===")


if __name__ == "__main__":
    demo_file_storage()