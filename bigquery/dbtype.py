import pandas as pd


def td_ddl_full_type(
    ColumnType: str,
    ColumnLength: int,
    DecimalTotalDigits: int,
    DecimalFractionalDigits: int,
) -> str:
    """Generate a DDL column type from Teradata DBC data dictionary

    Args:
        ColumnType (str): DBC Columns ColumnType
        ColumnLength (int): DBC Columns ColumnLength
        DecimalTotalDigits (int): DBC Columns DecimalTotalDigits
        DecimalFractionalDigits (int): DBC Columns DecimalFractionalDigits

    Returns:
        str: The appropriate statement for a column DDL type
    """
    if ColumnType == "BF":
        return "BYTE(" + ColumnLength + ")"
    elif ColumnType == "BV":
        return "VARBYTE(" + ColumnLength + ")"
    elif ColumnType == "CF":
        return "CHAR(" + ColumnLength + ")"
    elif ColumnType == "CV":
        return "VARCHAR(" + ColumnLength + ")"
    elif ColumnType.ljust(2, " ") == "D ":
        return "DECIMAL(" + DecimalTotalDigits + "," + DecimalFractionalDigits + ")"
    elif ColumnType == "DA":
        return "DATE"
    elif ColumnType.ljust(2, " ") == "F ":
        return "FLOAT"
    elif ColumnType == "I1":
        return "BYTEINT"
    elif ColumnType == "I2":
        return "SMALLINT"
    elif ColumnType == "I8":
        return "BIGINT"
    elif ColumnType.ljust(2, " ") == "I ":
        return "INTEGER"
    elif ColumnType == "AT":
        return "TIME(" + DecimalFractionalDigits + ")"
    elif ColumnType == "TS":
        return "TIMESTAMP(" + DecimalFractionalDigits + ")"
    elif ColumnType == "TZ":
        return "TIME(" + DecimalFractionalDigits + ")" + " WITH TIME ZONE"
    elif ColumnType == "SZ":
        return "TIMESTAMP(" + DecimalFractionalDigits + ")" + " WITH TIME ZONE"
    elif ColumnType == "YR":
        return "INTERVAL YEAR(" + DecimalTotalDigits + ")"
    elif ColumnType == "YM":
        return "INTERVAL YEAR(" + DecimalTotalDigits + ")" + " TO MONTH"
    elif ColumnType == "MO":
        return "INTERVAL MONTH(" + DecimalTotalDigits + ")"
    elif ColumnType == "DY":
        return "INTERVAL DAY(" + DecimalTotalDigits + ")"
    elif ColumnType == "DH":
        return "INTERVAL DAY(" + DecimalTotalDigits + ")" + " TO HOUR"
    elif ColumnType == "DM":
        return "INTERVAL DAY(" + DecimalTotalDigits + ")" + " TO MINUTE"
    elif ColumnType == "DS":
        return (
            "INTERVAL DAY("
            + DecimalTotalDigits
            + ")"
            + " TO SECOND("
            + DecimalFractionalDigits
            + ")"
        )
    elif ColumnType == "HR":
        return "INTERVAL HOUR(" + DecimalTotalDigits + ")"
    elif ColumnType == "HM":
        return "INTERVAL HOUR(" + DecimalTotalDigits + ")" + " TO MINUTE"
    elif ColumnType == "HS":
        return (
            "INTERVAL HOUR("
            + DecimalTotalDigits
            + ")"
            + " TO SECOND("
            + DecimalFractionalDigits
            + ")"
        )
    elif ColumnType == "MI":
        return "INTERVAL MINUTE(" + DecimalTotalDigits + ")"
    elif ColumnType == "MS":
        return (
            "INTERVAL MINUTE("
            + DecimalTotalDigits
            + ")"
            + " TO SECOND("
            + DecimalFractionalDigits
            + ")"
        )
    elif ColumnType == "SC":
        return (
            "INTERVAL SECOND("
            + DecimalTotalDigits
            + ","
            + DecimalFractionalDigits
            + ")"
        )
    elif ColumnType == "BO":
        return "BLOB(" + ColumnLength + ")"
    elif ColumnType == "CO":
        return "CLOB(" + ColumnLength + ")"
    elif ColumnType == "PD":
        return "PERIOD(DATE)"
    elif ColumnType == "PM":
        return "PERIOD(TIMESTAMP(" + DecimalFractionalDigits + ")" + " WITH TIME ZONE"
    elif ColumnType == "PS":
        return "PERIOD(TIMESTAMP(" + DecimalFractionalDigits + "))"
    elif ColumnType == "PT":
        return "PERIOD(TIME(" + DecimalFractionalDigits + "))"
    elif ColumnType == "PZ":
        return "PERIOD(TIME(" + DecimalFractionalDigits + "))" + " WITH TIME ZONE"
    elif ColumnType == "++":
        return None
    elif ColumnType == "N":
        return "NUMBER(" + DecimalTotalDigits + "," + DecimalFractionalDigits + ")"


