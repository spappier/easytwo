from setuptools import setup


with open('README.rst') as f:
    README = f.read()


setup(
    name='easytwo',
    version='0.1.1',
    description='Easy EC2 Queries.',
    long_description=README,
    author='Santiago Pappier',
    author_email='spappier@gmail.com',
    url='http://github.com/spappier/easytwo',
    entry_points=dict(console_scripts=['easytwo = easytwo:main']),
    py_modules=['easytwo'],
    install_requires=['boto3>=1.4', 'click>=6.7'],
    license='MIT',
    keywords='aws ec2',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
