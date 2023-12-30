from setuptools import setup,find_packages
from typing import List
HYPHER_E_DOT = '-e .'
'''
In a requirements.txt file for Python projects, the -e flag is used to specify an editable installation. This is often used during development when you want to install a package in "editable" mode, meaning that changes to the source code will immediately affect the installed package without requiring a reinstallation.

'''


def get_requirements(file_path:str)->List[str]:
    '''
    This function will return the list of requirement .

    '''
    requirements = []
    with open(file_path) as file_pointer:
        requirements = file_pointer.readlines();
        requirements = [req.replace("\n","") for req in requirements]

        if HYPHER_E_DOT in requirements:
            requirements.remove(HYPHER_E_DOT)
    return requirements
setup(
    name='mlproject',
    version= '0.0.1',
    author= 'sanskar',
    author_email= 'sanskar1dethe@gmail.com',
    packages= find_packages(),
    install_requires = get_requirements('requirements.txt')
)