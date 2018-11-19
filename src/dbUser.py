class dbUser:
    def __init__(self, teleid, lang = "ru", debugName = "-", triggers = [], userActions = {}):
        self.teleId = teleid
        self.lang = lang
        self.debugName = debugName
        self.triggers = triggers
        self.userActions = userActions

    def toDict(self):
        a =  {
            "teleId" : self.teleId,
            "lang" : self.lang,
            "debugName" : self.debugName,
            "triggers" : self.triggers,
            "userActions" : self.userActions
        }
        return a

    @staticmethod
    def parse(dict):
        user = dbUser(
            dict["teleId"],
            dict["lang"],
            dict["debugName"] if "debugName" in dict else "-",
            dict["triggers"],
            dict["userActions"]
        )
        return user