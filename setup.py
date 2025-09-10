from setuptools import setup
import versioneer

setup(
    name='autofeedback',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
