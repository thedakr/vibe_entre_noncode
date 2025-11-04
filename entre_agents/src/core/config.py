"""
Configuration management for VEntre agents.
Loads settings from environment variables and .env files.
"""

import os
from pathlib import Path
from typing import Optional


class Config:
    """
    Central configuration for VEntre agent system.
    Loads from environment variables and .env file.
    """

    def __init__(self, env_file: str = None):
        """
        Initialize configuration.

        Args:
            env_file: Path to .env file (defaults to .env in project root)
        """
        # Load environment variables from .env file if it exists
        if env_file is None:
            env_file = self._find_env_file()

        if env_file and os.path.exists(env_file):
            self._load_env_file(env_file)

        # API Keys
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        # Database
        self.database_type = os.getenv("DATABASE_TYPE", "sqlite")
        self.database_path = os.getenv("DATABASE_PATH", "data/ventre.db")
        self.database_url = os.getenv("DATABASE_URL")  # For PostgreSQL

        # LLM Settings
        self.llm_provider = os.getenv("LLM_PROVIDER", "anthropic")
        self.llm_model = os.getenv("LLM_MODEL")  # None = use default
        self.llm_temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        self.llm_max_tokens = int(os.getenv("LLM_MAX_TOKENS", "4096"))

        # Agent Settings
        self.entrepreneur_id = os.getenv("ENTREPRENEUR_ID", "default_user")
        self.agent_mode = os.getenv("AGENT_MODE", "development")  # development or production

        # Logging
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_file = os.getenv("LOG_FILE", "logs/ventre.log")

    def _find_env_file(self) -> Optional[str]:
        """Find .env file in current or parent directories."""
        current_dir = Path.cwd()

        # Check current directory and up to 3 levels up
        for _ in range(4):
            env_path = current_dir / ".env"
            if env_path.exists():
                return str(env_path)
            current_dir = current_dir.parent

        return None

    def _load_env_file(self, env_file: str):
        """Load environment variables from .env file."""
        try:
            from dotenv import load_dotenv
            load_dotenv(env_file)
        except ImportError:
            # If python-dotenv not installed, parse manually
            self._parse_env_file(env_file)

    def _parse_env_file(self, env_file: str):
        """Simple .env file parser (fallback if python-dotenv not available)."""
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        os.environ[key] = value

    def get_database_connection_string(self) -> str:
        """Get appropriate database connection string based on type."""
        if self.database_type == "sqlite":
            # Ensure directory exists
            db_path = Path(self.database_path)
            db_path.parent.mkdir(parents=True, exist_ok=True)
            return str(db_path)
        elif self.database_type == "postgresql":
            if not self.database_url:
                raise ValueError("DATABASE_URL required for PostgreSQL")
            return self.database_url
        else:
            raise ValueError(f"Unsupported database type: {self.database_type}")

    def validate(self):
        """Validate that required configuration is present."""
        errors = []

        # Check for required API key based on provider
        if self.llm_provider == "anthropic" and not self.anthropic_api_key:
            errors.append("ANTHROPIC_API_KEY is required when using Anthropic")
        elif self.llm_provider == "openai" and not self.openai_api_key:
            errors.append("OPENAI_API_KEY is required when using OpenAI")

        # Check database configuration
        if self.database_type == "postgresql" and not self.database_url:
            errors.append("DATABASE_URL is required for PostgreSQL")

        if errors:
            raise ValueError("Configuration validation failed:\n" + "\n".join(f"  - {e}" for e in errors))

    def __repr__(self):
        """String representation (hides API keys)."""
        return (
            f"Config(\n"
            f"  llm_provider={self.llm_provider},\n"
            f"  database_type={self.database_type},\n"
            f"  entrepreneur_id={self.entrepreneur_id},\n"
            f"  agent_mode={self.agent_mode}\n"
            f")"
        )


# Global config instance (can be imported throughout the app)
config = Config()
