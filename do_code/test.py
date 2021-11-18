import pickledb

db = pickledb.load('example.db', False)

# db.set('asdf','fff')
print(db.get('asdf'))

db.dump()