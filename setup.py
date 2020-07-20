import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='pdf_scraper',
    version='0.1.0',
    author='Brennen Herbruck',
    author_email='brennen.herbruck@gmail.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bherbruck/pdf_scraper',
    packages=['pdf_scraper'],
    install_requires=requirements,
    python_requires='>=3.6',
)