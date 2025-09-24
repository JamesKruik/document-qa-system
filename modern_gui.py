import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
from document_loader import load_and_chunk
from embeddings_manager import create_embeddings, save_embeddings, load_embeddings
from vector_search import find_most_relevant
from qa_agent import ask_gpt, get_available_models, get_model_recommendation

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ModernDocumentQAGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Document Q&A System")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Data storage
        self.loaded_pdfs = []
        self.embeddings = []
        self.embeddings_file = "embeddings.json"
        self.selected_model = "gpt-4o"  # Default to better model
        self.available_models = get_available_models()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="📚 Document Q&A System", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.grid(row=0, column=0, pady=(20, 30))
        
        # Content frame
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)
        
        # PDF Management Section
        self.setup_pdf_section()
        
        # Q&A Section
        self.setup_qa_section()
        
        # Load existing embeddings on startup
        self.load_existing_embeddings()
        
    def setup_pdf_section(self):
        # PDF Management Frame
        self.pdf_frame = ctk.CTkFrame(self.content_frame)
        self.pdf_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        self.pdf_frame.grid_columnconfigure(1, weight=1)
        
        # PDF Section Title
        pdf_title = ctk.CTkLabel(
            self.pdf_frame, 
            text="📄 Document Management", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        pdf_title.grid(row=0, column=0, columnspan=3, pady=(15, 10))
        
        # Load PDFs button
        self.load_btn = ctk.CTkButton(
            self.pdf_frame,
            text="📁 Load PDF Files",
            command=self.load_pdfs,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.load_btn.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="w")
        
        # Process PDFs button
        self.process_btn = ctk.CTkButton(
            self.pdf_frame,
            text="⚡ Process Documents",
            command=self.process_pdfs,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("#3B8ED0", "#1F6AA5"),
            hover_color=("#36719F", "#144870")
        )
        self.process_btn.grid(row=1, column=2, padx=(10, 20), pady=10, sticky="e")
        
        # PDF List Frame
        list_frame = ctk.CTkFrame(self.pdf_frame)
        list_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=20, pady=(0, 15))
        list_frame.grid_columnconfigure(0, weight=1)
        
        # PDF List Label
        list_label = ctk.CTkLabel(list_frame, text="Loaded Documents:", font=ctk.CTkFont(size=12, weight="bold"))
        list_label.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 5))
        
        # PDF Listbox with scrollbar
        self.pdf_listbox = tk.Listbox(
            list_frame,
            height=4,
            bg="#2B2B2B",
            fg="white",
            selectbackground="#3B8ED0",
            font=("Arial", 11),
            relief="flat",
            borderwidth=0
        )
        self.pdf_listbox.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 10))
        
        # Remove PDF button
        self.remove_btn = ctk.CTkButton(
            list_frame,
            text="🗑️ Remove Selected",
            command=self.remove_pdf,
            height=30,
            width=150,
            font=ctk.CTkFont(size=12)
        )
        self.remove_btn.grid(row=2, column=0, pady=(0, 10))
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.pdf_frame, 
            text="Ready to load PDF documents", 
            font=ctk.CTkFont(size=12),
            text_color="#A0A0A0"
        )
        self.status_label.grid(row=3, column=0, columnspan=3, pady=(0, 15))
        
    def setup_qa_section(self):
        # Q&A Frame
        self.qa_frame = ctk.CTkFrame(self.content_frame)
        self.qa_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 20))
        self.qa_frame.grid_columnconfigure(0, weight=1)
        self.qa_frame.grid_rowconfigure(2, weight=1)
        
        # Q&A Section Title
        qa_title = ctk.CTkLabel(
            self.qa_frame, 
            text="💬 Ask Questions", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        qa_title.grid(row=0, column=0, pady=(15, 10))
        
        # Question input frame
        question_frame = ctk.CTkFrame(self.qa_frame)
        question_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        question_frame.grid_columnconfigure(0, weight=1)
        
        # Model selection frame
        model_frame = ctk.CTkFrame(question_frame)
        model_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 10))
        model_frame.grid_columnconfigure(1, weight=1)
        
        # Model selection label
        model_label = ctk.CTkLabel(model_frame, text="🤖 AI Model:", font=ctk.CTkFont(size=12, weight="bold"))
        model_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        # Model selection dropdown
        model_names = [f"{info['name']} ({info['cost']} cost, {info['accuracy']} accuracy)" 
                      for model_id, info in self.available_models.items()]
        self.model_dropdown = ctk.CTkComboBox(
            model_frame,
            values=model_names,
            command=self.on_model_change,
            width=300,
            font=ctk.CTkFont(size=11)
        )
        self.model_dropdown.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady=10)
        self.model_dropdown.set(f"{self.available_models[self.selected_model]['name']} (Medium cost, Excellent accuracy)")
        
        # Question label
        question_label = ctk.CTkLabel(question_frame, text="Your Question:", font=ctk.CTkFont(size=14, weight="bold"))
        question_label.grid(row=1, column=0, sticky="w", padx=15, pady=(10, 5))
        
        # Question entry
        self.question_entry = ctk.CTkEntry(
            question_frame,
            placeholder_text="Type your question here...",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.question_entry.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 15))
        self.question_entry.bind('<Return>', lambda e: self.ask_question())
        
        # Ask button
        self.ask_btn = ctk.CTkButton(
            question_frame,
            text="🔍 Ask Question",
            command=self.ask_question,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("#28A745", "#1E7E34"),
            hover_color=("#218838", "#155724")
        )
        self.ask_btn.grid(row=3, column=0, pady=(0, 15))
        
        # Answer frame
        answer_frame = ctk.CTkFrame(self.qa_frame)
        answer_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        answer_frame.grid_columnconfigure(0, weight=1)
        answer_frame.grid_rowconfigure(1, weight=1)
        
        # Answer label
        answer_label = ctk.CTkLabel(answer_frame, text="Answer:", font=ctk.CTkFont(size=14, weight="bold"))
        answer_label.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 5))
        
        # Answer text area
        self.answer_text = ctk.CTkTextbox(
            answer_frame,
            height=200,
            font=ctk.CTkFont(size=12),
            wrap="word"
        )
        self.answer_text.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        
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
            self.status_label.configure(text=f"✅ Loaded {len(self.loaded_pdfs)} PDF(s). Click 'Process Documents' to create embeddings.")
        
    def remove_pdf(self):
        """Remove selected PDF from the list"""
        selection = self.pdf_listbox.curselection()
        if selection:
            index = selection[0]
            self.pdf_listbox.delete(index)
            del self.loaded_pdfs[index]
            self.status_label.configure(text=f"🗑️ Removed PDF. {len(self.loaded_pdfs)} PDF(s) remaining.")
    
    def process_pdfs(self):
        """Process PDFs and create embeddings in a separate thread"""
        if not self.loaded_pdfs:
            messagebox.showwarning("No PDFs", "Please load some PDF files first.")
            return
        
        # Disable button and show processing status
        self.process_btn.configure(state='disabled', text="⏳ Processing...")
        self.status_label.configure(text="⚙️ Processing PDFs and creating embeddings...")
        
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
        self.process_btn.configure(state='normal', text="⚡ Process Documents")
        self.status_label.configure(text=f"🎉 Successfully processed {len(self.loaded_pdfs)} PDF(s). Ready for questions!")
        self.ask_btn.configure(state='normal')
        messagebox.showinfo("Success", "PDFs processed successfully! You can now ask questions.")
    
    def _processing_error(self, error_msg):
        """Called when PDF processing encounters an error"""
        self.process_btn.configure(state='normal', text="⚡ Process Documents")
        self.status_label.configure(text="❌ Error processing PDFs")
        messagebox.showerror("Error", f"Failed to process PDFs:\n{error_msg}")
    
    def load_existing_embeddings(self):
        """Load existing embeddings if they exist"""
        if os.path.exists(self.embeddings_file):
            try:
                self.embeddings = load_embeddings(self.embeddings_file)
                self.status_label.configure(text="📚 Loaded existing embeddings. Ready for questions!")
                self.ask_btn.configure(state='normal')
            except Exception as e:
                self.status_label.configure(text="❌ Error loading existing embeddings")
                print(f"Error loading embeddings: {e}")
        else:
            self.ask_btn.configure(state='disabled')
    
    def on_model_change(self, choice):
        """Handle model selection change"""
        # Find the model ID from the display name
        for model_id, info in self.available_models.items():
            if info['name'] in choice:
                self.selected_model = model_id
                break
    
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
        model_name = self.available_models[self.selected_model]['name']
        self.ask_btn.configure(state='disabled', text=f"🤔 Thinking with {model_name}...")
        self.answer_text.delete("1.0", "end")
        self.answer_text.insert("1.0", f"Processing your question with {model_name}...")
        
        # Run question answering in separate thread
        thread = threading.Thread(target=self._ask_question_thread, args=(question,))
        thread.daemon = True
        thread.start()
    
    def _ask_question_thread(self, question):
        """Ask question in background thread"""
        try:
            # Find most relevant context
            context = find_most_relevant(question, self.embeddings)
            
            # Get answer from GPT using selected model
            answer = ask_gpt(question, context, model=self.selected_model)
            
            # Update GUI in main thread
            self.root.after(0, self._question_complete, answer)
            
        except Exception as e:
            self.root.after(0, self._question_error, str(e))
    
    def _question_complete(self, answer):
        """Called when question answering is complete"""
        self.ask_btn.configure(state='normal', text="🔍 Ask Question")
        self.answer_text.delete("1.0", "end")
        self.answer_text.insert("1.0", answer)
    
    def _question_error(self, error_msg):
        """Called when question answering encounters an error"""
        self.ask_btn.configure(state='normal', text="🔍 Ask Question")
        self.answer_text.delete("1.0", "end")
        self.answer_text.insert("1.0", f"Error: {error_msg}")
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

def main():
    app = ModernDocumentQAGUI()
    app.run()

if __name__ == "__main__":
    main()
