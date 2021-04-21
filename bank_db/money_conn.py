import psycopg2
from psycopg2 import Error
from cust_logging.my_logger import MyLog as Log_Me
from data_model.money_acct import CheckingAcct
from bank_db.conn_access_point import DatabaseConn as conn_cred


class MoneyDbConn:
    # holds the data
    bankacct = {}

    @staticmethod
    def make_connect(query=None, var_tuple=None):
        MoneyDbConn.bankacct.clear()
        connection = "No connection made yet!"
        cursor = connection
        try:
            # read connection parameters
            params = conn_cred.load_conn()
            # Connect to an existing database
            connection = psycopg2.connect(**params)
            # If you don't specify a query into this function then default to this
            if query is None:
                # Create a cursor to perform database operations
                cursor = connection.cursor()
                # Print PostgreSQL details
                Log_Me.info_log("PostgreSQL server information")
                Log_Me.info_log(connection.get_dsn_parameters())
                # Executing a SQL query
                cursor.execute("SELECT version();")
                # Fetch result
                record = cursor.fetchone()
                Log_Me.info_log("You are connected to - ")
                Log_Me.info_log(record)
            else:
                # Create a cursor to perform database operations
                cursor = connection.cursor()
                # Print PostgreSQL details
                Log_Me.info_log("PostgreSQL server information")
                Log_Me.info_log(connection.get_dsn_parameters())
                # Executing a SQL query
                cursor.execute(query, var_tuple)
                # Commit the SQL query
                connection.commit()
                # Fetch result
                record = cursor.fetchall()
                counter = 0
                for row in record:
                    MoneyDbConn.bankacct[counter] = CheckingAcct(acct_id=row[0], user_id=row[1], nickname=row[2], balance=row[3],
                                                         disabled=row[4], date_created=row[5])
                    counter += 1
                Log_Me.info_log("You are connected to Postgre here are your results - ")
                Log_Me.info_log(record)
                Log_Me.info_log(MoneyDbConn.bankacct)
                return MoneyDbConn.bankacct

        except (Exception, Error) as error:
            Log_Me.error_log("Error while connecting to PostgreSQL")
            Log_Me.error_log(error)
            raise error
        finally:
            if connection:
                cursor.close()
                connection.close()
                Log_Me.info_log("PostgreSQL connection is closed")


if __name__ == "__main__":
    MoneyDbConn.make_connect("SELECT * FROM bank_users;")
