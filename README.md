# Introduction
I created this project to further my understanding of CI/CD concepts as well as to deploy a machine learning model in an actual use case for the first time. The news project website takes as an argument the copied text from a news article, tokenizes the text, and uses cosine similarity to generate a list of the top 3 similar articles from the internal database. The database is created using the newspaper libarary and is stored locally within the instance in an SQLite3 database. The project is hosted on Vercel and the front-end has been built using JavaScript. The backend is hosted using AWS App Runner. The model in use is the all-MiniLM-L6-v2 from the sentence-transformers library.

# Project Structure
The backend folder contains the F


