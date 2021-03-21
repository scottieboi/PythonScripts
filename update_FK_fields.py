import psycopg2
import os
from dotenv import load_dotenv


def update_region_id():
    select_query = """
    SELECT wl.id, wl.region, r.id
    FROM winelist wl
    INNER JOIN region r ON wl.region = r.region
    """

    cursor.execute(select_query)
    record = cursor.fetchall()

    print("Updating regionid")
    count = 0
    for r in record:
        update_query = """
        UPDATE winelist
        SET regionid = {regionid}
        WHERE id = {id}
        """.format(regionid=r[2], id=r[0])

        cursor.execute(update_query)
        connection.commit()
        count += cursor.rowcount

    print("Updated ", count, " rows")


def update_vineyard_id():
    select_query = """
    SELECT wl.id, wl.vineyard, v.id
    FROM winelist wl
    INNER JOIN vineyard v ON wl.vineyard = v.vineyard
    """

    cursor.execute(select_query)
    record = cursor.fetchall()

    print("Update vineyardid")
    count = 0
    for r in record:
        update_query = """
        UPDATE winelist
        SET vineyardid = {vineyardid}
        WHERE id = {id}
        """.format(vineyardid=r[2], id=r[0])

        cursor.execute(update_query)
        connection.commit()
        count += cursor.rowcount

    print("Updated ", count, " rows")


try:
    load_dotenv()
    # Connect to an existing database
    connection = psycopg2.connect(user=os.getenv("POSTGRES_USER"),
                                  password=os.getenv("POSTGRES_PASSWORD"),
                                  host="127.0.0.1",
                                  port="5432",
                                  database="wines")

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    # Print PostgreSQL details
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")
    # Executing a SQL query
    cursor.execute("SELECT version();")
    # Fetch result
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

    update_region_id()
    update_vineyard_id()


except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
