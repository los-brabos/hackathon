
import logging

logger = logging.getLogger(__name__)

def example_node(parameter1: str):
    """This node add a suffix into a string parameter

    Args:
        parameter1 (str): Random string
    """
    logger.info(f"String used: {parameter1}")

    return parameter1 + "_suffix"


