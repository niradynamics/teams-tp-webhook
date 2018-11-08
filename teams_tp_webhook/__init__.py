import os
from pyhocon import ConfigFactory
import logging

logger = logging.getLogger(__name__)

class Config(object):
    def __init__(self):
        self._config = ConfigFactory.parse_file(os.path.join(os.path.dirname(__file__), "reference.conf"))

    def add_override(self, extra_config_file: str):

        logger.debug(f"Considering extra_config_file {extra_config_file}")
        if extra_config_file is not None:
            logger.debug(f"Adding configuration from {extra_config_file}")
            extra = ConfigFactory.parse_file(extra_config_file)
            self._config = extra.with_fallback(self._config)
        return self._config

    def __getattr__(self, attr):
        return getattr(self._config, attr)

config = Config()