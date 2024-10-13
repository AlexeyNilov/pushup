from data.fastlite_db import DB, prepare_db, create_profile_table
from fastcore.utils import hl_md


prepare_db()

t = DB.t.event
print(hl_md(t.schema, "sql"))

for e in DB.t.event():
    print(e)
    break

t = DB.t.profile
t.drop()
create_profile_table()

t = DB.t.profile
print(hl_md(t.schema, "sql"))

for p in DB.t.profile():
    print(p)
    break
