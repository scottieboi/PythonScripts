import sys
from db_helper import DbHelper
import argparse

# Construct the argument parser
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument('searchterms', metavar='search', type=str,
                nargs='+', help='A list of search terms')
ap.add_argument("-v", "--version", required=False, type=int,
                help="Specifies a cellar version no. to search within")
args = vars(ap.parse_args())


def create_search_str(searchterms):
    result = []
    for searchterm in searchterms:
        search_str = []
        search_str.append(
            "LOWER(v.vineyard) LIKE '%{search}%'".format(search=searchterm))
        search_str.append(
            "LOWER(wl.winename) LIKE '%{search}%'".format(search=searchterm))
        search_str.append(
            "LOWER(wt.winetype) LIKE '%{search}%'".format(search=searchterm))

        if searchterm.isdigit():
            search_str.append(
                "wl.vintage={search}".format(search=int(searchterm)))

        result.append(" OR ".join(search_str))

    return result


with DbHelper() as db_helper:
    connection = db_helper.connection
    cursor = db_helper.cursor

    # Default verion is 0
    version = 0
    if args['version'] != None:
        version = args['version']

    search_query = "(" + \
        ") AND (".join(create_search_str(args['searchterms'])) + ")"

    select_query = """
    SELECT wl.id, v.vineyard, wl.winename, wl.vintage, wt.winetype, q.bottlecount, q.boxes
    FROM winelist wl
    INNER JOIN vineyard v ON wl.vineyardid = v.id
    INNER JOIN winetype wt ON wl.winetypeid = wt.id
    INNER JOIN
    (SELECT wl.id, COUNT(l.no) as bottlecount, array_agg(l.box) as boxes
    FROM winelist wl
    INNER JOIN vineyard v ON wl.vineyardid = v.id
    INNER JOIN winetype wt ON wl.winetypeid = wt.id
    INNER JOIN location l ON wl.id = l.wineid and l.cellarversion={version}
    WHERE {search_query}
    GROUP BY wl.id) AS q ON wl.id = q.id
    """.format(search_query=search_query, version=version)

    cursor.execute(select_query)
    records = cursor.fetchall()

    for r in records:
        print(str(r)[1:-1])
