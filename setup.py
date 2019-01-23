from setuptools import setup


with open('requirements.txt', 'r') as f:
    install_requires = f.read().splitlines()

setup(
    name='One-Click',
    version='0.1',
    install_requires=install_requires,
    entry_points='''
        [console_scripts]
        one-click=one_click.cli:main
    '''
)
