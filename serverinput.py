
class InputServer:
    def __init__(self):
        self.server = ""
    
    def enter_server(self):
        if self.server != "":
            return self.server
        else:
            print("Server is blank")
    
    #removes character from player name
    def remove_character(self):
        self.server = self.server[:-1]
    
    #adds character to player name
    def add_character(self, event):
        self.server += event.unicode