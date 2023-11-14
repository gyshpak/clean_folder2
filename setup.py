from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='1',
    description='sort files to directories by type',
    author='Gena Shpak',
    author_email='gena_shpak@ukr.net',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean_folder = clean_folder.clean:main']}
)