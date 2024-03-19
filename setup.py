from setuptools import find_packages, setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='piyankara Jayadewa (PJ)',
    author_email='piyankara.jayadewa@gmail.com',
    install_requires=["openai","langchain","nltk","numpy","streamlit","python-dotenv","pyPDF2"],
    packages=find_packages(),
)
