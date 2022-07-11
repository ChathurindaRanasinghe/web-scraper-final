import json
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection


def connect_database(local:bool = True) -> connection:
    while True:
        try:
            if local:
                return psycopg2.connect(host='localhost', database='pcmarketexpert',
                                    user='chathurindaranasinghe', password='Chathurinda99*', cursor_factory=RealDictCursor)
            else:
                return psycopg2.connect(host='ec2-34-227-120-79.compute-1.amazonaws.com', database='d9d22fts9g9a5v',
                                user='lyziyojnxnwrft',
                                password='753a0badd64ebbf8df3ce4032f3edac65f87eb09be85ad005448fba0708f3e81',
                                cursor_factory=RealDictCursor)

        except Exception as error:
            print("Connection Failed! :(")
            print("Error: ", error)
            time.sleep(2)


def save_data(products: dict,local_db:bool) -> bool:
    conn = connect_database(local=local_db)
    cursor = conn.cursor()

    for category in products:
        for product in products[category]:
            if bool(product.shops):
                query = """
                        INSERT INTO "pc-parts" (NAME,PRICES,SHOPS,SPECS,BRAND,AVAILABILITY,LINKS,CATEGORY,INDEX) 
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                        """
                record = (
                    product.name,
                    json.dumps(product.prices),
                    json.dumps(product.shops),
                    json.dumps(product.specs),
                    product.brand,
                    json.dumps(product.availability),
                    json.dumps(product.links),
                    product.category,
                    product.index
                )
                cursor.execute(query, record)
                conn.commit()
