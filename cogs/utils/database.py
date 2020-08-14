import sqlite3

conn = sqlite3.connect('canyon.db')

conn.row_factory = sqlite3.Row

c = conn.cursor()

def get_from(table, guild_id, column):
    c.execute(f"SELECT * FROM {table} WHERE guild=:guild", {"guild": guild_id})
    return c.fetchone()[column]

def update_in(table, guild_id, column, argument=None):
    c.execute(f"SELECT * FROM {table} WHERE guild=:guild", {"guild": guild_id})

    with conn:
        if c.fetchone():
            c.execute(f"UPDATE {table} SET {column} = :argument WHERE guild=:guild", {"argument": argument, "guild": guild_id})
        else: 
            c.execute(f"INSERT INTO {table} VALUES (:guild, :prefix, :none)", {"guild": guild_id, "prefix": None, "none": None})
            c.execute(f"UPDATE {table} SET {column} = :argument", {"argument": argument})

def delete_row(table, guild_id):
    c.execute(f"DELETE FROM {table} WHERE guild=:guild", {"guild": guild_id})
