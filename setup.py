from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt') as req:
        return req.read().splitlines()

setup(
    name='lumen-cli',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='An AI-powered CLI to illuminate your codebase with local LLMs.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/your-username/lumen-cli', # Replace with your repo URL
    packages=find_packages(),
    install_requires=read_requirements(),
    entry_points='''
        [console_scripts]
        lumen=lumen_cli.main:cli
    ''',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Documentation',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    python_requires='>=3.8',
)
