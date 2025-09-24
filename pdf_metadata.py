import os
from PyPDF2 import PdfReader
from datetime import datetime

def extract_pdf_metadata(file_path):
    """Extract metadata from PDF file"""
    try:
        reader = PdfReader(file_path)
        metadata = reader.metadata
        
        # Get basic file info
        file_stats = os.stat(file_path)
        file_size = file_stats.st_size
        file_size_mb = round(file_size / (1024 * 1024), 2)
        
        # Extract metadata
        pdf_info = {
            'filename': os.path.basename(file_path),
            'filepath': file_path,
            'file_size_mb': file_size_mb,
            'num_pages': len(reader.pages),
            'title': metadata.get('/Title', 'No title') if metadata else 'No title',
            'author': metadata.get('/Author', 'Unknown') if metadata else 'Unknown',
            'subject': metadata.get('/Subject', 'No subject') if metadata else 'No subject',
            'creator': metadata.get('/Creator', 'Unknown') if metadata else 'Unknown',
            'producer': metadata.get('/Producer', 'Unknown') if metadata else 'Unknown',
            'creation_date': metadata.get('/CreationDate', 'Unknown') if metadata else 'Unknown',
            'modification_date': metadata.get('/ModDate', 'Unknown') if metadata else 'Unknown',
            'last_modified': datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Clean up metadata values
        for key, value in pdf_info.items():
            if isinstance(value, str) and value.startswith('D:'):
                # Handle PDF date format
                try:
                    date_str = value[2:]  # Remove 'D:' prefix
                    if len(date_str) >= 14:
                        year = date_str[:4]
                        month = date_str[4:6]
                        day = date_str[6:8]
                        hour = date_str[8:10]
                        minute = date_str[10:12]
                        second = date_str[12:14]
                        pdf_info[key] = f"{year}-{month}-{day} {hour}:{minute}:{second}"
                except:
                    pass
        
        return pdf_info
        
    except Exception as e:
        return {
            'filename': os.path.basename(file_path),
            'filepath': file_path,
            'file_size_mb': 0,
            'num_pages': 0,
            'title': 'Error reading metadata',
            'author': 'Unknown',
            'subject': 'Unknown',
            'creator': 'Unknown',
            'producer': 'Unknown',
            'creation_date': 'Unknown',
            'modification_date': 'Unknown',
            'last_modified': 'Unknown',
            'error': str(e)
        }

def get_pdf_preview(file_path, max_chars=200):
    """Get a preview of PDF content"""
    try:
        reader = PdfReader(file_path)
        first_page_text = reader.pages[0].extract_text()
        
        # Clean and truncate
        preview = first_page_text.strip().replace('\n', ' ').replace('\r', ' ')
        preview = ' '.join(preview.split())  # Remove extra whitespace
        
        if len(preview) > max_chars:
            preview = preview[:max_chars] + "..."
            
        return preview if preview else "No text content found"
        
    except Exception as e:
        return f"Error reading content: {str(e)}"
