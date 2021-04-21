import psycopg2
from psycopg2 import Error
from data_model.db_model import BankUsers
from cust_logging.my_logger import MyLog as Log_Me
from bank_db.conn_access_point import DatabaseConn as conn_cred


class DbConn:
    # holds the data
    bankuser = {}

    @staticmethod
    def make_connect(query=None, var_tuple=None):
        DbConn.bankuser.clear()
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
                    DbConn.bankuser[counter] = BankUsers(identify_me=row[0], username=row[1], password=row[2],
                                                         disabled=row[3], date_created=row[4])
                    counter += 1
                Log_Me.info_log("You are connected to Postgre here are your results - ")
                Log_Me.info_log(record)
                Log_Me.info_log(DbConn.bankuser)
                return DbConn.bankuser

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
    DbConn.make_connect("SELECT * FROM bank_users;")
