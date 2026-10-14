import config


def test_config_exists():

    assert config.COLLECTION_NAME
    assert config.EMBEDDING_MODEL
    assert config.LLM_MODEL
