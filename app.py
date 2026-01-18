# Fast API server for the RAG based retrieval system.
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import yaml
import uvicorn
from munch import Munch
from src.retrieval_es import Retrieval
from src.agent import MedAgent


# Initialize the Fast API app
app = FastAPI()

try:
    # Load the configuration
    with open('config/main.yaml', 'r') as f:
        config = yaml.safe_load(f)
        config = Munch.fromDict(config)

    # intializing agent 
    retrieval = Retrieval(config)
    agent = MedAgent(config, retrieval)
except Exception as e:
    raise RuntimeError("Error : Application Startup Failed") from e


# Request modes
class DocumentRequest(BaseModel):
    document: str = Field()
    metadata: str = Field()

class SearchRequest(BaseModel):
    query: str = Field()

class QARequest(BaseModel):
    question: str = Field()


# creating endpoints for the app
@app.post("/documents")
async def create_document(req: DocumentRequest):
    """
        Create new document in the Vector Store.
    """
    try:
        status = retrieval.create_new_entry(document=req.document, metadata=req.metadata)
        if status:
            return {"status": "sucess", "message": "sucussfully created an index for document"}
        else:
            return {"status": "failed", "message": "Failed to create an index"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    


@app.post("/search")
async def search_documents(req: SearchRequest):
    """
        Searching the document using Elastic Search.
    """
    try:
        docs = retrieval.querying(req.query)
        if not docs:
            return {"status":"failed",'results': [], "message": "No documents found"}
        return {"status": "success", "results": docs}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    


@app.post("/qa")
async def retrieve_documents(req: QARequest):
    """
        Combining both retrieval and generation steps.
    """
    try:
        response =  agent.med_graph.invoke({
                    "question": "Did Mohs micrographic surgery fixed-tissue technique for melanoma of the nose?"
                    })
        if not response or "answer" not in response:
            return {
                "status": "failed",
                "message": "No relevant information found"
            }
        return {
            "status": "success",
            "message": response['answer']
        }
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed process your query"
        }

# running the app
if __name__ == "__main__":
    uvicorn.run(app, 
                host=config.app_config.host, 
                port=config.app_config.port, 
                debug=config.app_config.debug, 
                reload=config.app_config.reload, 
                workers=config.app_config.workers
            )