from langchain_openai import ChatOpenAI
from agents.prompts import GENERATOR_SYSTEM
from config import MOCK_MODE, OPENAI_MODEL
from pathlib import Path

def _mock_lesson(topic: str, feedback: list[str] | None = None, inject_error: bool = False) -> str:
    # Deliberately simple offline sample. The evaluator still runs against it.
    lesson_title = (
    topic if topic.lower().startswith("introduction to ")
    else f"Introduction to {topic}"
)
    false_claim = "RAG means the model retrains itself on every question.\n\n" if inject_error else ""
    return f'''# {lesson_title}

## 1. What is RAG?
RAG means Retrieval-Augmented Generation. It is a way for an AI application to
look up useful information before it writes an answer. The information may come
from documents that the application is allowed to search.

{false_claim}Think of RAG like an open-book test. Instead of answering only from
memory, you first find the relevant page in a book and then use that page to answer.

## 2. Why is RAG useful?
A language model may not know the latest details or the private information in
your documents. RAG can provide relevant information at question time. This can
make answers more useful and can help the application show where information came from.
RAG does not guarantee that every answer is correct.

## 3. How does RAG work?
1. Prepare: split documents into smaller pieces and convert each piece into a
   numerical representation called an embedding.
2. Store: save the pieces and their embeddings in a searchable index.
3. Retrieve: turn the user's question into an embedding and find pieces with
   similar meaning.
4. Generate: give the question and selected pieces to the language model.
5. Answer: the model writes a response using the supplied information.

An embedding is a list of numbers that represents meaning. Similar meanings
often have representations that are close to each other. A retrieval system
uses this to find relevant text.

## 4. A simple example
Imagine a college has a 40-page student handbook. A student asks, "When does
the library close on Saturday?" The RAG application searches the handbook,
finds the paragraph about Saturday library hours, and gives that paragraph
and the question to the language model. The model then explains the closing time.
The answer should be checked against the handbook; retrieval can find the wrong
paragraph or miss the right one.

## 5. What RAG does not do
- It does not automatically update or retrain the model's internal weights.
- It does not guarantee that retrieved information is correct or complete.
- It is not the same as fine-tuning. Fine-tuning changes model parameters using
  training examples; RAG supplies external information while answering.

## 6. Key words
- **Language model:** an AI system trained to understand and generate text.
- **Retrieval:** finding information relevant to a question.
- **Embedding:** a numerical representation of text meaning.
- **Vector index:** a data structure that helps search embeddings by similarity.
- **Context:** information supplied to the model for a particular answer.

## 7. Quick recap
RAG combines search with text generation. It finds relevant information first,
then gives that information to a language model to help it answer. Good document
quality, retrieval, and evaluation are still important.

## 8. Check your understanding
1. What are the two main activities combined in RAG?
   **Answer:** Retrieving information and generating an answer.
2. Does RAG retrain the model every time someone asks a question?
   **Answer:** No. It supplies relevant external information at answer time.
3. Why might a RAG answer still be wrong?
   **Answer:** It may retrieve irrelevant or incomplete information, or the model
   may misunderstand or misuse the supplied information.
'''

def generate_lesson(topic: str, feedback: list[str] | None = None, inject_error: bool = False) -> str:
    if MOCK_MODE:
        return _mock_lesson(topic, feedback, inject_error)
    llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0.3)
    user_prompt = f"Create a beginner lesson about: {topic}\n"
    if feedback:
        user_prompt += "\nThe previous draft failed these checks. Fix them explicitly:\n- " + "\n- ".join(feedback)
    if inject_error:
        user_prompt += "\nFor evaluator testing only, include one obviously false statement that RAG retrains the model on every question."
    return llm.invoke([("system", GENERATOR_SYSTEM), ("human", user_prompt)]).content
