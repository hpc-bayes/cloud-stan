from utils.config import Config


def test_config_defaults():
    config = Config()
    assert config.cloud_storage_path == "path/to/default/storage"
