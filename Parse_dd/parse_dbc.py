import cantools
from can.interface import Bus

db=cantools.database.load_file( '/home/mobase/Parse_dd/CAN_CanNm.dbc')

bus=Bus(channel='can0',interface='socketcan')

for message in db.messages:
        print(message.name,message.frame_id)
