# Introduction to RAG (Retrieval-Augmented Generation)

*A beginner-friendly lesson for someone starting from zero*

## 1. What is RAG?

RAG stands for **Retrieval-Augmented Generation**. It is a way to help an AI application answer a question by finding useful information first and then using that information to write an answer.

Think of an open-book test. You do not have to remember every fact. You find the right page in your book, read it, and then answer the question. RAG works in a similar way.

RAG combines two activities:

- **Retrieval:** finding information that is useful for the question.
- **Generation:** writing a new answer using the question and the information found.

## 2. Why do we need RAG?

An AI language model learns patterns from data used during its training. But it may not know a company's latest rules, a college's private handbook, or a document that was created yesterday.

RAG can let an application search approved documents at the time a question is asked. This is useful when answers need information from:

- Company policies and handbooks
- Product manuals
- College notes and course material
- Frequently asked questions
- Other collections of documents

RAG can make an answer more relevant to those documents. It does **not** guarantee that the answer is correct. The search may find the wrong text, or the model may misunderstand the text.

## 3. How does RAG work?

A simple RAG system usually follows these steps.

### Step 1: Prepare the documents

The application receives documents, such as PDF files or text files. It divides long documents into smaller pieces. These pieces are often called **chunks**.

Why split a document? A very long document may contain many different subjects. Smaller pieces can make it easier to find the part related to a question.

### Step 2: Create embeddings

An **embedding** is a list of numbers that represents information about the meaning of a piece of text. A computer can compare these number lists to find text with similar meaning.

For example, the question "When does the library shut?" may be close in meaning to a document sentence saying "The library closes at 6 p.m."

### Step 3: Store the information for search

The chunks and their embeddings are saved in a searchable store. A **vector database** or vector index is one type of system used for this. It helps find chunks whose embeddings are similar to the question's embedding.

### Step 4: Retrieve useful chunks

When a learner asks a question, the application creates an embedding for the question. It searches the store and selects the chunks that seem most relevant.

This search step is called **retrieval**.

### Step 5: Generate the answer

The application sends the question and the selected text to a **language model**. A language model is an AI system that can understand and generate text.

The model uses the supplied text as context and writes an answer. In this situation, **context** means the information provided to the model for the current task.

### Step 6: Check the answer

The application or a human should check whether the answer matches the source. A RAG system can still make mistakes, so checking matters.

## 4. A simple example: College library timings

Imagine a college has a student handbook. It contains this sentence:

> On Saturdays, the college library closes at 2:00 p.m.

A student asks:

**"What time does the library close on Saturday?"**

Here is what the RAG application does:

1. It turns the student's question into a form that can be used for search.
2. It searches the handbook information.
3. It finds the sentence about Saturday closing time.
4. It gives that sentence and the student's question to the language model.
5. The model answers: "The library closes at 2:00 p.m. on Saturday."

The answer is useful because it is based on the handbook sentence that was found. The application should still show or check the source so the student can verify it.

## 5. What RAG does not do

- **RAG does not retrain the model for every question.** It retrieves outside information and supplies it while the answer is being created.
- **RAG does not guarantee truth.** Search can return irrelevant or incomplete text.
- **RAG is not the same as fine-tuning.** Fine-tuning changes a model by training it further on examples. RAG supplies external information at question time.
- **RAG does not fix poor documents.** If the source information is wrong or old, the answer may also be wrong.

## 6. Important words to remember

| Word | Simple meaning |
|---|---|
| RAG | A method that searches for information and then uses AI to write an answer |
| Retrieval | Finding useful information |
| Generation | Creating a new answer or text |
| Chunk | A smaller piece of a long document |
| Embedding | A list of numbers representing text meaning |
| Vector database | A store that helps search for similar embeddings |
| Language model | An AI system that can understand and generate text |
| Context | Information given to the model for the current answer |

## 7. Quick recap

RAG helps an AI application answer questions using information from selected documents.

Remember these three ideas:

1. **What:** RAG combines information search with AI text generation.
2. **Why:** It can provide useful information that may not be inside the model's training data.
3. **How:** It prepares documents, finds relevant pieces, and gives them to a language model to help create an answer.

## 8. Check your understanding

**Question 1: What are the two main activities in RAG?**

Answer: Retrieval (finding information) and generation (writing an answer).

**Question 2: Does RAG retrain the model whenever a user asks a question?**

Answer: No. It retrieves external information and supplies it to the model while it creates the answer.

**Question 3: Why can a RAG answer still be incorrect?**

Answer: The system may find the wrong information, miss useful information, or the language model may misunderstand what it receives.
