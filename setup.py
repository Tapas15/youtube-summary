"""
YouTube to Book Summary Converter - Setup Script

This package provides tools to convert YouTube videos into comprehensive
book-style summaries using Groq's LLM API.
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="youtube_summary",
    version="1.0.0",
    author="YouTube Summary Tool",
    author_email="support@example.com",
    description="Transform YouTube videos into comprehensive book-style summaries using AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/youtube_summary",
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.8",
    install_requires=[
        "youtube-transcript-api>=0.6.2",
        "groq>=0.9.0",
        "python-dotenv>=1.0.0",
        "tqdm>=4.66.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "youtube-summary=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Documentation :: Tools",
    ],
    keywords=[
        "youtube", "transcript", "summary", "ai", "groq", 
        "llm", "book", "converter", "video", "nlp"
    ],
    project_urls={
        "Bug Reports": "https://github.com/example/youtube_summary/issues",
        "Source": "https://github.com/example/youtube_summary",
        "Groq API": "https://console.groq.com/",
    },
)
