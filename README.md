# Retrieval-Augmented Generation (RAG) in FAQ Chatbot

##### Inspired by https://github.com/wandabwa2004/LLMs/tree/main

## Requirements
python 3.12
beautifulsoup4
chromadb
sentence-transformers
openai



## Table of Contents
- [Overview](#overview)

## Overview

1) **Data Scraping**: extracts Q&A data from a FAQ support page of a brand called 'Fitness Passport', using Python's `requests` and `BeautifulSoup`
1) **Data Handling**: cleans, chunks, and embeds the scraped data using Sentence Transformers
1) **Retrieval & Query Processing**: Stores embeddings in vector DB - ChromaDB and retrieves context for user queries



