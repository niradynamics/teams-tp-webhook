from setuptools import setup, find_packages

setup(
    name='TeamsTPWebhook',
    version='0.1dev',
    packages=find_packages(exclude=['tests']),
    license='MIT',
    install_requires=[
        'aiohttp==3.4.4',
        'aiohttp-negotiate',
        'botbuilder-core>=4.0.0.a6'
        ],
    entry_points={
        'console_scripts': [
            'teams-tp-webhook-server=teams_tp_webhook.server:main',
        ]
    }

)