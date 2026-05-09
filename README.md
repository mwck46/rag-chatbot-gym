# Retrieval-Augmented Generation (RAG) in FAQ Chatbot

##### Inspired by https://github.com/wandabwa2004/LLMs/tree/main

## Requirements
python 3.12
beautifulsoup4
streamlit
chromadb
sentence-transformers
openai



## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [Scraping FAQs](#scraping-faqs)
  - [Running the Chatbot](#running-the-chatbot)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Overview

1) **Data Scraping**: extracts Q&A data from a FAQ support page of a brand called 'Fitness Passport', using Python's `requests` and `BeautifulSoup`
1) **Data Handling**: cleans, chunks, and embeds the scraped data using Sentence Transformers
1) **Retrieval & Query Processing**: Stores embeddings in vector DB - ChromaDB and retrieves context for user queries
1) **Response Generation**: Constructs a contextual prompt for LLM (e.g. OpenAI’s GPT) and context-aware responses via a Streamlit interface
1) **Chatbot Interface**: Provides a user-friendly interface using Streamlit.

## Running the Chatbot
```streamlit run app.py```

