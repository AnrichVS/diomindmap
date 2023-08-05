from projen.python import PythonProject

project = PythonProject(
    author_email="anrich@labs.epiuse.com",
    author_name="anrich",
    module_name="diomindmap",
    name="diomindmap",
    version="0.1.0",
)

project.synth()