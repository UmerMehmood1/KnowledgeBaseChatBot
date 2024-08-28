import uvicorn

from fastapi import FastAPI
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain.indexes import VectorstoreIndexCreator
import csv
from langchain_core.documents import Document
import traceback
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware to handle CORS requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this as needed, e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

class EmbeddingModel:
    def __init__(self, model_name: str):
        self.model = HuggingFaceEmbeddings(model_name=model_name)
class DocumentLoader:
    def __init__(self, file_path, encoding='utf-8'):
        self.file_path = file_path
        self.encoding = encoding

    def load(self):
        documents = []
        try:
            with open(self.file_path, mode='r', encoding=self.encoding) as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    document = Document(page_content=' '.join(row))
                    documents.append(document)
        except UnicodeDecodeError as e:
            raise RuntimeError(f"Error loading {self.file_path} with encoding {self.encoding}. Exception: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error loading {self.file_path}. Exception: {str(e)}")
        return documents
class Indexer:
    def __init__(self, embedding_model: EmbeddingModel, loader: DocumentLoader):
        documents = loader.load()
        self.index = VectorstoreIndexCreator(
            vectorstore_cls=DocArrayInMemorySearch,
            embedding=embedding_model.model
        ).from_documents(documents)

    def search(self, query: str):
        return self.index.vectorstore.similarity_search(query)
class LanguageModel:
    def __init__(self, model_name: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.pipeline = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)

    def generate_summary(self, documents: str, max_input_length: int):
        if len(documents) > max_input_length:
            documents = documents[:max_input_length]

        summary_prompt = f"You are an assistant, as an assistant explain about this product to customer in 150 words: {documents}"
        summary = self.pipeline(summary_prompt, max_new_tokens=250, num_return_sequences=1)
        return summary[0]['generated_text']
class QueryProcessor:
    def __init__(self, indexer: Indexer, language_model: LanguageModel):
        self.indexer = indexer
        self.language_model = language_model

    def remove_repetitions(self, text):
        # Split the text into lines or sentences (based on your needs)
        text =text.replace("You are an assistant, as an assistant explain about this product to customer in 150 words: ","")
        lines = text.split('\n')
        
        # Use a set to keep track of unique lines
        seen = set()
        unique_lines = []

        for line in lines:
            # Strip whitespace and check if the line is already seen
            stripped_line = line.strip()
            if stripped_line and stripped_line not in seen:
                seen.add(stripped_line)
                unique_lines.append(stripped_line)
        
        # Join the unique lines back into a single string
        return '\n'.join(unique_lines)

    def process_query(self, query: str):
        results = self.indexer.search(query)
        if not results:
            return "No results found."
        
        # Extract the 'page_content' attribute from each Document object
        documents = "\n".join([doc.page_content for doc in results])
        
        # Generate the summary from the collected document content
        max_input_length = self.language_model.tokenizer.model_max_length - 50
        summary = self.language_model.generate_summary(documents, max_input_length)
        
        # Remove repetitions from the summary before returning
        return self.remove_repetitions(summary)


embedding_model = EmbeddingModel(model_name="sentence-transformers/all-MiniLM-L6-v2")
document_loader = DocumentLoader(file_path='OutdoorClothingCatalog_1000.csv')
indexer = Indexer(embedding_model, document_loader)
language_model = LanguageModel(model_name="distilgpt2")
query_processor = QueryProcessor(indexer, language_model)
@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/query/{query}")
async def read_item(query: str):
    # Initialize components
    try:
        response = query_processor.process_query(query)
        print(response)
        return {"response":response}
    except Exception as e:
        print(traceback.format_exc())
        return {"error":e}


if __name__ == '__main__':
	uvicorn.run(app, port=8080, host="127.0.0.2")