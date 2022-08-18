=====
Usage
=====

Start by importing AutoFeedback.

.. code-block:: python

    import AutoFeedback

Then use one of the three high level functions available for checking student
code.

Checking Variables
==================

:py:meth:`AutoFeedback.varchecks.check_vars`

.. code-block:: python

   from AutoFeedback.varchecks import check_vars
   assert check_vars('x', 3)

will check whether the student has defined a variable `x` in main.py to be equal to 3 and
print feedback to the screen.

Checking Functions
==================

:py:meth:`AutoFeedback.funcchecks.check_func`

.. code-block:: python

   from AutoFeedback.func_checks import check_funcs
   assert check_func('addup', inputs=[(3, 4), (5, 6)], expected=[7, 11])

will check whether the student has defined a function named addup `addup` in main.py which takes two input arguments, adds them and returns the result. 

To check whether functions call other named functions, use the `calls` optional
argument:

.. code-block:: python

   assert check_func('addAndMult', inputs=[(3, 4)], expected=[84], calls=['addup'])

which checks whether the function `addAndMult` calls the function `addup` during
its execution.


Checking Plots
==============

:py:meth:`AutoFeedback.plotchecks.check_plot`

To check a student's plot object you must first define the 'lines' you expect to
see in the plot. The lines are of type :py:meth:`AutoFeedback.plotclass.line`
and are defined and tested as follows:


.. code-block:: python

   from AutoFeedback.plotclass import line
   from AutoFeedback.plotchecks import check_plot
   line1 = line([0,1,2,3], [0,1,4,9],
                linestyle=['-', 'solid'],
                colour=['r', 'red', (1.0,0.0,0.0,1)],
                label='squares')
   line2 = line([0,1,2,3], [0,1,8,27],
                linestyle=['--', 'dashed'],
                colour=['b', 'blue', (0.0,0.0,1.0,1)],
                label='cubes')

   assert check_plot([line1, line2], expaxes=[0,3,0,27], 
                     explabels=['x', 'y', 'Plot of squares and cubes']
                     explegend=True)

which checks to ensure that both the squared and cubed values are plotted with
the correct colour and linestyle, that the legend is shown with the correct
labels, and that the axis limits, labels and figure title are set correctly.
