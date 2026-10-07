# from pydantic import BaseModel
# from fastapi import FastAPI
# from src.agent import graph

# class QuestionRequest(BaseModel):
#     question: str


# class QuestionResponse(BaseModel):
#     answer: str

# app = FastAPI(
#     title="UAE Legislation Agent",
#     version="1.0.0",
# )


# @app.post("/ask", response_model=QuestionResponse)
# def ask_question(request: QuestionRequest):
#     result = graph.invoke(
#         {
#             "question": request.question,
#         }
#     )

#     return QuestionResponse(answer=result["answer"])


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.agent import graph

app = FastAPI(
    title="UAE Legislation Agent",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


class QuestionResponse(BaseModel):
    answer: str
    retrieved_chunks: list
    reranked_chunks: list


@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):

    result = graph.invoke({"question": request.question})

    return {
        "answer": result["answer"],
        "retrieved_chunks": [
            {
                "text": chunk.text,
                "metadata": chunk.metadata,
            }
            for chunk in result.get("retrieved_chunks", [])
        ],
        "reranked_chunks": [
            {
                "text": chunk.text,
                "metadata": chunk.metadata,
            }
            for chunk in result.get("reranked_chunks", [])
        ],
    }
