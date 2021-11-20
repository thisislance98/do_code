#from codeclient import CodeClient
#from do_code import CodeClient
from docode import CodeClient

cc = CodeClient()
a = cc.do("generate ten random characters and return result")
print('A', a)

raise SystemExit('\n-')

import pickledb

db = pickledb.load('example.db', False)

# db.set('asdf','fff')
print(db.get('asdf'))

db.dump()