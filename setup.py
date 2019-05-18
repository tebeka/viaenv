import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def find_version():
    py_file = 'viaenv.py'

    with open(py_file) as fp:
        for line in fp:
            match = re.search("__version__ = '(.+)'", line)
            if match:
                return match.group(1)
    assert False, f'cannot find version in {py_file}'


with open('README.md') as fp:
    long_desc = fp.read()


setup(
    name='viaenv',
    version=find_version(),
    description='Configuration via environment',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    author='Miki Tebeka',
    author_email='miki.tebeka@gmail.com',
    license='BSD',
    url='https://github.com/tebeka/viaenv',
    py_modules=['viaenv'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'flake8', 'hypothesis'],
)
