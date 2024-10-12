from data.fastlite_db import DB, prepare_db


prepare_db()
for e in DB.t.event():
    print(e)
