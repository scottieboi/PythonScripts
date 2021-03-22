import sys
from db_helper import DbHelper


if len(sys.argv) < 2:
    print('Incorrect usage. Please specify a search term.')
elif len(sys.argv) > 3:
    print('Incorrect usage. Too many args.')
else:
    with DbHelper() as db_helper:
        connection = db_helper.connection
        cursor = db_helper.cursor

        version = 0
        if len(sys.argv) == 3 and sys.argv[2].isdigit():
            version = sys.argv[2]

        print(version)

        select_query = """
        SELECT wl.id, v.vineyard, wl.winename, wl.vintage, wt.winetype, q.bottlecount
        FROM winelist wl
        INNER JOIN vineyard v ON wl.vineyardid = v.id
        INNER JOIN winetype wt ON wl.winetypeid = wt.id
        INNER JOIN
        (SELECT wl.id, COUNT(l.no) as bottlecount
        FROM winelist wl
        INNER JOIN vineyard v ON wl.vineyardid = v.id
        INNER JOIN location l ON wl.id = l.wineid and l.cellarversion={version}
        WHERE LOWER(v.vineyard) LIKE '%{search}%'
        GROUP BY wl.id) AS q ON wl.id = q.id
        """.format(search=sys.argv[1], version=version)

        cursor.execute(select_query)
        records = cursor.fetchall()

        for r in records:
            print(str(r)[1:-1])
