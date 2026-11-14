
# Trusted Reference: Retrieval-Augmented Generation

## Definition
RAG stands for Retrieval-Augmented Generation.
It combines information retrieval with language generation.

## Purpose
RAG supplies relevant external information to a language model
when answering a user's question.

## Working process
1. Documents are collected.
2. Documents are split into smaller chunks.
3. Chunks are converted into embeddings.
4. Embeddings are stored in a searchable index.
5. A user submits a question.
6. Relevant chunks are retrieved.
7. The question and retrieved information are sent to a language model.
8. The model generates an answer.

## Important facts
- RAG does not automatically retrain model weights for every question.
- RAG does not guarantee that every generated answer is correct.
- Retrieval can return irrelevant or incomplete information.
- Embeddings are numerical representations of text.
- Fine-tuning and RAG are different techniques.
- Fine-tuning updates model parameters using training examples.
- RAG provides external information at answer time.

## Limitations
- Poor source documents can produce poor answers.
- Retrieval quality affects answer quality.
- The language model can misunderstand retrieved information.
- Human review may be needed for important applications.
