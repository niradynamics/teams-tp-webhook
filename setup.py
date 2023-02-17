from setuptools import setup, find_packages

setup(
    name='TeamsTPWebhook',
    version='0.7',
    packages=find_packages(exclude=['tests']),
    license='MIT',
    install_requires=[
        'aiohttp==3.8.4',
        'botbuilder-core==4.14.3',
        'pyhocon==0.3.60'
        ],
    entry_points={
        'console_scripts': [
            'teams-tp-webhook-server=teams_tp_webhook.server:main',
            'targetprocess_test=teams_tp_webhook.targetprocess:cmdline'
        ]
    },
    package_data={'':['reference.conf']},
)
