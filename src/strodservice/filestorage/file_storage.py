import os
import json
import shutil
from pathlib import Path
from typing import List, Dict, Optional, Union
from datetime import datetime
import mimetypes
from ..config.settings import settings
from ..exceptions import FileValidationError, FileStorageError


class FileStorage:
    """
    A file storage system that allows searching and loading files
    """
    
    def __init__(self, storage_path: str = None, index_file: str = "file_index.json"):
        """
        Initialize the file storage system
        
        Args:
            storage_path: Path where files will be stored (uses config default if None)
            index_file: Name of the file that stores the index of all files
        """
        # Use configured storage path if not provided
        if storage_path is None:
            storage_path = settings.STORAGE_PATH
        
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
    
    def _validate_file(self, source_path: Path) -> None:
        """Validate file before storing it."""
        # Check if file exists
        if not source_path.exists():
            raise FileNotFoundError(f"Source file does not exist: {source_path}")
        
        # Check file size
        file_size = source_path.stat().st_size
        if file_size > settings.MAX_FILE_SIZE:
            raise FileValidationError(
                f"File size {file_size} bytes exceeds maximum allowed size of {settings.MAX_FILE_SIZE} bytes"
            )
        
        # Check file extension
        file_extension = source_path.suffix.lower().lstrip('.')
        if file_extension not in settings.ALLOWED_FILE_EXTENSIONS:
            raise FileValidationError(
                f"File extension '{file_extension}' is not allowed. "
                f"Allowed extensions: {', '.join(settings.ALLOWED_FILE_EXTENSIONS)}"
            )
        
        # Additional security check: prevent directory traversal
        if '..' in str(source_path) or str(source_path).startswith('/'):
            raise FileValidationError("Invalid file path detected")
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to prevent security issues."""
        # Remove any path components to prevent directory traversal
        filename = Path(filename).name
        # Remove potentially dangerous characters
        filename = "".join(c for c in filename if c.isalnum() or c in "._- ")
        return filename.strip()
    
    def store_file(self, source_path: str, filename: str = None, tags: List[str] = None) -> str:
        """
        Store a file in the storage system with validation
        
        Args:
            source_path: Path to the source file
            filename: Desired filename in storage (optional, uses original name if not provided)
            tags: List of tags to associate with the file (optional)
        
        Returns:
            Path to the stored file
        """
        source_path = Path(source_path)
        
        # Validate the file before storing
        self._validate_file(source_path)
        
        if filename is None:
            filename = source_path.name
        else:
            # Sanitize the filename
            filename = self._sanitize_filename(filename)
        
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
        try:
            shutil.copy2(source_path, destination_path)
        except Exception as e:
            raise FileStorageError(f"Failed to copy file: {str(e)}")
        
        # Add to index
        file_info = {
            "original_name": source_path.name,
            "stored_name": destination_path.name,
            "size": destination_path.stat().st_size,
            "created": datetime.fromtimestamp(destination_path.stat().st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(destination_path.stat().st_mtime).isoformat(),
            "path": str(destination_path),
            "mimetype": mimetypes.guess_type(str(destination_path))[0] or "application/octet-stream",
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
        # Sanitize filename to prevent directory traversal
        safe_filename = self._sanitize_filename(filename)
        file_info = self.file_index.get(safe_filename)
        if file_info:
            # Additional security check to ensure the file is within our storage path
            file_path = Path(file_info['path'])
            try:
                # Resolve the path and ensure it's within the storage directory
                resolved_path = file_path.resolve()
                storage_path = self.storage_path.resolve()
                if not str(resolved_path).startswith(str(storage_path)):
                    raise FileStorageError("File path is outside of storage directory")
                return file_info['path']
            except Exception:
                return None
        return None
    
    def load_file_content(self, filename: str) -> bytes:
        """
        Load the content of a stored file with security checks
        
        Args:
            filename: Name of the file to load
            
        Returns:
            File content as bytes
        """
        # Sanitize filename to prevent directory traversal
        safe_filename = self._sanitize_filename(filename)
        file_path = self.get_file_path(safe_filename)
        if not file_path:
            raise FileNotFoundError(f"File not found in storage: {filename}")
        
        file_path_obj = Path(file_path)
        
        # Additional security check to ensure the file is within our storage path
        try:
            resolved_path = file_path_obj.resolve()
            storage_path = self.storage_path.resolve()
            if not str(resolved_path).startswith(str(storage_path)):
                raise FileStorageError("File path is outside of storage directory")
        except Exception:
            raise FileStorageError("Invalid file path")
        
        with open(file_path_obj, 'rb') as f:
            return f.read()
    
    def list_all_files(self) -> List[Dict]:
        """List all files in the storage"""
        return list(self.file_index.values())
    
    def delete_file(self, filename: str) -> bool:
        """
        Delete a file from storage with security checks
        
        Args:
            filename: Name of the file to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        # Sanitize filename to prevent directory traversal
        safe_filename = self._sanitize_filename(filename)
        file_info = self.file_index.get(safe_filename)
        if not file_info:
            return False
        
        try:
            # Remove the physical file
            file_path = Path(file_info['path'])
            
            # Security check: ensure file is within storage directory
            resolved_path = file_path.resolve()
            storage_path = self.storage_path.resolve()
            if not str(resolved_path).startswith(str(storage_path)):
                return False
                
            if file_path.exists():
                file_path.unlink()
            
            # Remove from index
            del self.file_index[safe_filename]
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
        # Sanitize filename to prevent directory traversal
        safe_filename = self._sanitize_filename(filename)
        if safe_filename in self.file_index:
            current_tags = set(self.file_index[safe_filename].get('tags', []))
            current_tags.update(tags)
            self.file_index[safe_filename]['tags'] = list(current_tags)
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