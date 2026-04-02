"""Configuration loader using pydantic-settings.

Loads settings from environment variables and .env file
with type validation and sensible defaults.
"""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ICloudSettings(BaseSettings):
    """iCloud connection settings."""

    model_config = SettingsConfigDict(env_prefix="ICLOUD_")

    username: str = Field(description="Apple ID email address")


class AzureSettings(BaseSettings):
    """Azure Blob Storage settings."""

    model_config = SettingsConfigDict(env_prefix="AZURE_STORAGE_")

    connection_string: str = Field(description="Azure Storage connection string")
    container_name: str = Field(default="mom-photos", description="Blob container name")


class PipelineSettings(BaseSettings):
    """Pipeline behavior settings."""

    model_config = SettingsConfigDict(env_prefix="PIPELINE_")

    log_level: str = Field(default="INFO", description="Logging level")
    dry_run: bool = Field(default=False, description="Run without making changes")


class Settings(BaseSettings):
    """Root settings — loads all config from .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Sub-configs
    icloud: ICloudSettings = Field(default_factory=lambda: ICloudSettings())
    azure: AzureSettings = Field(default_factory=lambda: AzureSettings())
    pipeline: PipelineSettings = Field(default_factory=lambda: PipelineSettings())

    # Local paths
    staging_dir: Path = Field(default=Path("./staging"), description="Local staging directory")
    log_dir: Path = Field(default=Path("./logs"), description="Log output directory")

    # Feature flags
    dedup_enabled: bool = Field(default=True, description="Enable deduplication")

    def ensure_dirs(self) -> None:
        """Create required directories if they don't exist."""
        self.staging_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)


def load_settings() -> Settings:
    """Load and validate settings from environment."""
    settings = Settings()
    settings.ensure_dirs()
    return settings


if __name__ == "__main__":
    # Quick validation: python src/config.py
    try:
        config = load_settings()
        print("Configuration loaded successfully!")
        print(f"  Staging dir: {config.staging_dir}")
        print(f"  Log dir:     {config.log_dir}")
        print(f"  Log level:   {config.pipeline.log_level}")
        print(f"  Dry run:     {config.pipeline.dry_run}")
        print(f"  Dedup:       {config.dedup_enabled}")
    except Exception as e:
        print(f"Configuration error: {e}")
        raise SystemExit(1) from e
