"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline, pipeline

from {{cookiecutter.package_name}}.pipelines import example

def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    
    example_pipeline = example.create_pipeline()
    
    return {"__default__": pipeline([]),
    "example": example_pipeline
    }
