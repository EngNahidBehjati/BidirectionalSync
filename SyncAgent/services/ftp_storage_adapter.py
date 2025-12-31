from config.schema import AgentConfig
from interface_ports.storage_port_interface import IStoragePort

class FTPStorageAdapter(IStoragePort):
    def __init__(self, config: AgentConfig):
        self._config = config
        self._host = config.ftp_host
        self._user = config.ftp_user
        self._password = config.ftp_pass
        self._local = config.local_path
        self._remote = config.remote_path
        self._session = None
