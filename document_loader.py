from PyPDF2 import PdfReader
import re
import os

def load_pdf(file_path):
    """Load PDF and extract text from all pages"""
    reader = PdfReader(file_path)
    texts = []
    for page in reader.pages:
        text = page.extract_text()
        if text.strip():  # Only add non-empty pages
            texts.append(text.strip())
    return texts

def clean_text(text):
    """Clean and normalize text"""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove page numbers and headers/footers (simple patterns)
    text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
    return text.strip()

def chunk_text(text, chunk_size=1000, overlap=200):
    """Split text into overlapping chunks for better context preservation"""
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # Try to break at sentence boundaries
        if end < len(text):
            # Look for sentence endings within the last 100 characters
            sentence_end = text.rfind('.', start, end)
            if sentence_end > start + chunk_size * 0.7:  # If we found a sentence end reasonably close
                end = sentence_end + 1
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        # Move start position with overlap
        start = end - overlap
        if start >= len(text):
            break
    
    return chunks

def load_and_chunk(files):
    """Load multiple PDFs and return all chunks with metadata"""
    all_chunks = []
    
    for file_path in files:
        if file_path.endswith(".pdf"):
            print(f"Processing PDF: {file_path}")
            texts = load_pdf(file_path)
            
            for page_num, text in enumerate(texts, 1):
                # Clean the text
                cleaned_text = clean_text(text)
                if not cleaned_text:
                    continue
                
                # Chunk the text
                chunks = chunk_text(cleaned_text)
                
                for chunk_num, chunk in enumerate(chunks):
                    all_chunks.append({
                        'text': chunk,
                        'source_file': file_path,
                        'page': page_num,
                        'chunk_id': f"{os.path.basename(file_path)}_p{page_num}_c{chunk_num}"
                    })
        else:
            # Handle other file types
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
                cleaned_text = clean_text(text)
                chunks = chunk_text(cleaned_text)
                
                for chunk_num, chunk in enumerate(chunks):
                    all_chunks.append({
                        'text': chunk,
                        'source_file': file_path,
                        'page': 1,
                        'chunk_id': f"{os.path.basename(file_path)}_c{chunk_num}"
                    })
    
    print(f"Created {len(all_chunks)} chunks from {len(files)} files")
    return all_chunks