def td_type(
    ColumnType: str,
) -> str:
    """Generate a basic column type from Teradata DBC data dictionary

    Args:
        ColumnType (str): DBC Columns ColumnType

    Returns:
        str: The appropriate type
    """
    if ColumnType == "BF":
        return "BYTE"
    elif ColumnType == "BV":
        return "VARBYTE"
    elif ColumnType == "CF":
        return "CHAR"
    elif ColumnType == "CV":
        return "VARCHAR"
    elif ColumnType.ljust(2, " ") == "D ":
        return "DECIMAL"
    elif ColumnType == "DA":
        return "DATE"
    elif ColumnType.ljust(2, " ") == "F ":
        return "FLOAT"
    elif ColumnType == "I1":
        return "BYTEINT"
    elif ColumnType == "I2":
        return "SMALLINT"
    elif ColumnType == "I8":
        return "BIGINT"
    elif ColumnType.ljust(2, " ") == "I ":
        return "INTEGER"
    elif ColumnType == "AT":
        return "TIME)"
    elif ColumnType == "TS":
        return "TIMESTAMP"
    elif ColumnType == "TZ":
        return "TIME"
    elif ColumnType == "SZ":
        return "TIMESTAMP"
    elif ColumnType == "YR":
        return "INTERVAL YEAR"
    elif ColumnType == "YM":
        return "INTERVAL YEAR TO MONTH"
    elif ColumnType == "MO":
        return "INTERVAL MONTH"
    elif ColumnType == "DY":
        return "INTERVAL DAY"
    elif ColumnType == "DH":
        return "INTERVAL DAY TO HOUR"
    elif ColumnType == "DM":
        return "INTERVAL DAY TO MINUTE"
    elif ColumnType == "DS":
        return "INTERVAL DAY TO SECOND"
    elif ColumnType == "HR":
        return "INTERVAL HOUR"
    elif ColumnType == "HM":
        return "INTERVAL HOUR TO MINUTE"
    elif ColumnType == "HS":
        return "INTERVAL HOUR TO SECOND)"
    elif ColumnType == "MI":
        return "INTERVAL MINUTE"
    elif ColumnType == "MS":
        return "INTERVAL MINUTE TO SECOND"
    elif ColumnType == "SC":
        return "INTERVAL SECOND"
    elif ColumnType == "BO":
        return "BLOB"
    elif ColumnType == "CO":
        return "CLOB"
    elif ColumnType == "PD":
        return "PERIOD(DATE)"
    elif ColumnType == "PM":
        return "PERIOD(TIMESTAMP(WITH TIME ZONE))"
    elif ColumnType == "PS":
        return "PERIOD(TIMESTAMP())"
    elif ColumnType == "PT":
        return "PERIOD(TIME())"
    elif ColumnType == "PZ":
        return "PERIOD(TIME()) WITH TIME ZONE"
    elif ColumnType == "++":
        return None
    elif ColumnType == "N":
        return "NUMBER"


def bq_ddl(
    df: pd.DataFrame,
    td_type_mapping: pd.DataFrame,
) -> str:
    """Generate the DDL for a BigQuery table from metadata dataframe

    Args:
        df (pd.DataFrame): Pandas dataframe with columns

    Returns:
        str: SQL DDL for BigQuery
    """
    breakpoint()
    ddl = "create table " + df["DatabaseName"][0] + "." + df["TableName"][0] + " (\n"
    bq_rows = []
    for index, row in df.iterrows():
        bq_type = td_type_mapping[td_type_mapping["source_type"] == row["TdType"]][
            "target_type"
        ]
        bq_rows.append(row["ColumnName"] + " " + bq_type.values[0])
    ddl = ddl + "\n,".join(bq_rows)
    ddl = ddl + "\n)\n;\n"
    return ddl
