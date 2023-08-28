from setuptools import setup

setup(name='clean_folder',
      version='0.0.5',
      packages=['clean_folder'],
      # packages=find_packages(),
      author='Serhii',
      description="clean folder from trash",
      licence='MIT',
      entry_points={'console_scripts':['clean-folder=clean_folder.clean:main']}
      )