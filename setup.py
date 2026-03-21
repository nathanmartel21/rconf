from setuptools import setup

setup(
    name='rconf',
    version='0.1.0',
    py_modules=['main'],
    packages=['modules'],
    install_requires=[
        'paramiko',
        'PyYAML'
    ],
    entry_points={
        'console_scripts': [
            # Crée la commande `rconf` qui pointe vers la fonction `main` du fichier `main.py`
            'rconf=main:main',
        ],
    },
)