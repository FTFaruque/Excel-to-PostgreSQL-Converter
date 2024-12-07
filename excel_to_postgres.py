from pandas import read_excel
from sqlalchemy import create_engine
from  json import load
from jsonschema import validate
from typing import Mapping
from argparse import ArgumentParser

__schema = {
    "$schema" : "https://json-schema.org/draft/2020-12/schema",
    "title" : "Config schema",
    "type" : "object",
    "properties" : {
        "Excel":{
            "type" : "object",
            "properties":{
                "source":{
                    "type" : "string"
                },
                "sheet_names":{
                    "type" : "array",
                    "items":{
                        "type" : "string"
                    },
                    "minItems" : 1
                }
            },
            "required" : ["source", "sheet_names"]
        },
        "Postgres-DB":{
            "type": "object",
            "properties":{
                "username":{
                    "type" : "string"
                },
                "password": {
                    "type" : "string"
                },
                "db_name": {
                    "type" : "string"
                },
                "server":{
                    "type" : "string"
                },
                "table_name" : {
                    "type" : "array",
                    "items":{
                        "type" : "string"
                    }
                }
            },
            "required" : ["username", "password", "db_name", "server"]
        },
        "name_map" : {
            "additionalProperties":{
                "type" : "string"
            }
        }
    },
    "required" : ["Excel", "Postgres-DB"]
}


def read_config(config_path:str) -> tuple[Mapping[str, any]]:
    "Read json and return config for excel, postgres and name_map for changing source to destination table name"
    with open(config_path, "r") as file:
        config = load(file)
        validate(config, __schema)
    if "name_map" not in config.keys():
        return config["Excel"], config["Postgres-DB"], {}
    return config["Excel"], config["Postgres-DB"], config["name_map"]


def load_to_postgres(source:str, sheet_name:None|str, pg_engine:object, table_name:str):
    df = read_excel(source, sheet_name=sheet_name)
    df.to_sql(
        table_name,
        pg_engine,
        if_exists="replace"
    )
    print(f"Synced:  source name:{sheet_name} destination name:{table_name}")

def map_sheetname_to_tablename(source_sheets, name_map={}):
    unmapped = set(source_sheets).difference(set(name_map.keys()))
    return {**name_map, **{k:k for k in unmapped}}



if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--path", help="path to json config file")
    config_path = parser.parse_args().path

    excel, pg_config, name_map = read_config(config_path)
    name_map = map_sheetname_to_tablename(excel["sheet_names"], name_map)

    pg_engine = create_engine(f"postgresql://{pg_config["username"]}:{pg_config["password"]}@{pg_config["server"]}:{pg_config["port"]}/{pg_config["db_name"]}")
    for sheet in excel["sheet_names"]:
        load_to_postgres(excel["source"], sheet, pg_engine, name_map[sheet])

