"""
Main interaction module for the file storage system
This file demonstrates how to interact with the file storage system from outside the package
"""
import sys
import os
from pathlib import Path

# Add the src directory to the Python path so we can import the kskapp package
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from kskapp import FileStorage


def main():
    """
    Main function to demonstrate interaction with the file storage system
    """
    print("Interactive File Storage System")
    print("=" * 40)
    
    # Initialize the file storage system
    storage = FileStorage("/workspace/storage")
    
    while True:
        print("\nOptions:")
        print("1. Store a file")
        print("2. Search for files")
        print("3. List all files")
        print("4. Load file content")
        print("5. Add tags to a file")
        print("6. View all tags")
        print("7. Delete a file")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == "1":
            source_path = input("Enter the path to the file you want to store: ").strip()
            filename = input("Enter the filename to store it as (or press Enter to keep original): ").strip()
            tags_input = input("Enter tags separated by commas (or press Enter for no tags): ").strip()
            
            tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
            
            try:
                if filename:
                    stored_path = storage.store_file(source_path, filename=filename, tags=tags)
                else:
                    stored_path = storage.store_file(source_path, tags=tags)
                
                print(f"File stored successfully at: {stored_path}")
            except FileNotFoundError:
                print("Error: Source file not found!")
            except Exception as e:
                print(f"Error storing file: {e}")
        
        elif choice == "2":
            query = input("Enter search query (or press Enter to skip): ").strip()
            tags_input = input("Enter tags to search for (separated by commas, or press Enter to skip): ").strip()
            extension = input("Enter file extension to filter by (e.g., .txt, or press Enter to skip): ").strip()
            
            tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else None
            if not extension:
                extension = None
            
            results = storage.search_files(
                query=query if query else None,
                tags=tags,
                extension=extension
            )
            
            print(f"\nFound {len(results)} file(s):")
            for file_info in results:
                print(f"  - {file_info['stored_name']} ({file_info['size']} bytes)")
                print(f"    Tags: {file_info['tags']}")
                print(f"    Path: {file_info['path']}")
                print()
        
        elif choice == "3":
            all_files = storage.list_all_files()
            print(f"\nAll {len(all_files)} file(s) in storage:")
            for file_info in all_files:
                print(f"  - {file_info['stored_name']} ({file_info['size']} bytes)")
                print(f"    Tags: {file_info['tags']}")
                print(f"    Path: {file_info['path']}")
                print()
        
        elif choice == "4":
            filename = input("Enter the filename to load: ").strip()
            try:
                content = storage.load_file_content(filename)
                print(f"\nContent of {filename}:")
                print(content.decode('utf-8', errors='replace')[:500])  # First 500 chars
                if len(content) > 500:
                    print("... (content truncated)")
            except Exception as e:
                print(f"Error loading file: {e}")
        
        elif choice == "5":
            filename = input("Enter the filename to add tags to: ").strip()
            tags_input = input("Enter tags to add (separated by commas): ").strip()
            
            tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
            
            if storage.add_tags(filename, tags):
                file_info = storage.file_index.get(filename)
                print(f"Tags updated for {filename}: {file_info['tags']}")
            else:
                print(f"File {filename} not found!")
        
        elif choice == "6":
            all_tags = storage.get_all_tags()
            print(f"\nAll tags in storage ({len(all_tags)} total):")
            for tag in all_tags:
                print(f"  - {tag}")
        
        elif choice == "7":
            filename = input("Enter the filename to delete: ").strip()
            if storage.delete_file(filename):
                print(f"File {filename} deleted successfully!")
            else:
                print(f"File {filename} not found or could not be deleted!")
        
        elif choice == "8":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()