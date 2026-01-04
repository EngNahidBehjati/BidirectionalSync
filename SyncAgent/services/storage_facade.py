from interface_ports.storage_port import StoragePort

class StorageFacade(StoragePort):

    def __init__(self, local_adapter, superior_adapter):
        self._local = local_adapter
        self._superior = superior_adapter

    def list_superior(self):
        return self._superior.list_superior()

    def stat_superior(self, file):
        return self._superior.stat_superior(file)

    def read_superior(self, file):
        return self._superior.read_superior(file)



    def list_agent(self):
        return self._local.list_agent()

    def stat_agent(self, file):
        return self._local.stat_agent(file)

    def write_agent(self, file, content):
        return self._local.write_agent(file, content)

    def delete_agent(self, file):
        return self._local.delete_agent(file)

    def backup_agent(self, file):
        return self._local.backup_agent(file)
