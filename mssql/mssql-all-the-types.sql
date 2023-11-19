/*
MS SQL Server testing tables
 */
-- Working types
-- the columns that are commented out do not work in the pipeline with no extra settings
drop table if exists cwms.test_working_types go
create table
  cwms.test_working_types (
    test_char char
    --, test_bit bit /* ValueError: Failed to decode schema due to an issue with Field proto*/

  , test_bigint bigint
    --, test_datetime datetime /* return Timestamp(seconds=int(value.seconds), micros=int(value.micros)) TypeError: int() argument must be a string, a bytes-like object or a number, not 'NoneType'*/
    --, test_date date /* return Timestamp(seconds=int(value.seconds), micros=int(value.micros)) TypeError: int() argument must be a string, a bytes-like object or a number, not 'NoneType' */

  , test_decimal decimal(10, 4)
  , test_int int
  , test_numeric numeric(10, 4)
  , test_nvarchar nvarchar(max)
  , test_smallint smallint
    --, test_tinyint tinyint /* ValueError: Encountered a type that is not currently supported by RowCoder: nullable: true atomic_type: BYTE */

  , test_uniqueidentifier uniqueidentifier
  , test_varchar varchar(30)
  ) go
insert into
  cwms.test_working_types
values
  (
    'a'
    --, 1

  , 100000000000000
    --, GETDATE()
    --, GETDATE()

  , 1.12
  , 1
  , 1.12
  , 'abcdefghijklmnopqrstuvwyz1234567890!@#$%^&*()'
  , 1
    --, 1

  , newid()
  , 'abc'
  )
;

select
  test_char
, test_bigint
, test_decimal
, test_int
, test_numeric
, test_nvarchar
, test_smallint
, test_uniqueidentifier
, test_varchar
from
  mortimer_dev.cwms.test_working_types
;

-- All the types
-- A table with all the types that errors out when trying the pipeline
drop table if exists cwms.test_types go
create table
  cwms.test_types (
    test_char char
  , test_bit bit
  , test_bigint bigint
  , test_date date
  , test_datetime datetime
  , test_decimal decimal(10, 4)
  , test_int int
  , test_numeric numeric(10, 4)
  , test_nvarchar nvarchar(max)
  , test_smallint smallint
  , test_tinyint tinyint
  , test_uniqueidentifier uniqueidentifier
  , test_varchar varchar(30)
  ) go
insert into
  cwms.test_types
values
  (
    'a'
  , 1
  , 100000000000000
  , getdate()
  , getdate()
  , 1.12
  , 1
  , 1.12
  , 'abcdefghijklmnopqrstuvwyz1234567890!@#$%^&*()'
  , 1
  , 1
  , newid()
  , 'abc'
  )
;

-- BigQuery 
-- A target table in BigQuery to test moving data from SQL Server to BigQuery using a Dataflow template
create table
  cwms.test_types (
    test_char string
  , test_bit int64
  , test_bigint int64
  , test_date date
  , test_datetime datetime
  , test_decimal numeric
  , test_int int64
  , test_numeric numeric(10, 4)
  , test_nvarchar string
  , test_smallint int64
  , test_tinyint int64
  , test_uniqueidentifier string
  , test_varchar string
  )
;

-- Test Row Coder
-- All the bad types that do not work with the pipeline
drop table if exists cwms.test_bad_types 
go
;

create table
  cwms.test_bad_types (
    test_bit bit
    , test_date date
    , test_datetime datetime
    , test_tinyint tinyint
  ) 
go
insert into
  cwms.test_bad_types
values
  (
    1
    , cast(getdate() as date)
    , getdate()
    , 1
  )
;

-- BQ empty
drop table cwms.test_bad_types
;

create table
  cwms.test_bad_types (
    test_bit boolean
  , test_date date
  , test_datetime timestamp
  , test_tinyint int64
)
;