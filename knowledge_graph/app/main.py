"""Main App"""

from langchain.chains import GraphCypherQAChain
from langchain.prompts import PromptTemplate

from memgraph import MemgraphGraph

graph = MemgraphGraph(url="bolt://localhost:9896", username="neo4j", password="neo4jneo4j")

CYPHER_GENERATION_TEMPLATE = """Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Schema:
{schema}
Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement in your response.

The question is:
{question}
"""

CYPHER_GENERATION_PROMPT = PromptTemplate(input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE)

CYPHER_QA_TEMPLATE = """You are an assistant that helps to form nice and human understandable answers.
The information part contains the provided information that you must use to construct an answer.
The provided information is authoritative, you must never doubt it or try to use your internal knowledge to correct it.
Make the answer sound as a response to the question.
Do not mention that you based the results on the given information.
If the provided information is empty, say that you don't know the answer.

Information:
{context}

Question:
{question} 
"""

CYPHER_QA_PROMPT = PromptTemplate(input_variables=["context", "question"], template=CYPHER_QA_TEMPLATE)

if __name__ == "__main__":
    chain = GraphCypherQAChain.from_llm(
        graph=graph,
        verbose=True,
        cypher_prompt=CYPHER_GENERATION_PROMPT,
        qa_prompt=CYPHER_QA_PROMPT,
        top_k=50,
    )

    query = "How many tables do we have?"
    # print(chain.invoke({"query": query}))
