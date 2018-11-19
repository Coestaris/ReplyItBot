class dbUser:
    def __init__(self, teleid, lang = "ru", debugName = "-", triggers = [], userActions = {}, enabled = True):
        self.teleId = teleid
        self.lang = lang
        self.debugName = debugName
        self.triggers = triggers
        self.userActions = userActions
        self.enabled = enabled

    def toDict(self):
        a =  {
            "teleId" : self.teleId,
            "lang" : self.lang,
            "debugName" : self.debugName,
            "triggers" : self.triggers,
            "userActions" : self.userActions,
            "enabled" : self.enabled
        }
        return a

    @staticmethod
    def parse(dict):
        user = dbUser(
            dict["teleId"],
            dict["lang"],
            dict["debugName"] if "debugName" in dict else "-",
            dict["triggers"],
            dict["userActions"],
            dict["enabled"]
        )
        return user