from projen.python import PythonProject

project = PythonProject(
    name="DioMindmap",
    description="Create Draw.io mind map diagrams with indented text files.",
    module_name="diomindmap",
    version="0.1.5",
    author_email="anrichvs@gmail.com",
    author_name="Anrich van Schalkwyk",
    deps=["typer@0.9.0",
          "N2G@0.3.3",
          "python-igraph@0.10.6"],
    pytest=False,
    poetry=True,
    poetry_options={
        "repository": "https://github.com/AnrichVS/diomindmap",
        "scripts": {
            "diomindmap": "diomindmap.__main__:main"
        }
    }
)
project.add_git_ignore(".idea/")
project.synth()
