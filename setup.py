"""Build and install the wmtmetadata package."""

import os
from setuptools import setup, find_packages


def read_requirements():
    path = os.path.dirname(os.path.abspath(__file__))
    requirements_file = os.path.join(path, 'requirements.txt')
    try:
        with open(requirements_file, 'r') as req_fp:
            requires = req_fp.read().split()
    except IOError:
        return []
    else:
        return [require.split() for require in requires]


setup(name='wmtmetatdata',
      version='0.1',
      description='CSDMS Web Modeling Tool (WMT) component metadata and tools',
      author='Mark Piper',
      author_email='mark.piper@colorado.edu',
      license='MIT',
      url='http://csdms.colorado.edu',
      setup_requires=['setuptools', ],
      packages=find_packages(),
      # entry_points={
      #     'console_scripts': [
      #         'build-metadata=wmtmetadata.cmd.build:main',
      #     ],
      # },
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
      ],
)
