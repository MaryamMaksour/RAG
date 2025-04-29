# Mini RAG APP

This is a minimal implementaion of the RAG model for question answering

## What we will do:

<li> <b>Upload</b> a document. </li>
<li> <b> Process </b> the document. ==> (extracting the text -> <b>Chunking</b> the text) </li>
<li> <b>Embedding</b> chunk Using LLM </li>
<li> Store ( chunk,embed) in <b>vector based DB</b></li>
<li> <b>Search</b> for similar in document</li>
<li> <b>Answer</b> from the document</li>

## Requirments
- python 3.8 or later

## Installation

### Install the required packages

```bash
$ pip install r- requirements.txt
```

### Setup the environment variables
```bash
$ cp .env.example .env
```

set your environment variables in the `.env` file. Like `OPENAI_API_KEY` value.

## Run the FatsAPI server

```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 8000
```