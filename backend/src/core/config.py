from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SynapseOS"

    postgres_host: str
    postgres_port: int

    postgres_db: str
    postgres_user: str
    postgres_password: str

    jwt_secret_key: str
    jwt_algorithm: str

    access_token_expire_minutes: int
    refresh_token_expire_days: int

    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket_name: str
    minio_secure: bool

    groq_api_key: str
    groq_model: str = "llama-3.3-70b-versatile"

    # ---------- Knowledge ----------
    knowledge_collection: str = "enterprise_docs_v5"
    knowledge_chunk_size: int = 384
    knowledge_chunk_overlap: int = 64
    knowledge_top_k: int = 5
    rag_similarity_threshold: float = 0.70
    rag_candidate_k: int = 10
    rag_top_k: int = 5
    knowledge_default_search_limit: int = 20

    reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    # reranker_model: str = "BAAI/bge-reranker-base"
    # ---------- Embeddings ----------
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    embedding_dimension: int = 384
    # ---------- Generator ----------
    groq_model: str = "llama-3.3-70b-versatile"
    groq_judge_model: str ="llama-3.1-8b-instant"
    generator_temperature: float = 0.1
    generator_max_tokens: int = 700

    neo4j_uri: str
    neo4j_username: str
    neo4j_password: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.postgres_user}:"
            f"{self.postgres_password}@"
            f"{self.postgres_host}:"
            f"{self.postgres_port}/"
            f"{self.postgres_db}"
        )


settings = Settings()

print(settings.database_url)
