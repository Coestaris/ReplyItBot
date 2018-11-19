import json
import utils

class cfg:
    def __init__(self, admins = [], tg_token = ''):
        self.admins = admins
        self.tg_token = tg_token
        utils.LIST_OF_ADMINS = admins

    @staticmethod
    def parse_cfg():
        with open('../cfg.json') as f:
            data = json.load(f)
            return cfg(
                data["admins"], 
                data["tg_token"])


globalCfg = cfg()