from setuptools import setup 

setup(
    name="DemoLoading",
    packages=["loader_fhir"],
    # package_data={"orangedemo": ["icons/*.svg"]},
    classifiers=["Example :: Invalid"],
    # Declare orangedemo package to contain widgets for the "Demo" category
    entry_points={"orange.widgets": "DemoLoading = loader_fhir"},
)

