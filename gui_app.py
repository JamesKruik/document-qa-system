import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from document_loader import load_and_chunk
from embeddings_manager import create_embeddings, save_embeddings, load_embeddings
from vector_search import find_most_relevant
from qa_agent import ask_gpt

class DocumentQAGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Document Q&A System")
        self.root.geometry("800x600")
        
        # Data storage
        self.loaded_pdfs = []
        self.embeddings = []
        self.embeddings_file = "embeddings.json"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # PDF Loading Section
        pdf_frame = ttk.LabelFrame(main_frame, text="PDF Documents", padding="10")
        pdf_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        pdf_frame.columnconfigure(1, weight=1)
        
        # Load PDF button
        ttk.Button(pdf_frame, text="Load PDF Files", command=self.load_pdfs).grid(row=0, column=0, padx=(0, 10))
        
        # PDF listbox
        self.pdf_listbox = tk.Listbox(pdf_frame, height=4)
        self.pdf_listbox.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Remove PDF button
        ttk.Button(pdf_frame, text="Remove Selected", command=self.remove_pdf).grid(row=0, column=2)
        
        # Process PDFs button
        self.process_btn = ttk.Button(pdf_frame, text="Process PDFs", command=self.process_pdfs)
        self.process_btn.grid(row=1, column=0, columnspan=3, pady=(10, 0))
        
        # Status label
        self.status_label = ttk.Label(pdf_frame, text="Ready to load PDFs")
        self.status_label.grid(row=2, column=0, columnspan=3, pady=(5, 0))
        
        # Q&A Section
        qa_frame = ttk.LabelFrame(main_frame, text="Ask Questions", padding="10")
        qa_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        qa_frame.columnconfigure(0, weight=1)
        
        # Question input
        ttk.Label(qa_frame, text="Your Question:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.question_entry = ttk.Entry(qa_frame)
        self.question_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.question_entry.bind('<Return>', lambda e: self.ask_question())
        
        # Ask button
        self.ask_btn = ttk.Button(qa_frame, text="Ask Question", command=self.ask_question)
        self.ask_btn.grid(row=2, column=0, pady=(0, 10))
        
        # Answer display
        ttk.Label(qa_frame, text="Answer:").grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        self.answer_text = scrolledtext.ScrolledText(qa_frame, height=8, wrap=tk.WORD)
        self.answer_text.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure answer text grid weight
        qa_frame.rowconfigure(4, weight=1)
        
        # Load existing embeddings on startup
        self.load_existing_embeddings()
        
    def load_pdfs(self):
        """Open file dialog to select PDF files"""
        files = filedialog.askopenfilenames(
            title="Select PDF Files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        for file in files:
            if file not in self.loaded_pdfs:
                self.loaded_pdfs.append(file)
                self.pdf_listbox.insert(tk.END, os.path.basename(file))
        
        if self.loaded_pdfs:
            self.status_label.config(text=f"Loaded {len(self.loaded_pdfs)} PDF(s). Click 'Process PDFs' to create embeddings.")
        
    def remove_pdf(self):
        """Remove selected PDF from the list"""
        selection = self.pdf_listbox.curselection()
        if selection:
            index = selection[0]
            self.pdf_listbox.delete(index)
            del self.loaded_pdfs[index]
            self.status_label.config(text=f"Removed PDF. {len(self.loaded_pdfs)} PDF(s) remaining.")
    
    def process_pdfs(self):
        """Process PDFs and create embeddings in a separate thread"""
        if not self.loaded_pdfs:
            messagebox.showwarning("No PDFs", "Please load some PDF files first.")
            return
        
        # Disable button and show processing status
        self.process_btn.config(state='disabled', text="Processing...")
        self.status_label.config(text="Processing PDFs and creating embeddings...")
        
        # Run processing in separate thread to avoid GUI freezing
        thread = threading.Thread(target=self._process_pdfs_thread)
        thread.daemon = True
        thread.start()
    
    def _process_pdfs_thread(self):
        """Process PDFs in background thread"""
        try:
            # Load and chunk documents
            chunks = load_and_chunk(self.loaded_pdfs)
            
            # Create embeddings
            embeddings = create_embeddings(chunks)
            
            # Save embeddings
            save_embeddings(embeddings, self.embeddings_file)
            
            # Update GUI in main thread
            self.root.after(0, self._processing_complete, embeddings)
            
        except Exception as e:
            self.root.after(0, self._processing_error, str(e))
    
    def _processing_complete(self, embeddings):
        """Called when PDF processing is complete"""
        self.embeddings = embeddings
        self.process_btn.config(state='normal', text="Process PDFs")
        self.status_label.config(text=f"Successfully processed {len(self.loaded_pdfs)} PDF(s). Ready for questions!")
        self.ask_btn.config(state='normal')
        messagebox.showinfo("Success", "PDFs processed successfully! You can now ask questions.")
    
    def _processing_error(self, error_msg):
        """Called when PDF processing encounters an error"""
        self.process_btn.config(state='normal', text="Process PDFs")
        self.status_label.config(text="Error processing PDFs")
        messagebox.showerror("Error", f"Failed to process PDFs:\n{error_msg}")
    
    def load_existing_embeddings(self):
        """Load existing embeddings if they exist"""
        if os.path.exists(self.embeddings_file):
            try:
                self.embeddings = load_embeddings(self.embeddings_file)
                self.status_label.config(text="Loaded existing embeddings. Ready for questions!")
                self.ask_btn.config(state='normal')
            except Exception as e:
                self.status_label.config(text="Error loading existing embeddings")
                print(f"Error loading embeddings: {e}")
        else:
            self.ask_btn.config(state='disabled')
    
    def ask_question(self):
        """Ask a question using the loaded embeddings"""
        if not self.embeddings:
            messagebox.showwarning("No Data", "Please process some PDFs first or ensure embeddings.json exists.")
            return
        
        question = self.question_entry.get().strip()
        if not question:
            messagebox.showwarning("No Question", "Please enter a question.")
            return
        
        # Disable ask button and show processing
        self.ask_btn.config(state='disabled', text="Thinking...")
        self.answer_text.delete(1.0, tk.END)
        self.answer_text.insert(tk.END, "Processing your question...")
        
        # Run question answering in separate thread
        thread = threading.Thread(target=self._ask_question_thread, args=(question,))
        thread.daemon = True
        thread.start()
    
    def _ask_question_thread(self, question):
        """Ask question in background thread"""
        try:
            # Find most relevant context
            context = find_most_relevant(question, self.embeddings)
            
            # Get answer from GPT
            answer = ask_gpt(question, context)
            
            # Update GUI in main thread
            self.root.after(0, self._question_complete, answer)
            
        except Exception as e:
            self.root.after(0, self._question_error, str(e))
    
    def _question_complete(self, answer):
        """Called when question answering is complete"""
        self.ask_btn.config(state='normal', text="Ask Question")
        self.answer_text.delete(1.0, tk.END)
        self.answer_text.insert(tk.END, answer)
    
    def _question_error(self, error_msg):
        """Called when question answering encounters an error"""
        self.ask_btn.config(state='normal', text="Ask Question")
        self.answer_text.delete(1.0, tk.END)
        self.answer_text.insert(tk.END, f"Error: {error_msg}")

def main():
    root = tk.Tk()
    app = DocumentQAGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
