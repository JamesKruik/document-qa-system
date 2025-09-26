# Document Q&A System

A modern, AI-powered document question and answer system built with Python and OpenAI's API.

## 🚀 Features

- **Modern GUI**: Sleek CustomTkinter interface with dark theme
- **Multiple AI Models**: Choose from GPT-4o Mini, GPT-4o, GPT-3.5 Turbo, or GPT-4
- **Smart PDF Processing**: Intelligent text chunking with overlap for better context
- **Vector Search**: Advanced similarity search for relevant document sections
- **Real-time Q&A**: Interactive question answering with progress indicators

## 📁 Project Structure

```
document_searcher/
├── main.py                 # Original command-line interface
├── modern_gui.py          # Modern GUI application
├── run_gui.py             # GUI launcher script
├── query_manager.py       # Command-line query interface
├── qa_agent.py            # AI model interface
├── document_loader.py     # PDF processing and chunking
├── embeddings_manager.py  # Vector embeddings management
├── vector_search.py      # Similarity search
├── pdf_metadata.py       # PDF metadata extraction
├── model_comparison.py   # Model performance testing
├── gui_app.py            # Original GUI (legacy)
├── api_testing.py        # API testing utilities
├── view_usage.py         # Usage monitoring
└── README.md             # This file
```

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/JamesKruik/document-qa-system.git
   cd document-qa-system/document_searcher
   ```

2. **Install dependencies**:
   ```bash
   pip install openai python-dotenv PyPDF2 numpy customtkinter
   ```

3. **Set up environment variables**:
   - Create a `.env` file in the `document_searcher` directory
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

## 🎮 Usage

### **GUI Application (Recommended)**
```bash
python modern_gui.py
```

### **Command Line Interface**
```bash
python main.py
```

### **Query Manager (Interactive CLI)**
```bash
python query_manager.py
```

### **Model Comparison**
```bash
python model_comparison.py
```

## 🤖 Available AI Models

| Model | Cost | Accuracy | Best For |
|-------|------|----------|----------|
| GPT-4o Mini | Low | Good | Simple questions |
| GPT-4o | Medium | Excellent | Most tasks |
| GPT-3.5 Turbo | Very Low | Medium | Technical content |
| GPT-4 | High | Outstanding | Complex reasoning |

## 📖 How It Works

1. **Load PDFs**: Select and load your PDF documents
2. **Process Documents**: Create vector embeddings for intelligent search
3. **Ask Questions**: Type questions and get accurate answers
4. **Choose Models**: Select the AI model that fits your needs

## 🔧 Technical Details

- **PDF Processing**: PyPDF2 for text extraction
- **Text Chunking**: Smart chunking with sentence boundary detection
- **Embeddings**: OpenAI's text-embedding-3-small model
- **Vector Search**: Cosine similarity with multiple chunk retrieval
- **GUI Framework**: CustomTkinter for modern interface

## 📝 Example Questions

- "How do I configure the device settings?"
- "What are the technical specifications?"
- "What troubleshooting steps are available?"

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- OpenAI for the powerful API
- CustomTkinter for the modern GUI framework
- PyPDF2 for PDF processing capabilities
