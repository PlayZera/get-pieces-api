from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

class Settings(BaseSettings):

    SECRET_KEY: str = Field(
        default="keyP@ss",
        env="SECRET_KEY",
        description="Chave secreta para identificar applicação"
    )

    ALGORITHM: str = Field(
        default="HS256",
        env="ALGORITHM",
        description="Algoritmo para desincritografar informações em código"
    )

    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=240,
        env="ACCESS_TOKEN_EXPIRE_MINUTES",
        description="Tempo em segundos para expirar sessão"
    )

    OLLAMA_API_URL: str = Field(
        default="http://localhost:11434/api/generate",
        env="OLLAMA_API_URL",
        description="Url API Ollama"
    )

    MODEL_NAME: str = Field(
        default="mistral",
        env="MODEL_NAME",
        description="Modelo de lingaugem que será utilizado"
    )

    EXCEL_FILE: Path = Field(
        default=Path(__file__).parent.parent.parent / "data" / "pieces_db.xlsx",
        env="EXCEL_FILE",
        description="Diretorio arquivo excel"
    )

    JSON_DB_PATH: Path = Field(
        default=Path(__file__).parent.parent.parent / "data" / "pieces_db.json",
        env="JSON_DB_PATH",
        description="Diretório para aqruivo JSON"
    )

    IMAGES_PATH: Path = Field(
        default=Path(__file__).parent.parent.parent / "product_images",
        env="IMAGES_PATH",
        description="Diretório para imagens"
    )

    USE_JSON_STORAGE: bool = Field(
        default=False,
        env="USE_JSON_STORAGE",
        description="Utilizar banco de dados JSON"
    )

    MONGODB_URI: str = Field(
        default="mongodb://localhost:27017",
        env="MONGODB_URI",
        description="URI de conexão com o MongoDB"
    )
    MONGODB_NAME: str = Field(
        default="product_db",
        env="MONGODB_NAME",
        description="Nome do banco de dados MongoDB"
    )

    GOOGLE_PSE_KEY: str = Field(
        default="",
        env="GOOGLE_PSE_KEY",
        description="Chave para busca personalizada no google"
    )

    GOOGLE_PSE_ID: str = Field(
        default="",
        env="GOOGLE_PSE_ID",
        description="Id para busca personalizada no google"
    )

    USE_GEMINI: bool = Field(
        default=False,
        env="USE_GEMINI",
        description="Utilizar Gemini para busca de informações"
    )

    GEMINI_API_KEY: str = Field(
        default="",
        env="GEMINI_API_KEY",
        description="Chave para utilizar Gemini",
    )
    
    MONGODB_USERNAME: str = Field(
        default="",
        env="MONGODB_USERNAME",
        description="Usuário para autenticação no MongoDB",
    )
    
    MONGODB_PASSWORD: str = Field(
        default="",
        env="MONGODB_PASSWORD",
        description="Senha para autenticação no MongoDB",
    )
    
    PRODUCTION: bool = Field(
        default=False,
        env="PRODUCTION",
        description="Produção",
    )
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
    
    

settings = Settings()