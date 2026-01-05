import os
import json
import shutil
from pathlib import Path
from typing import List, Dict, Optional, Union
from datetime import datetime


class FileStorage:
    """
    A file storage system that allows searching and loading files
    """
    
    def __init__(self, storage_path: str = "/workspace/storage", index_file: str = "file_index.json"):
        """
        Initialize the file storage system
        
        Args:
            storage_path: Path where files will be stored
            index_file: Name of the file that stores the index of all files
        """
        self.storage_path = Path(storage_path)
        self.index_file = self.storage_path / index_file
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Load existing index or create new one
        self.file_index = self._load_index()
    
    def _load_index(self) -> Dict:
        """Load the file index from disk"""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def _save_index(self):
        """Save the file index to disk"""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.file_index, f, ensure_ascii=False, indent=2)
    
    def store_file(self, source_path: str, filename: str = None, tags: List[str] = None) -> str:
        """
        Store a file in the storage system
        
        Args:
            source_path: Path to the source file
            filename: Desired filename in storage (optional, uses original name if not provided)
            tags: List of tags to associate with the file (optional)
        
        Returns:
            Path to the stored file
        """
        source_path = Path(source_path)
        
        if not source_path.exists():
            raise FileNotFoundError(f"Source file does not exist: {source_path}")
        
        if filename is None:
            filename = source_path.name
        
        # Create destination path
        destination_path = self.storage_path / filename
        
        # Handle duplicate filenames
        counter = 1
        original_destination = destination_path
        while destination_path.exists():
            stem = original_destination.stem
            suffix = original_destination.suffix
            destination_path = self.storage_path / f"{stem}_{counter}{suffix}"
            counter += 1
        
        # Copy file to storage
        shutil.copy2(source_path, destination_path)
        
        # Add to index
        file_info = {
            "original_name": source_path.name,
            "stored_name": destination_path.name,
            "size": destination_path.stat().st_size,
            "created": datetime.fromtimestamp(destination_path.stat().st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(destination_path.stat().st_mtime).isoformat(),
            "path": str(destination_path),
            "tags": tags or []
        }
        
        self.file_index[destination_path.name] = file_info
        self._save_index()
        
        return str(destination_path)
    
    def search_files(self, query: str = None, tags: List[str] = None, extension: str = None) -> List[Dict]:
        """
        Search for files in the storage system
        
        Args:
            query: Text query to search in filenames
            tags: List of tags to filter by
            extension: File extension to filter by
        
        Returns:
            List of matching file information
        """
        results = []
        
        for filename, file_info in self.file_index.items():
            match = True
            
            # Check query match in filename
            if query and query.lower() not in filename.lower():
                match = False
            
            # Check tags
            if tags and not any(tag in file_info.get('tags', []) for tag in tags):
                match = False
            
            # Check extension
            if extension and not filename.lower().endswith(extension.lower()):
                match = False
            
            if match:
                results.append(file_info)
        
        return results
    
    def get_file_path(self, filename: str) -> Optional[str]:
        """
        Get the path to a stored file by its name
        
        Args:
            filename: Name of the file to retrieve
            
        Returns:
            Path to the file or None if not found
        """
        file_info = self.file_index.get(filename)
        if file_info:
            return file_info['path']
        return None
    
    def load_file_content(self, filename: str) -> bytes:
        """
        Load the content of a stored file
        
        Args:
            filename: Name of the file to load
            
        Returns:
            File content as bytes
        """
        file_path = self.get_file_path(filename)
        if not file_path:
            raise FileNotFoundError(f"File not found in storage: {filename}")
        
        with open(file_path, 'rb') as f:
            return f.read()
    
    def list_all_files(self) -> List[Dict]:
        """List all files in the storage"""
        return list(self.file_index.values())
    
    def delete_file(self, filename: str) -> bool:
        """
        Delete a file from storage
        
        Args:
            filename: Name of the file to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        file_info = self.file_index.get(filename)
        if not file_info:
            return False
        
        try:
            # Remove the physical file
            file_path = Path(file_info['path'])
            if file_path.exists():
                file_path.unlink()
            
            # Remove from index
            del self.file_index[filename]
            self._save_index()
            return True
        except Exception:
            return False
    
    def add_tags(self, filename: str, tags: List[str]) -> bool:
        """
        Add tags to a file
        
        Args:
            filename: Name of the file
            tags: Tags to add
            
        Returns:
            True if successful, False otherwise
        """
        if filename in self.file_index:
            current_tags = set(self.file_index[filename].get('tags', []))
            current_tags.update(tags)
            self.file_index[filename]['tags'] = list(current_tags)
            self._save_index()
            return True
        return False
    
    def get_all_tags(self) -> List[str]:
        """Get all unique tags in the storage"""
        all_tags = set()
        for file_info in self.file_index.values():
            tags = file_info.get('tags', [])
            all_tags.update(tags)
        return sorted(list(all_tags))


# Example usage
if __name__ == "__main__":
    # Create a file storage instance
    storage = FileStorage("/workspace/storage")
    
    # Example: Store a file (if you have a file to store)
    # storage.store_file("/path/to/your/file.txt", tags=["document", "important"])
    
    # Example: Search files
    # results = storage.search_files(query="report", tags=["important"])
    # print(results)
    
    print("File storage system initialized.")
    print(f"Storage path: {storage.storage_path}")
    print(f"Number of files in storage: {len(storage.list_all_files())}")