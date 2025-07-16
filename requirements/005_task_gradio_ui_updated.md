
# Task 005 – Gradio User Interface

## 1. Summary

This task adds a simple web-based interface using Gradio to interact with the KMS system. Users will be able to upload OJK regulatory documents (PDFs), ask questions in natural language (English or Indonesian), and receive answers with cited source references. The UI connects all the core components from previous tasks into a complete user-facing experience.

## 2. Project Setup

### Files to be Created
- `app.py`: main entry point that launches the Gradio interface.

### Dependencies
To be added in `requirements.txt` if not yet present:
```
gradio
```

## 3. Implementation

1. In `app.py`, import the pipeline from Tasks 001–004:
   - Load PDF documents and chunk them
   - Generate embeddings and store in FAISS (or reuse existing index)
   - Accept user query and retrieve relevant chunks
   - Use GPT-4 to generate answers from retrieved content
2. Build the following Gradio components:
   - File uploader for `.pdf`
   - Textbox for user query input
   - Output textbox for generated answer
3. Display citation for each answer, showing source file name and page number
4. Ensure interface supports both English and Indonesian queries

## 4. Integration

This task connects:
- Task 001 (document ingestion)
- Task 002 (embedding)
- Task 003 (retriever)
- Task 004 (LLM-based QA)

This is the final integration layer for user interaction and demonstration.

## 5. Testing

### Test Plan

- Upload OJK documents such as:
  - Panduan Resiliensi Digital (2024)
  - Tata Kelola Kecerdasan Artifisial Perbankan Indonesia
  - Panduan Kode Etik Kecerdasan Buatan AI oleh OJK
- Ask questions such as:
  - "Apa saja prinsip dasar AI yang bertanggung jawab menurut OJK?"
  - "Langkah-langkah ketahanan terhadap gangguan digital?"
  - "Apa pendekatan etis yang disarankan OJK untuk AI di fintech?"
- Check that the answer:
  - Is relevant and coherent
  - Includes the correct file name and page number
  - Appears correctly in both Indonesian and English
- Test for robustness:
  - Upload no files or invalid PDFs
  - Input empty or unclear questions
  - Check UI responsiveness and error handling
