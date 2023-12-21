# %%
import jaydebeapi
import os
from dotenv import load_dotenv

load_dotenv()
MSSQL_PASSWORD = os.getenv("MSSQL_PASSWORD")
MSSQL_HOSTNAME = os.getenv("MSSQL_HOSTNAME")

# %%
conn = jaydebeapi.connect(
    jclassname="com.microsoft.sqlserver.jdbc.SQLServerDriver",
    url=f"jdbc:sqlserver://{MSSQL_HOSTNAME}:1433;databaseName=mortimer_dev;trustServerCertificate=true;",
    driver_args=["sa", MSSQL_PASSWORD],
    jars="./mssql-jdbc-12.4.2.jre11.jar",
)

# %%
curs = conn.cursor()
curs.execute("select * from nfl.VENUE")
res = curs.fetchall()
curs.close()
conn.close()
# %%
