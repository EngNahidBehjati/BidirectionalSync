from SyncAgent.config.manager import ConfigManager
from config.manager import ConfigManager
from config.schema import AgentConfig
from services.ftp_storage_adapter import FTPStorageAdapter
from services.api_remote_adapter import HTTPServerAdaptor
from engine.engine import SyncEngine

class Agent:
    def __init__(self, config: AgentConfig):
        self.config = config
        self.storage = FTPStorageAdapter(config)
        self.remote = HTTPServerAdaptor(config)
        self.engine = SyncEngine(config, self.storage, self.remote)

    def run(self):
        self.engine.run()

if __name__ == "__main__":
    cfg = ConfigManager(
        local_paths=["config/defaults.yaml",
                     "config/base.yaml",
                     "config/production.yaml"]
    ).build()
