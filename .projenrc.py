from projen.python import PythonProject

project = PythonProject(
    name="DioMindmap",
    module_name="diomindmap",
    version="0.1.0",
    author_email="@anrichvs",
    author_name="Anrich van Schalkwyk",
    deps=["typer@0.9.0",
          "N2G@0.3.3",
          "python-igraph@0.10.6"],
    pytest=False,
    poetry=True
)
project.add_git_ignore(".idea/")
project.synth()
