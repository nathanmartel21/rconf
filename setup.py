from setuptools import setup

setup(
    name='rconf',
    version='0.1.0',
    package_dir={'': 'src'},
    py_modules=['main'],
    packages=['modules'],
    install_requires=[
        'paramiko',
        'PyYAML'
    ],
    entry_points={
        'console_scripts': [
            'rconf=main:main',
        ],
    },
)