import sys
from config.config_manager import ConfigManager
from adapter.api_client import ApiClient
from state import AgentStateMachine
from lock import SingleInstanceLock


def main():
    cfg = ConfigManager().build()
    lock = SingleInstanceLock()
    lock.acquire()

    api = ApiClient(cfg.api_base_url, cfg.api_token)
    agent = AgentStateMachine(cfg, api)
    agent.run()

    lock.release()


if __name__ == "__main__":
    main()
