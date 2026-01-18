"""
    Retrieval using ElasticSearch
"""
from elasticsearch import Elasticsearch, helpers
import pandas as pd
from dotenv import load_dotenv
from typing import List, AnyStr, Optional
import os
from sentence_transformers import SentenceTransformer
from .datasources import MedDataset
from tqdm import tqdm

# loading the environmental variables
load_dotenv()


class Retrieval:
    def __init__(self, cfg):
        self.elastic_api_key = os.getenv("ELASTIC_API_KEY")
        self.endpoint = os.getenv('ELASTIC_ENDPOINT')
        self.use_esv = cfg.retrieval.use_elastic_search_vectorization
        self.embedding_dims = cfg.retrieval.embedding_dims
        self.index_name = cfg.retrieval.index_name
        self.similarity_metric = cfg.retrieval.similarity_metric
        self.k_neighbours = cfg.retrieval.num_knn

        # initializing client
        self._init_client()
        # loading the embedding model
        self.model = SentenceTransformer(cfg.retrieval.embed_model)

        # creating an index mapping
        self.index_mapping = {
            "properties": {
                "record":{"type": "text"},
                "metadata":{'type': "text"}
            }
        }
        self.index_mapping["properties"]["embedding"] = {
            "type": "dense_vector",
            "dims": self.embedding_dims,
            "index": "true",
            "similarity": "cosine"
        }
        
        # setting options in a client
        self.client.options(ignore_status=[400,404]).indices.create(
            index=self.index_name, mappings = self.index_mapping, settings={}
        )

        self.data_loader = MedDataset(
                                        path=cfg.external_data.data_path,
                                        batch_size = cfg.external_data.batch_size,
                                        shuffle= cfg.external_data.shuffle
                                    )

    def _init_client(self):
        # Initializing client
        self.client = Elasticsearch(self.endpoint, api_key = self.elastic_api_key)
        print(self.client.info())
        print("|> Success : Client Created !!!")

    def _is_index_exists(self)-> bool:
        is_exists = self.client.indices.exists(index=self.index_name)
        return is_exists
    
    def _get_embeddings(self, doc: str)-> list[float]:
        if not doc.strip():
            print("Error : Cannot create an embedding for Empty text")
            return []
        embedding = self.model.encode(doc)
        return embedding.tolist()
    
    def batch_to_bulk_action(self, batch):
        for record in batch.iterrows():
            action = {
                "_index": self.index_name,
                "_source": {
                    "record": record[1]["record"],
                    "metadata": record[1]["conditions"]
                }
            }
            action["_source"]["embedding"] = self._get_embeddings(record[1]["record"])
            yield action

    def indexing(self):
        if self.client.count(index=self.index_name)["count"]!=0:
            try:
                print("| CREATING indexing ..")
                for data_batch in tqdm(self.data_loader, total=len(self.data_loader)//self.data_loader.batch_size, desc="Creating indexing"):
                    actions = self.batch_to_bulk_action(data_batch)
                    helpers.bulk(self.client, actions)
                    
            except helpers.BulkIndexError as e:
                print(f"Error: Got an Error while indexing the dataset ,:: {e.errors}")
        else:
            print("INFO: Already Indexed Created")
    

    def delete_index(self):
        if self.client.indices.exists(index=self.index_name):
            print("Deleting existing %s" % self.index_name)
            self.client.indices.delete(index=self.index_name, ignore=[400, 404])


    def querying(self, query):
        question_embedding = self._get_embeddings(query)
        knn = {
            'field' : 'embedding',
            'query_vector': question_embedding,
            'k': self.k_neighbours,
            'num_candidates': 150
        }
        response = self.client.search(index=self.index_name, knn=knn, size=5)
        results = []
        for hit in response['hits']['hits']:
            id = hit['_id']
            score = hit["_score"]
            metadata = hit["_source"]["metadata"]
            record = hit["_source"]["record"]
            result = {
                'id': id,
                '_score': score,
                'condition': metadata,
                'record': record
            }
            results.append(result)
        return results


    def create_new_entry(self, document, metadata):
        try:
            self.client.index(
                index=self.index_name,
                document={
                    "record":document,
                    "metadata":metadata,
                    "embedding":self._get_embeddings(document)

                }
            )
            print("|> Created new extry index ")
        except:
            print("|> unable to update index")

       

    
    

# sanity checking
if __name__ == "__main__":
    import yaml
    from munch import Munch
    with open('config/main.yaml', 'r') as f:
        config = yaml.safe_load(f)
        config = Munch.fromDict(config)
    retrieval = Retrieval(config)
    # creating indexing
    # retrieval.indexing()
    retrieval.create_new_entry("this is something", metadata="no disease")
    # results  = retrieval.querying("tell me about neuro disease , what patient suffered")
    # print(results)
