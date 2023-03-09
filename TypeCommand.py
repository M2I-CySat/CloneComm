#Creates a new Command class which includes system ID
#Mostly for simulating how a CySat packet will be created (likely to be removed later)
class TypeCommand:
    def __init__(self, sys_id, cmd_id):
        self.sys_id = sys_id
        self.cmd_id = cmd_id

def create_TypeCommand(sys_id, cmd_id):
    sending_cmd = TypeCommand(sys_id, cmd_id)
    return sending_cmd