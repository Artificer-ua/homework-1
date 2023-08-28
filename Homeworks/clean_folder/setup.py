from setuptools import setup

setup(name='clean_folder',
      versiom='0.0.3',
      packages=['clean_folder'],
      # packages=find_packages(),
      author='Serhii',
      description="clean folder from trash",
      licence='MIT',
      entry_points={'console_scripts':['clean-folder=clean_folder.clean:main']}
      )