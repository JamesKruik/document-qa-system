#!/usr/bin/env python3
"""
Test script to demonstrate markdown rendering in the Document Q&A System
"""

import customtkinter as ctk
import tkinter as tk
import re
from tkinter import font as tkfont

def render_markdown_to_tk_text(textbox: tk.Text, content: str):
    """Render markdown content to a tkinter Text widget with formatting"""
    textbox.configure(state="normal")
    textbox.delete("1.0", "end")

    lines = content.splitlines()
    for line in lines:
        # --- Headers & bullets ---
        if line.startswith("# "):
            textbox.insert("end", line[2:].strip() + "\n", "h1")
            continue
        elif line.startswith("## "):
            textbox.insert("end", line[3:].strip() + "\n", "h2")
            continue
        elif line.startswith("- "):
            line = "• " + line[2:].strip()

        # --- Inline formatting ---
        pos = 0
        for match in re.finditer(r"\*\*(.*?)\*\*|\*(.*?)\*|`(.*?)`", line):
            start, end = match.span()
            # normal text before match
            textbox.insert("end", line[pos:start])

            if match.group(1):  # **bold**
                textbox.insert("end", match.group(1), "bold")
            elif match.group(2):  # *italic*
                textbox.insert("end", match.group(2), "italic")
            elif match.group(3):  # `code`
                textbox.insert("end", match.group(3), "code")

            pos = end
        textbox.insert("end", line[pos:] + "\n")

    textbox.configure(state="disabled")

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Create the main window
app = ctk.CTk()
app.geometry("900x600")
app.title("Document Q&A - Markdown Rendering Test")

# Main frame
frame = ctk.CTkFrame(app)
frame.pack(fill="both", expand=True, padx=16, pady=16)

# Title
title_label = ctk.CTkLabel(
    frame, 
    text="📚 Markdown Rendering Test", 
    font=ctk.CTkFont(size=24, weight="bold")
)
title_label.pack(pady=(20, 30))

# Answer text area with markdown support
answer_box = tk.Text(
    frame,
    wrap="word",
    bg="#1e1e1e",
    fg="white",
    insertbackground="white",
    relief="flat",
    padx=12,
    pady=8,
    font=("Segoe UI", 12)
)
answer_box.pack(fill="both", expand=True, padx=20, pady=(0, 20))

# Configure markdown text tags
default_font = tkfont.Font(family="Segoe UI", size=12)
bold_font = tkfont.Font(family="Segoe UI", size=12, weight="bold")
italic_font = tkfont.Font(family="Segoe UI", size=12, slant="italic")
code_font = tkfont.Font(family="Consolas", size=11)
h1_font = tkfont.Font(family="Segoe UI", size=18, weight="bold")
h2_font = tkfont.Font(family="Segoe UI", size=15, weight="bold")

answer_box.configure(font=default_font)

# Configure text tags
answer_box.tag_config("bold", font=bold_font)
answer_box.tag_config("italic", font=italic_font)
answer_box.tag_config("code", font=code_font, background="#333333")
answer_box.tag_config("h1", font=h1_font, foreground="#00e0e0", spacing3=8)
answer_box.tag_config("h2", font=h2_font, foreground="#ffaa00", spacing3=4)

# Sample markdown content
sample_markdown = """
# Document Q&A System Features

This system provides **powerful document analysis** capabilities with *intelligent* question answering.

## Key Features

- **Vector Search**: Find relevant content using semantic similarity
- **Multiple AI Models**: Support for GPT-4, GPT-3.5, and other models
- **PDF Processing**: Extract and analyze PDF documents
- **Markdown Rendering**: Beautiful text formatting with `code blocks`

## How It Works

The system uses **Retrieval-Augmented Generation (RAG)** to:

1. Process your documents and create embeddings
2. Find the most relevant content for your question
3. Generate accurate answers using AI models

### Example Code Usage

```python
# Load documents
chunks = load_and_chunk(pdf_files)

# Create embeddings
embeddings = create_embeddings(chunks)

# Ask questions
answer = ask_gpt(question, context)
```

## Benefits

- **Accurate**: Grounded in your actual documents
- **Fast**: Efficient vector search and caching
- **Flexible**: Works with any PDF documents
- **User-friendly**: Modern GUI with markdown support

*Ready to test your documents?* Load some PDFs and start asking questions!
"""

# Render the markdown content
render_markdown_to_tk_text(answer_box, sample_markdown)

# Start the application
app.mainloop()
