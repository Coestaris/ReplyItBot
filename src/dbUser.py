class dbUser:
    def __init__(self, teleid, lang = "ru", debugName = "-", triggers = [], 
            userActions = {}, enabled = True, ignoreCase = True, adminMode = False):
        self.teleId = teleid
        self.lang = lang
        self.debugName = debugName
        self.triggers = triggers
        self.userActions = userActions
        self.enabled = enabled
        self.ignoreCase = ignoreCase
        self.adminMode = adminMode

    def toDict(self):
        a =  {
            "teleId" : self.teleId,
            "lang" : self.lang,
            "debugName" : self.debugName,
            "triggers" : self.triggers,
            "userActions" : self.userActions,
            "enabled" : self.enabled,
            "ignoreCase" : self.ignoreCase,
            "adminMode" : self.adminMode
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
            dict["enabled"],
            dict["ignoreCase"],
            dict["adminMode"]
        )
        return user