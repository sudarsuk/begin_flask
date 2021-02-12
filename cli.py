#!/usr/local/bin/python
import json
import sys
import glob

import models as db

if len(sys.argv) <= 1 or sys.argv[1] != "reset":
    print("Usage: ./cli.py reset")
    exit(0)

assert sys.argv[1] == "reset"

cur = db.postgres_db.cursor()
cur.execute("SELECT TABLENAME FROM pg_tables where schemaname='public'")

# delete tables
for t in cur.fetchall():
    cur.execute('DROP TABLE "%s"' % t)
    db.postgres_db.commit()

# import sql file and create tables
for path in glob.glob("test_data_sql/*.sql"):
    print("[+] Table create: %s" % path.split("/", 1)[1].rsplit(".", 1)[0])
    with open(path, "r") as f:
        cur.execute(f.read())
    db.postgres_db.commit()
print("Done")

cur.execute(""" SELECT setval('order-tagtaa-mn--product_id_seq', max(id)) FROM public."order-tagtaa-mn--product" """)
cur.execute(""" SELECT setval('order-tagtaa-mn--order_id_seq', max(id)) FROM public."order-tagtaa-mn--order" """)
cur.execute(""" SELECT setval('order-tagtaa-mn--data_id_seq', max(id)) FROM public."order-tagtaa-mn--data" """)
cur.execute(""" SELECT setval('mostmn-com--product_id_seq', max(id)) FROM public."mostmn-com--product" """)
cur.execute(""" SELECT setval('mostmn-com--order_id_seq', max(id)) FROM public."mostmn-com--order" """)
cur.execute(""" SELECT setval('mostmn-com--data_id_seq', max(id)) FROM public."mostmn-com--data" """)
