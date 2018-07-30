from setuptools import setup

setup(name='httptest',
      version='0.1',
      description='The funniest joke in the world',
      url='https://github.com/LangJin/HttpTest',
      author='LangJin / Snake',
      author_email='fenyukuang@163.com',
      license='MIT',
      packages=['httptest'],
      install_requires=[
          'requests',
      ],
    entry_points={
        'console_scripts': [
            'httptest=httptest.cli:main'
        ]
    },
      zip_safe=False)