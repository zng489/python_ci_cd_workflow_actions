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
)