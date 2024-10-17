import os
import faiss
import pickle
import yaml
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from IPython.display import display, Markdown
from dotenv import load_dotenv
import google.generativeai as genai
import getpass
# from langchain import SerpAPIWrapper - to search from google
# need SerpAPIWrapperkey
# Load environment variables
load_dotenv()

# Read config.yml file
if(os.path.isfile("config.yml")):
    print("Reading config.yml file...")
else:
    print("FILE-NOT-FOUND: Reading config.yml file failed !!")
    exit()
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

config


# FAISS index directory and files from config
index_dir = config["faiss_index"]["index_dir"]
index_file = config["faiss_index"]["index_file"]
pickle_file = config["faiss_index"]["pickle_file"]
# Load the FAISS index
index = faiss.read_index(f"{index_dir}/{index_file}")

# Load the docstore and index_to_docstore_id map
with open(f"{index_dir}/{pickle_file}", "rb") as f:
    docstore = pickle.load(f)
# Configure the Google Generative AI API
genai_api_key = os.getenv(config["google_generative_ai"]["api_key_env_var"])
genai.configure(api_key=genai_api_key)

# Set up Google Generative AI model
model_name = config["google_generative_ai"]["model_name"]
temperature = config["google_generative_ai"]["temperature"]
model = ChatGoogleGenerativeAI(model=model_name, temperature=temperature, convert_system_message_to_human=True)
# Initialize FAISS vectorstore for retrieval
embedding_model = config["google_generative_ai"]["embedding_model"]
embeddings = GoogleGenerativeAIEmbeddings(model=embedding_model)
faiss_index = FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=config["retrieval"]["allow_dangerous_deserialization"])

# Load templates from the config file
system_template = config["templates"]["system_template"]
condense_question_template = config["templates"]["condense_question_template"]
user_template = config["templates"]["user_template"]

# Define a template for the QA chain using the user template from the config
QA_CHAIN_PROMPT = PromptTemplate.from_template(user_template)

# Set up the QA chain with FAISS retriever
qa_chain = RetrievalQA.from_chain_type(
    model,
    retriever=faiss_index.as_retriever(search_kwargs=config["retrieval"]["search_kwargs"]),
    return_source_documents=True,
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)
# You can use `system_template` and `condense_question_template` in the future
# where you need these templates.
# `condense_question_template` for history


# Function to ask a question and get the result
def ask_question(question):
    result = qa_chain({"query": question})
    return result["result"]
