CREATE TABLE [event] (
   [id] INTEGER PRIMARY KEY,
   [time] TEXT,
   [user_id] INTEGER,
   [value] INTEGER
)

CREATE TABLE [profile] (
   [user_id] INTEGER PRIMARY KEY,
   [max_set] INTEGER,
   [sum_per_day] INTEGER,
   [goal_set] INTEGER,
   [goal_per_day] INTEGER,
   [training_mode] TEXT,
   [training_day] INTEGER,
   [age] INTEGER
)
