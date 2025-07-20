from setuptools import setup, find_packages

setup(
    name="kms-pilot-project",
    version="0.1.0",
    packages=find_packages(include=["backend", "backend.*"]),
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn[standard]>=0.15.0",
        "python-multipart>=0.0.5",
        "pymupdf>=1.19.0",
        "faiss-cpu>=1.7.0",
        "openai>=0.27.0",
        "langdetect>=1.0.9",
        "tiktoken>=0.3.0",
        "langgraph>=0.0.0",
        "langchain>=0.0.0",
        "sentence-transformers>=2.2.2",
        "watchdog>=2.1.0",
    ],
    python_requires=">=3.8",
)
