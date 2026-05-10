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

1) **Data Scraping**: extracts Q&A data from a FAQ support page of a brand called 'Fitness Passport'
1) **Data Handling**: indexing the document using chromadb's build-in embedding algorithm
1) **Retrieval & Query Processing**: embed questions using sentence-transformers/all-MiniLM-L6-v2, and query chroma db



