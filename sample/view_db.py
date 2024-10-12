from data.fastlite_db import DB


for e in DB.t.event():
    print(e)
