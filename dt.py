import sqlite3

conn=sqlite3.connect("my_database.db")
cursor=conn.cursor()
cursor.execute("""
create table if not exists users (
               id int primary key,
               name text not null
               )
""")

# cursor.execute('insert into users (id,name) values (?,?)',(2,'aloce'))
# conn.commit()

cursor.execute("select * from users")
rows=cursor.fetchall()

cursor.execute("select COUNT(*) from users")
length=cursor.fetchone()

for row in rows:
    print(row)

print("length :",length)

conn.close()
