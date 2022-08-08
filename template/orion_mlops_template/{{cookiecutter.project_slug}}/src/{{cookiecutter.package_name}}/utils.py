import re
from pathlib import Path
import sys

def is_venv():
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def sql_to_query_parameter(base_conf_path, parameters: dict) -> dict:
    """Change the parameter_sql: path/to/file.sql to
    parameter_query: query(str) inside globals_dict.

    Args:
        parameters (dict): parameters.yaml file inside conf/ folder

    Returns:
        dict: globals_dict used in Kedro context
    """

    project_path = Path(base_conf_path.split('conf')[0])
    global_dict = dict()
    sql_files = dict()
    suffix = '_sql'
    sql_paths = dict(
        filter(lambda kv_pair: kv_pair[0].endswith(suffix),
               parameters.items())
        )
    
    for parameter_name, sql_path in sql_paths.items():
        query_name = parameter_name.replace('sql', 'query')
        sql_files[parameter_name] = sql_path #.replace('src/maf_tickets/', '')
        try:
            p = project_path.joinpath(sql_files[parameter_name])
            if p.is_file():
                query = ''
                with open(str(p), 'r') as file:
                    query = file.read().rstrip().replace('\t', '').replace('\n', ' ').rstrip()
                query = re.sub(' +', ' ', query)
                if len(query):
                    global_dict[query_name] = query
        except Exception as exp:
            pass
    return global_dict