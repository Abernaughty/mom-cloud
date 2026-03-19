"""
mom-cloud configuration loader.
Reads from .env file and environment variables.
"""

import os
from pathlib import Path
from dataclasses import dataclass


@dataclass
class ICloudConfig:
    username: str
    password: str


@dataclass
class AzureConfig:
    storage_account_name: str
    storage_account_key: str
    container_name: str


@dataclass
class PipelineConfig:
    staging_dir: Path
    organize_format: str
    dedup_strategy: str
    log_level: str


@dataclass
class AppConfig:
    icloud: ICloudConfig
    azure: AzureConfig
    pipeline: PipelineConfig


def load_config() -> AppConfig:
    """Load configuration from environment variables."""
    return AppConfig(
        icloud=ICloudConfig(
            username=os.environ["ICLOUD_USERNAME"],
            password=os.environ["ICLOUD_PASSWORD"],
        ),
        azure=AzureConfig(
            storage_account_name=os.environ["AZURE_STORAGE_ACCOUNT_NAME"],
            storage_account_key=os.environ["AZURE_STORAGE_ACCOUNT_KEY"],
            container_name=os.getenv("AZURE_STORAGE_CONTAINER", "photos"),
        ),
        pipeline=PipelineConfig(
            staging_dir=Path(os.getenv("LOCAL_STAGING_DIR", "/data/staging")),
            organize_format=os.getenv("PHOTO_ORGANIZE_FORMAT", "%Y/%m"),
            dedup_strategy=os.getenv("DEDUP_STRATEGY", "hash"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        ),
    )
