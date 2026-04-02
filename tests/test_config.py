"""Tests for configuration loader."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from src.config import Settings

# Shortened connection string for test readability
TEST_CONN_STR = (
    "DefaultEndpointsProtocol=https;"
    "AccountName=test;"
    "AccountKey=dGVzdA==;"
    "EndpointSuffix=core.windows.net"
)


@pytest.fixture
def env_vars():
    """Minimal environment variables for valid config."""
    return {
        "ICLOUD_USERNAME": "test@icloud.com",
        "AZURE_STORAGE_CONNECTION_STRING": TEST_CONN_STR,
        "AZURE_STORAGE_CONTAINER_NAME": "test-photos",
        "STAGING_DIR": "/tmp/mom-cloud-test/staging",
        "LOG_DIR": "/tmp/mom-cloud-test/logs",
    }


@pytest.fixture
def clean_env(env_vars):
    """Patch environment with test values, clearing .env file loading."""
    with patch.dict(os.environ, env_vars, clear=False):
        yield env_vars


class TestSettings:
    """Tests for Settings configuration."""

    def test_loads_from_environment(self, clean_env):
        """Settings should load from environment variables."""
        settings = Settings(
            _env_file=None,
            icloud__username=clean_env["ICLOUD_USERNAME"],
            azure__connection_string=clean_env["AZURE_STORAGE_CONNECTION_STRING"],
            azure__container_name=clean_env["AZURE_STORAGE_CONTAINER_NAME"],
            staging_dir=Path(clean_env["STAGING_DIR"]),
            log_dir=Path(clean_env["LOG_DIR"]),
        )
        assert settings.icloud.username == "test@icloud.com"
        assert settings.azure.container_name == "test-photos"

    def test_default_values(self, clean_env):
        """Settings should have sensible defaults."""
        settings = Settings(
            _env_file=None,
            icloud__username=clean_env["ICLOUD_USERNAME"],
            azure__connection_string=clean_env["AZURE_STORAGE_CONNECTION_STRING"],
        )
        assert settings.pipeline.log_level == "INFO"
        assert settings.pipeline.dry_run is False
        assert settings.dedup_enabled is True

    def test_ensure_dirs_creates_directories(self, clean_env, tmp_path):
        """ensure_dirs should create staging and log directories."""
        staging = tmp_path / "staging"
        logs = tmp_path / "logs"
        settings = Settings(
            _env_file=None,
            icloud__username=clean_env["ICLOUD_USERNAME"],
            azure__connection_string=clean_env["AZURE_STORAGE_CONNECTION_STRING"],
            staging_dir=staging,
            log_dir=logs,
        )
        settings.ensure_dirs()
        assert staging.exists()
        assert logs.exists()
