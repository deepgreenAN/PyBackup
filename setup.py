from setuptools import setup

install_requires = [
    "schedule"
]

packages = [
    "py_backup",
    "py_backup_cli"
]

console_scripts = [
    'schedule_and_backup=py_backup_cli.schedule_and_backup:main',
]


setup(
    name='py_backup',
    version='0.0.0',
    packages=packages,
    install_requires=install_requires,
    entry_points={'console_scripts': console_scripts},
    test_suit="test"
)