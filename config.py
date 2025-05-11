"""
Configuration file for the Multi-Agent Medical Chatbot

This file contains all the configuration parameters for the project.

If you want to change the LLM and Embedding model:

you can do it by changing all 'llm' and 'embedding_model' variables present in multiple classes below.

Each llm definition has unique temperature value relevant to the specific class. 
"""

import os
from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings

# Load environment variables from .env file
load_dotenv()

def get_llm(temperature=0.0):
    if os.getenv("OPENAI_API_BASE"):
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model_name=os.getenv("model_name"),
            openai_api_key=os.getenv("openai_api_key"),
            openai_api_base=os.getenv("OPENAI_API_BASE"),
            temperature=temperature,
            max_tokens=1000  # Limit token usage
        )
    else:
        from langchain_openai import AzureChatOpenAI
        return AzureChatOpenAI(
            deployment_name=os.getenv("deployment_name"),
            model_name=os.getenv("model_name"),
            azure_endpoint=os.getenv("azure_endpoint"),
            openai_api_key=os.getenv("openai_api_key"),
            openai_api_version=os.getenv("openai_api_version"),
            temperature=temperature,
            max_tokens=1000  # Limit token usage
        )

def get_embeddings():
    """Helper function to create embedding model instances based on provider config"""
    if os.getenv("OPENAI_API_BASE"):
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(
            model=os.getenv("embedding_model_name"),
            openai_api_key=os.getenv("openai_api_key"),
            openai_api_base=os.getenv("OPENAI_API_BASE")
        )
    else:
        from langchain_openai import AzureOpenAIEmbeddings
        return AzureOpenAIEmbeddings(
            deployment=os.getenv("embedding_deployment_name"),
            model=os.getenv("embedding_model_name"),
            azure_endpoint=os.getenv("azure_endpoint"),
            openai_api_key=os.getenv("openai_api_key"),
            openai_api_version=os.getenv("openai_api_version")
        )

class AgentDecisoinConfig:
    def __init__(self):
        self.llm = get_llm(temperature=0.1)  # Deterministic

class ConversationConfig:
    def __init__(self):
        self.llm = get_llm(temperature=0.7)  # Creative but factual

class WebSearchConfig:
    def __init__(self):
        self.llm = get_llm(temperature=0.3)  # Slightly creative but factual
        self.context_limit = 20     # include last 20 messsages (10 Q&A pairs) in history

class RAGConfig:
    def __init__(self):
        self.vector_db_type = "qdrant"
        self.embedding_dim = 1536  # Add the embedding dimension here
        self.distance_metric = "Cosine"  # Add this with a default value
        self.use_local = True  # Add this with a default value
        self.local_path = "./data/qdrant_db"  # Add this with a default value
        self.url = os.getenv("QDRANT_URL")
        self.api_key = os.getenv("QDRANT_API_KEY")
        self.collection_name = "medical_assistance_rag"  # Ensure a valid name
        self.chunk_size = 512  # Modify based on documents and performance
        self.chunk_overlap = 50  # Modify based on documents and performance
        self.processed_docs_dir = "./data/processed"  # Set a default value
        # self.embedding_model = "text-embedding-3-large"
        # Initialize Embeddings based on provider
        self.embedding_model = get_embeddings()
        self.llm = get_llm(temperature=0.3)  # Slightly creative for synthesizing responses
        self.document_sources = ["./data/documents"]
        self.top_k = 5  # Number of most similar chunks to return
        self.score_threshold = 0.7  # Similarity score threshold for relevance
        self.response_format_instructions = """Instructions:
        1. Answer the query based ONLY on the information provided in the context.
        2. If the context doesn't contain relevant information to answer the query, state: "I don't have enough information to answer this question based on the provided context."
        3. Do not use prior knowledge not contained in the context.
        5. Be concise and accurate.
        6. Provide a well-structured response based on retrieved knowledge."""  # ADD THIS LINE
        self.include_sources = True  # ADD THIS LINE
        self.metrics_save_path = "./logs/rag_metrics.json"  # ADD THIS LINE

        # ADJUST ACCORDING TO ASSISTANT'S BEHAVIOUR BASED ON THE DATA INGESTED:
        self.min_retrieval_confidence = 0.8  #the auto routing from RAG agent to WEB_SEARCH agent is dependent on this value

        self.context_limit = 20     # include last 20 messsages (10 Q&A pairs) in history

class MedicalCVConfig:
    def __init__(self):
        self.brain_tumor_model_path = "./agents/image_analysis_agent/brain_tumor_agent/models/brain_tumor_segmentation.pth"
        self.chest_xray_model_path = "./agents/image_analysis_agent/chest_xray_agent/models/covid_chest_xray_model.pth"
        self.skin_lesion_model_path = "./agents/image_analysis_agent/skin_lesion_agent/models/checkpointN25_.pth.tar"
        self.skin_lesion_segmentation_output_path = "./uploads/skin_lesion_output/segmentation_plot.png"
        self.llm = get_llm(temperature=0.1)  # Keep deterministic for classification tasks

class APIConfig:
    def __init__(self):
        self.host = "0.0.0.0"
        self.port = 8000
        self.debug = True
        self.rate_limit = 10
        self.max_image_upload_size = 5  # 1 MB max upload

class SpeechConfig:
    def __init__(self):
        # self.tts_voice_id = "EXAVITQu4vr4xnSDxMaL"
        # self.tts_stability = 0.5
        # self.tts_similarity_boost = 0.8
        # self.stt_model = "whisper-1"
        # self.stt_language = "en"
        self.eleven_labs_api_key = os.getenv("ELEVEN_LABS_API_KEY")  # Replace with your actual key
        self.eleven_labs_voice_id = "21m00Tcm4TlvDq8ikWAM"    # Default voice ID (Rachel)

class ValidationConfig:
    def __init__(self):
        self.require_validation = {
            "CONVERSATION_AGENT": False,
            "RAG_AGENT": False,
            "WEB_SEARCH_AGENT": False,
            "BRAIN_TUMOR_AGENT": True,
            "CHEST_XRAY_AGENT": True,
            "SKIN_LESION_AGENT": True
        }
        self.validation_timeout = 300
        self.default_action = "reject"

class UIConfig:
    def __init__(self):
        self.theme = "light"
        # self.max_chat_history = 50
        self.enable_speech = True
        self.enable_image_upload = True

class Config:
    def __init__(self):
        self.agent_decision = AgentDecisoinConfig()
        self.conversation = ConversationConfig()
        self.rag = RAGConfig()
        self.medical_cv = MedicalCVConfig()
        self.web_search = WebSearchConfig()
        self.api = APIConfig()
        self.speech = SpeechConfig()
        self.validation = ValidationConfig()
        self.ui = UIConfig()
        self.eleven_labs_api_key = os.getenv("ELEVEN_LABS_API_KEY")
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        self.max_conversation_history = 40  # storing 20 sets of QnA in history, history is truncated based on this value

# # Example usage
# config = Config()