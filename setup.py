import setuptools


def get_version():
    version = {}
    with open('dbt_rpc_client/version.py') as fp:
        exec(fp.read(), version)
    return version['__version__']


with open('README.md', 'r') as f:
    readme = f.read()


setuptools.setup(
    name='dbt_rpc_client',
    author='David Wallace',
    author_email='david.wallace@goodeggs.com',
    version=get_version(),
    url='https://github.com/goodeggs/dbt-rpc-client',
    description='A python SDK for the dbt RPC server.',
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Topic :: Software Development',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    keywords="dbt python rpc",
    license='MIT',
    packages=setuptools.find_packages(exclude=['tests']),
    install_requires=[
        'requests>=2.22.0',
        'attrs>=19.3.0'
    ],
    python_requires='>=3.6'
)
