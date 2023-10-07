import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="diploma_generator",
    version='{{VERSION_PLACEHOLDER}}',
    author="Andrés Alonzo",
    description="Generate diplomas using images and CSV Files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'fpdf==1.7.2',
    ],
    entry_points={
        'console_scripts': [
            'diploma_generator=diploma_generator.main:main',
            'diploma_generator_csv=diploma_generator.main:main_csv',
        ],
    },
    package_data={
        "diploma_generator": ["font.ttf"],
    },
    include_package_data=True
)
