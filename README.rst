================================
AutoFeedback: Assignment Checker
================================

.. image:: https://github.com/abrown41/AutoFeedback/actions/workflows/build_test.yml/badge.svg
        :target: https://github.com/abrown41/AutoFeedback/actions/workflows/ 
.. image:: https://github.com/abrown41/AutoFeedback/actions/workflows/build_docs.yml/badge.svg
        :target: https://github.com/abrown41/AutoFeedback/actions/workflows/
.. image:: https://github.com/abrown41/AutoFeedback/actions/workflows/install.yml/badge.svg
        :target: https://github.com/abrown41/AutoFeedback/actions/workflows/

.. image:: https://img.shields.io/pypi/v/AutoFeedback.svg
        :target: https://pypi.python.org/pypi/AutoFeedback

.. image:: https://codecov.io/gh/abrown41/AutoFeedback/branch/master/graph/badge.svg?token=R2Z5SI6T71
        :target: https://codecov.io/gh/abrown41/AutoFeedback
        
.. image:: https://img.shields.io/lgtm/grade/python/g/abrown41/AutoFeedback.svg?logo=lgtm&logoWidth=18
        :target: https://lgtm.com/projects/g/abrown41/AutoFeedback/context:python


Check basic python exercises and provide pretty feedback

* Free software: 3-clause BSD license

===========
Description
===========
AutoFeedback is a suite of python utilities for testing and providing usable feedback introductory python assignments, specifically relevant to mathematics and the use of numpy and matplotlib.

=======================
How to use AutoFeedback
=======================

AutoFeedback can be installed via pip

.. code:: shell

    pip install AutoFeedback

The suite provides three basic checkers: one each for checking variables,
functions and matplotlib.pyplot figures. 

===========================================
Installing a local version of AutoFeedback
===========================================

If you want to develop AutoFeedback you can install a local version of the code. 

.. code:: shell

    cd <path to AutoFeedback>
    pip install -r requirements-dev.txt -r requirements.txt
    pip install -e .


=====
Usage
=====
Full usage instructions can be found `here. <https://abrown41.github.io/AutoFeedback/usage.html>`_
