from setuptools import setup
import os
import shutil

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

if not os.path.isdir('cli_src'):
    os.makedirs('cli_src', exist_ok=True)

try:
    shutil.copytree('app', 'cli_src/app')
    shutil.copy('startup.py','cli_src/startup.py')
except:
    pass
setup(
    name="imagefapi",
    version="0.0.1",
    author="JohnnyRacer",
    license='MIT',
    description="A simple FastAPI based image endpoint solution.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johnnyracer/imagefapi",
    project_urls={
    "Bug Tracker": "https://github.com/johnnyracer/imagefapi/issues"},
    package_dir={"": "cli_src"},
        entry_points = {
        'console_scripts':[
            'imagefapi = startup:main'
        ]
    },
    install_requires =['anyio==3.5.0', 'asgiref==3.5.0', 'bcrypt==3.2.0', 'cffi==1.15.0', 'click==8.0.4', 'fastapi==0.75.1', 'gunicorn==20.1.0', 'h11==0.13.0', 'idna==3.3', 'passlib==1.7.4', 'pycparser==2.21', 'pydantic==1.9.0', 'pyjwt==2.3.0', 'python-dotenv==0.20.0', 'python-multipart==0.0.5', 'six==1.16.0', 'sniffio==1.2.0', 'starlette==0.17.1', 'typing-extensions==4.1.1', 'uvicorn==0.17.6', 'scikit-image==0.19.2', 'dhash==1.3'],
    python_requires=">=3.7",
)
