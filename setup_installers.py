from setuptools import setup, find_packages

with open("INSTALLER_README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="application-installers",
    version="1.0.0",
    author="Assistant",
    author_email="assistant@example.com",
    description="Demo installers for application deployment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/demo-installers",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'run-gui-installer=installer_demo:main',
            'run-console-installer=console_installer:main',
        ],
    },
    install_requires=[
        # зависимости могут быть добавлены при необходимости
    ],
)