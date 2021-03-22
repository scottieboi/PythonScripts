import sys
from db_helper import DbHelper

if len(sys.argv) != 4:
    print('Incorrect usage. Specify args as: wineid no_bottles box')
else:
    with DbHelper() as db_helper:
        connection = db_helper.connection
        cursor = db_helper.cursor

        query = """
        INSERT INTO location (wineid, no, box, cellarversion) VALUES ({wineid}, {no}, {box}, 1)
        """.format(wineid=sys.argv[1], no=sys.argv[2], box=sys.argv[3])

        cursor.execute(query)
        connection.commit()
        print("1 Record inserted successfully")
