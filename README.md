# python_ci_cd_workflow_actions

# ['python setup.py install', 'python setup.cfg install', 'pyproject.toml']
# pip install pipreqs
# python -m pipreqs.pipreqs

name: finnhub
email: zng489@hotmail.com
password: finnhub

API Key: cjvqj3pr01qjaspch750cjvqj3pr01qjaspch75g

-------------------------------
python_ci_cd_workflow_actions/setu.py

from setuptools import setup, find_packages

setup(
    name='your-package-name',
    version='0.1',
    url='http://github.com/yourusername/yourpackagename',
    author='author name',
    author_email='author@gmail.com',
    description='description of my package',
    packages=find_packages('src'),
    install_requires=[
        'requests',
        'python-dotenv',
        # other packages your project depends on
    ],
)-------------------------------------