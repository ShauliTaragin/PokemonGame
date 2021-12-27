
class Agent:
    def __init__(self , id:int):
        self.id = id
        value = 0
        src = 0
        dest = 0
        speed = 0.0
        pos = 0 #this is position in geo location
    """
    if we want to change agent according to json file we read we can do that here.
    """
    def update_from_json(self, json_file:str):
        pass

    def onNOde(self)->bool:
        pass
