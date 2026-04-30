from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="var-estimation-tool",
    version="1.0.0",
    author="VaR Estimation Tool Contributors",
    description="Value at Risk (VaR) estimation tool using Monte Carlo simulation for TSE stocks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/VaR-Estimation-Tool",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/VaR-Estimation-Tool/issues",
        "Documentation": "https://github.com/yourusername/VaR-Estimation-Tool/blob/main/README.md",
        "Source Code": "https://github.com/yourusername/VaR-Estimation-Tool",
    },
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "matplotlib>=3.4.0",
    ],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "var-tool=main:main",
        ],
    },
    include_package_data=True,
    keywords="VaR Value-at-Risk Monte-Carlo risk-management financial-analysis Tokyo-Stock-Exchange",
    zip_safe=False,
)
