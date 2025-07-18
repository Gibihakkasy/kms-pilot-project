#!/usr/bin/env python3
"""
CLI tool for testing document summarization.
"""
import os
import argparse
import time
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from chains.summarization_refine_chain import summarize_documents

def main():
    parser = argparse.ArgumentParser(description='Summarize a PDF document')
    parser.add_argument('--file', type=str, required=True, help='Path to the PDF file to summarize')
    parser.add_argument('--model', type=str, default='gpt-4', help='OpenAI model to use (default: gpt-4)')
    parser.add_argument('--chunk-size', type=int, default=4000, help='Size of text chunks (default: 4000 chars)')
    parser.add_argument('--chunk-overlap', type=int, default=200, help='Overlap between chunks (default: 200 chars)')
    args = parser.parse_args()
    
    # Verify OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        return
    
    try:
        start_time = time.time()
        
        # Load the document
        print(f"\n📄 Loading document: {args.file}")
        loader = PyPDFLoader(args.file)
        raw_docs = loader.load()
        
        # Split text into chunks
        print(f"✂️  Splitting document into manageable chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap,
            length_function=len,
        )
        
        docs = text_splitter.split_documents(raw_docs)
        
        print(f"📊 Document Statistics:")
        print(f"   - Pages: {len(raw_docs)}")
        print(f"   - Text Chunks: {len(docs)}")
        print(f"   - Avg. Chunk Size: {sum(len(d.page_content) for d in docs) // len(docs) if docs else 0} characters")
        
        # Initialize the LLM
        print(f"\n🤖 Initializing {args.model} model...")
        llm = ChatOpenAI(
            model_name=args.model,
            temperature=0,
            request_timeout=120  # Increase timeout for longer documents
        )
        
        # Generate the summary
        print("\n🔍 Analyzing document and generating summary...")
        print("   This may take several minutes depending on document size.")
        print("   Progress will be shown below:\n" + "-"*50)
        
        summary = summarize_documents(llm, docs)
        
        # Print the summary
        print("\n" + "✅"*40)
        print("📝 DOCUMENT SUMMARY:")
        print("✅"*40)
        print(summary)
        
        elapsed = time.time() - start_time
        print(f"\n✨ Summary completed in {elapsed:.1f} seconds")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return

if __name__ == "__main__":
    main()
