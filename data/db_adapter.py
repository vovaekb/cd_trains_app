import psycopg2
from datetime import datetime
from psycopg2.extras import RealDictCursor
from data.config import pg_config

class DBAdapter:
    def connect(self):
        self.conn = psycopg2.connect(**pg_config)

    def create_table(self):
        self.connect()
        print('Connection to DB is established')
        sql_query = "CREATE TABLE journeys_vladit_geek ("\
        "id SERIAL PRIMARY KEY,"\
        "source TEXT,"\
        "destination TEXT,"\
        "departure_datetime TIMESTAMP,"\
        "arrival_datetime TIMESTAMP,"\
        "carrier TEXT,"\
        "vehicle_type TEXT,"\
        "price FLOAT,"\
        "currency VARCHAR(3)"\
        ");"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql_query)
            self.conn.commit()
            print('Table is created')
        self.conn.close()

    def insert(self, journey):
        self.connect()
        sql_query = """
        INSERT INTO journeys_vladit_geek (source, destination,
                          departure_datetime, arrival_datetime, carrier,
                          vehicle_type, price, currency)
        VALUES (%(source)s,
                %(destination)s,
                %(departure_datetime)s,
                %(arrival_datetime)s,
                %(carrier)s,
                %(vehicle_type)s,
                %(price)s,
                %(currency)s);
        """
        format_str = '%d.%m.%Y %H:%M'  # The format
        departure_datetime = datetime.strptime(journey['departure_datetime'],
                                               format_str)
        arrival_datetime = datetime.strptime(journey['arrival_datetime'],
                                             format_str)
        values = {'source': journey['source'],
                  'destination': journey['destinations'],
                  'departure_datetime': departure_datetime,
                  'arrival_datetime': arrival_datetime,
                  'carrier': 'cd',
                  'vehicle_type': 'train',
                  'price': journey['price'],
                  'currency': 'CZK'
                  }
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql_query, values)
            self.conn.commit()
            print('Writing to table complete')
        self.conn.close()
        print('Done')

    def find_journeys(self, source, destination, departure_datetime):
        sql_select = """
        SELECT * FROM journeys_vladit_geek WHERE departure_datetime > %(departure_datetime) 
        AND source = %(source)
        AND destination = %(destination)
        """

        values = {'source': source,
                  'destination': destination,
                  'departure_datetime': departure_datetime}
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql_select, values)
            results_dict = cursor.fetchall()
            print(results_dict)
        self.conn.close()
