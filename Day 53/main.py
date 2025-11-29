from data_manager import DataManager
from filler import Filler

dm = DataManager()
dm.update_info()
info = dm.get_info()
print(info)
filler=Filler()
for item in info:
    filler.send_record_to_sheet(item)








