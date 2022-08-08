"""Project hooks."""
from typing import Any, Dict, Iterable, Optional

from kedro.config import ConfigLoader, TemplatedConfigLoader
from kedro.framework.hooks import hook_impl
from kedro.io import DataCatalog
from kedro.versioning import Journal

from {{cookiecutter.package_name}}.utils import sql_to_query_parameter
from pathlib import Path
import os
import yaml
import logging
import pdb
import sys
import traceback
from datetime import datetime

logger = logging.getLogger(__name__)
class ProjectHooks:
    
    @hook_impl
    def register_config_loader(
        self, conf_paths: Iterable[str], env: str, extra_params: Dict[str, Any],
    ) -> TemplatedConfigLoader:
        
        base_conf = conf_paths[0]
        env_conf = conf_paths[1]  # kedro run --env=
        parameters = dict()
        
        try:
            for conf_path in conf_paths:
                base_parameters = Path(conf_path).joinpath('parameters.yml')
                base_dir_parameters = Path(conf_path).joinpath('parameters')
                if base_parameters.is_file():
                    parameters.update(yaml.safe_load(open(str(base_parameters))))
                if base_dir_parameters.is_dir():
                    for p in base_dir_parameters.iterdir():
                        parameters.update(yaml.safe_load(open(str(p))))            
        except IOError:
            logger.error('Could not find parameters.yml file.')
        except Exception as e:
            logger.error(f'Something wrong with parameters')
            raise e
        
        # Translate .sql files paths into parameters -> {query: "select * ...",}   
        parameters = sql_to_query_parameter(base_conf, parameters)
        
        # Add an environment variables to the dictionary
        # these variables will be interpolated in conf/*.yml
        try:
            env_dict = dict()
            environment_file = Path(env_conf).joinpath('environment.yml')
            environment_base_file = Path(base_conf).joinpath('environment.yml')
            if environment_file.is_file():
                env_dict.update(yaml.safe_load(open(str(environment_file))))
                logger.info(f"{str(env_conf).split('/')[-1]} variables loaded!")
            else:
                if environment_base_file.is_file():
                    env_dict.update(yaml.safe_load(open(str(environment_base_file))))
                    logger.info(f"Base reference env variables loaded!")
                    # file should be empty, try to get from environment
                    for key in list(env_dict):
                        if (not env_dict[key]):
                            env_dict[key] = os.getenv(key, '')
                else:
                    logger.error('No environment.yml found!')
                    logger.error(
                    '\n\nYou need a environment.yml at conf/base ' +
                    'only with used variable keys!\nDO NOT PUT VALUES ON IT! ' +
                    'Could be like:\n\nuser:\npassword:\n\n')
                    exit()
            parameters.update(env_dict)
            logger.info("Parameters updated!")
        except IOError:
            logger.error('Could not find environment.yml file.')
            logger.error('You should have at least a reference environment.yml file inside conf/base')
        except TypeError as e:
            logger.error(f"Some declared variable is not present on environment")
            raise e
        except Exception as e:
            logger.error(f'Something wrong with environment file')
            raise e
        
        if "TODAY_DATE" not in parameters.keys():
            # If key doesn't exist
            today_date_environment = os.getenv("TODAY_DATE")
            if today_date_environment:
                logger.info(f"TODAY_DATE set from environment variable: {today_date_environment}")
                parameters["TODAY_DATE"] = today_date_environment
            else:
                logger.info("TODAY_DATE not provided, setting with python datetime...")
                parameters["TODAY_DATE"] = datetime.today().strftime("%Y%m%d")
        elif not parameters["TODAY_DATE"]:
            # If there is key but not value
            logger.info("TODAY_DATE without value, setting with python datetime...")
            parameters["TODAY_DATE"] = datetime.today().strftime("%Y%m%d")
        else:
            logger.info("Using TODAY_DATE from parameters.yml")
            logger.info(f"TODAY_DATE = {parameters['TODAY_DATE']}")
            

        # The standard values are stored in parameters.yml but globals_dict overwrites
        # this yml file. So, the loop below prevents the globals_dict overwrite
        # the config values to None and maintain the parameters.yml value.
        for key in list(parameters):
            if (not parameters[key]):
                logger.error(f'{key} was declared but not provided!')
                parameters.pop(key, None)
        
        return TemplatedConfigLoader(
            conf_paths,
            globals_pattern='*parameters.yml',
            globals_dict=parameters
        )

    @hook_impl
    def register_catalog(
        self,
        catalog: Optional[Dict[str, Dict[str, Any]]],
        credentials: Dict[str, Dict[str, Any]],
        load_versions: Dict[str, str],
        save_version: str,
        journal: Journal,
    ) -> DataCatalog:
        return DataCatalog.from_config(
            catalog, credentials, load_versions, save_version, journal
        )

class PDBNodeDebugHook:
    """A hook class for creating a post mortem debugging with the PDB debugger
    whenever an error is triggered within a node. The local scope from when the
    exception occured is available within this debugging session.
    """

    @hook_impl
    def on_node_error(self):
        _, _, traceback_object = sys.exc_info()

        #  Print the traceback information for debugging ease
        traceback.print_tb(traceback_object)

        # Drop you into a post mortem debugging session
        pdb.post_mortem(traceback_object)
    
    @hook_impl
    def on_pipeline_error(self):
        # We don't need the actual exception since it is within this stack frame
        _, _, traceback_object = sys.exc_info()

        #  Print the traceback information for debugging ease
        traceback.print_tb(traceback_object)

        # Drop you into a post mortem debugging session
        pdb.post_mortem(traceback_object)
