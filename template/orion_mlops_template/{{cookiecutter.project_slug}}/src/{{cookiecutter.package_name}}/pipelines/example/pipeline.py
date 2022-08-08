from kedro.pipeline import Pipeline, node

from .nodes import example_node


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                example_node,
                inputs=[
                    "params:parameter_1",
                ],
                outputs=["parameter_2"],

            ),
        ]
    )
