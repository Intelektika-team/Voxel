from setuptools import setup, find_packages

with open("README.txt", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='voxl',
    version='0.5',
    description='The voxel language api', 
    author='pt',
    author_email='kvantorium73.int@gmail.com',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/plain",
    install_requires=[
        'numpy>=1.21.0',
    ],
    entry_points={
        'console_scripts': [
            'voxel=voxel.cli:__main__',
        ],
    },
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)