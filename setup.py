
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="imagefapi",
    version="0.0.1",
    author="JohnnyRacer",
    license='MIT',
    include_package_data=True,
    description= "Simple FastAPI server to handle image CRUD operations."
    python_requires=">=3.7",
    install_requires = ['requests>=2.21.0', 'anyio==3.5.0', 'asgiref==3.5.0', 'bcrypt==3.2.0', 'cffi==1.15.0', 'click==8.0.4', 'fastapi==0.75.1', 'gunicorn==20.1.0', 'h11==0.13.0', 'idna==3.3', 'passlib==1.7.4', 'pycparser==2.21', 'pydantic==1.9.0', 'pyjwt==2.3.0', 'python-dotenv==0.20.0', 'python-multipart==0.0.5', 'six==1.16.0', 'sniffio==1.2.0', 'starlette==0.17.1', 'typing-extensions==4.1.1', 'uvicorn==0.17.6', 'scikit-image==0.19.2', 'redis==4.2.2', 'dhash==1.3'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johnnyracer/imagefapi",
    project_urls={"Bug Tracker": "https://github.com/johnnyracer/imagefapi/issues"}
        classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ]
)