.. _Usage:

=====
Usage
=====

AutoFeedback offers three high-level functions for checking student code

.. code-block:: python

    from AutoFeedback import check_vars, check_func, check_plot

Then use one of the three high level functions available for checking student
code.

Checking Variables
==================

:py:meth:`AutoFeedback.check_vars`

.. code-block:: python

   assert check_vars('x', 3)

will check whether the student has defined a variable `x` in main.py to be equal to 3 and
print feedback to the screen.

Checking Functions
==================

:py:meth:`AutoFeedback.check_func`

There are two ways to use `check_func`. The first is to define the functions exactly as you
wish the students to do. You should also set the `.inputs` attribute of each
function as a list of tuples containing some sample inputs that can be used for
testing the function:

.. code-block:: python
   
   def addup(x, y):
      return x+y
   addup.inputs = [(3, 4), (5, 6)]

   def addAndSquare(x, y):
      z = addup(x, y) 
      return z * z
   addAndSquare.inputs = [(3, 4)]

   assert check_func(addup)
   assert check_func(addAndSquare, calls=['addup'])

Although this requires more lines of code than the legacy usage (see below), it
removes the need to pre-calculate the expected outputs, ensuring that
the results are robust against changes to libraries, environments etc.

Legacy usage
------------

The second method is to pass the function name as a string. This is maintained
for backwards compatability. In this case the inputs and expected outputs must
be passed:

.. code-block:: python

   assert check_func('addup', inputs=[(3, 4), (5, 6)], expected=[7, 11])

will check whether the student has defined a function named addup `addup` in main.py which takes two input arguments, adds them and returns the result. 

To check whether functions call other named functions, use the `calls` optional
argument:

.. code-block:: python

   assert check_func('addAndSquare', inputs=[(3, 4)], expected=[49], calls=['addup'])

which checks whether the function `addAndSquare` calls the function `addup` during
its execution.


Checking Plots
==============

:py:meth:`AutoFeedback.check_plot`

To check a student's plot object you must first define the 'lines' you expect to
see in the plot. The lines are of type :py:meth:`AutoFeedback.plotclass.line`
and are defined and tested as follows:


.. code-block:: python

   from AutoFeedback.plotclass import line
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


Checking random variables
=========================

AutoFeedback can be used to provide feedback on student code that generates
random variables. To get AutoFeedback to test student code for generating random
variables you must provide information on the distribution that the student is
supposed to sample from. AutoFeedback then uses this information to perform
various two-tailed hypothesis tests on the numbers that the student’s codes
generates. The null hypothesis for these tests is that the student’s code is
generating these random variables correctly. The alternative hypothesis is that
the student code is not correctly sampling from the distribution. When using
these sorts of tests **there is a finite probablity that the student is told
that their code is incorrect even when it is correct** This fact is clearly
explained to students in the feedback they receive so these tests can be used if
you are asking students complete a formative assessesment task. If you are using
AutoFeedback for summative assessment it is probably best not to rely on the
marks it gives if your tasks involve random variables.

Two types of hypothesis test are performed. In the first the test statistic is:

.. math::


   T = \frac{ \overline{X} - \mu }{ \sqrt{\sigma^2 / n} }

where :math:`\overline{X}` is a sample mean computed from :math:`n`
identical random variables. :math:`\mu` and :math:`\sigma^2`, meanwhile,
are the expectation and variance of the sampled random variables. Under
the null hypothesis (that the student’s code is correct) the test
statistic above should be a sample from a standard normal distribution.

The second type of hypothesis test uses the following test statistic:

.. math::


   U = \frac{(n-1)S^2}{\sigma^2}

where :math:`S^2` is a sample variance computed from :math:`n` identical
and independent random variables. :math:`\sigma^2` is then the variance
of the sampled random variables. Under the null hypothesis the test
statistic above should be a sample from a chi2 distribution with
:math:`(n-1)` degrees of freedom.

The examples that follow illustrate how AutoFeedback can be used a range
of tasks that you might ask students to perform as part of an elementary
course in statistics.

Single random variable
----------------------

Suppose you want students to write a code to set a variable called
``var`` so that is a sample from a standard normal random variable. The
correct student code would look like this:

.. code:: python

   import numpy as np

   var = np.random.normal(0,1)

You can test this code using ``check_vars`` and ``randomclass`` as
follows:

.. code:: python

   from AutoFeedback.varchecks import check_vars
   from AutoFeedback.randomclass import randomvar

   # Create a random variable object with expectation 0 and variance 1 to test the student variable against
   r = randomvar( 0, variance=1 )
   # Use check_vars to test the student variable var against the random variable you created
   assert( check_vars( "var", r ) )

``check_var`` here calculates the test statistic :math:`T` that was
defined earlier using the value the student has given to the variable
named ``var`` in place of :math:`\overline{X}`. As the student has
calculated only a single random variable :math:`n` is set equal to 1.

By a similar logic, if the student is supposed to set the variable ``U``
equal to a uniform continuous random variable that lies between 0 and 1
by using program like this:

.. code:: python

   import numpy as np

   U = np.random.uniform(0,1)

you can test this code using ``check_vars`` and ``randomclass`` as
follows:

.. code:: python

   from AutoFeedback.varchecks import check_vars
   from AutoFeedback.randomclass import randomvar

   # Create a random variable object with expectation 0.5 and variance 1/12 to test the student variable against
   r = randomvar( 0.5, variance=1/12, vmin=0, vmax=1 )
   # Use check_vars to test the student variable U against the random variable you created
   assert( check_vars( "U", r ) )

Now, because ``vmin`` and ``vmax`` were set when the random variable was
setup, AutoFeedback checks that ``U`` is between 0 and 1 before
performing the hypothesis test that was performed on the normal random
variable.

Fuctions for generating random variables
----------------------------------------

Lets suppose you have set students the task of writing a function for
generating a Bernoulli random variable. A correct solution to this
problem will look something like this:

.. code:: python

   import numpy as np

   def bernoulli(p) : 
       if np.random.uniform(0,1)<p : return 1
       return 0

If this function is working correctly it should only ever return 0 or 1.
We can use AutoFeedback to test that this is case by including the
following assert statement in a test:

.. code:: python

   from AutoFeedback.randomclass import randomvar

   # We will test the students code by generating a Bernoulli random variable with p=0.5
   # Notice that inputs and variables are lists here.  If the inputs list and variables list
   # have more than one element then the function is called and tested for each set of input
   # parameters.
   inputs, variables = [(0.5,)], []
   # Create a random variable object using what we know about the Expectation and variance of 
   # a Bernoulli random variable with p=0.5.  Notice that we have set isinteger=True so as to 
   # ensure that AutoFeedback checks that the random variable is 0 or 1.
   variables.append( randomvar( 0.5, variance=0.25, vmin=0, vmax=1, isinteger=True ) )
   assert( check_func( 'bernoulli', inputs, variables ) )

| When the test above is run a hypothesis test is also performed on the
  value of the random variable that was generated as was described in
  the previous section.
| This test is likely to pass as long as the student’s function returns
  a zero or one though. In other words, there is quite a high probablity
  of a false positive result in the hypothesis test. To reduce the
  likelihood of a false positive test you can add set ``nsamples`` when
  you define the ``randomvar`` object as shown below:

.. code:: python

   from AutoFeedback.randomclass import randomvar

   # We will test the students code by generating a Bernoulli random variable with p=0.5
   # Notice that inputs and variables are lists here.  If the inputs list and variables list
   # have more than one element then the function is called and tested for each set of input
   # parameters.
   inputs, variables = [(0.5,)], []
   # Create a random variable object using what we know about the Expectation and variance of
   # a Bernoulli random variable with p=0.5.  Notice that we have set isinteger=True so as to
   # ensure that AutoFeedback checks that the random variable is 0 or 1.
   variables.append( randomvar( 0.5, variance=0.25, vmin=0, vmax=1, isinteger=True, nsamples=100 ) )
   assert( check_func( 'bernoulli', inputs, variables ) )

This code calls the student’s code 100 times so a sample of 100
Bernoulli random variables is generated. AutoFeedback will then perform
a hypothesis test on the mean and variance of these 100 random variables
in the manner discussed in the section below on testing codes for
plotting samples of random variables.

It is worth using these exercises to get students to think about the
fact that the sample mean and the sample variance are random variables.
To get students to think about the sample mean you can ask them to write
a function similar to the one shown below.

.. code:: python

   import numpy as np

   def sample_mean(n) :
       mean = 0
       for i in range(n) : mean = mean + np.random.normal(0,1)
       return mean/n

The function above generates a sample mean by adding together :math:`n`
identical and independent normal random variables. The mean and variance
for the random variable the function outputs are thus 0 and :math:`1/n`.
We can thus use AutoFeedback to test the students code by writing:

.. code:: python

   from AutoFeedback.randomclass import randomvar

   # We are going to test for a sample mean computed from 100 normal random variables here
   inputs, variables = [(100,)], []
   # We provide information on the expected random variable here
   variables.append( randomvar( 0.0, variance=1/100 ) )
   # And test by calling check_func
   assert( check_func( 'sample_mean', inputs, variables ) )

We might also be interested in getting students to write a function for
calulating a sample variance like this:

.. code:: python

   import numpy as np

   def sample_variance(n) : 
       S2, mean = 0, 0 
       for i in range(n) : 
           rv = np.random.normal(0,1)
           mean, S2 = mean + rv, S2 + rv*rv 
       mean = mean / n 
       return (n/(n-1))*( S2 / n - mean*mean )

This code can be tested by calculating the test statistic I called
:math:`U` earlier. This statistic should be a sample from a chi2
distribution with :math:`n-1` degrees of freedom if the function is
correct. To complete such a test using AutoFeedback you would write the
following code:

::

   from AutoFeedback.randomclass import randomvar

   # We are going to test for a sample mean computed from 100 normal random variables here
   inputs, variables = [(100,)], []
   # Notice that we have to specify dist="chi2" here.  This tells AutoFeedback to do the comparison of variance test rathar than 
   # that the test on the expectation (the expectation is not used during testing here).  Notice, furthermore, that the variable 
   # dof must be set equal to n-1 (the number of degrees of freedom)
   variables.append( randomvar( 0.0, variance=1, dist="chi2", dof=99 ) )
   # And test by calling check_func
   assert( check_func( 'sample_variance', inputs, variables ) )

I like to emphasize that, if we are given the variance, we can estimate
any percentile of the distribution. I will thus often ask students to
write functions to estimate percentiles. I might for instance, ask
students to calculate the 56th percentile, which then can do by writing
the following function:

.. code:: python

   import scipy stats
   import numpy as np

   def confidence_limit(n) :
       S2, mean = 0, 0 
       for i in range(n) : 
           rv = np.random.normal(0,1) 
           mean, S2 = mean + rv, S2 + rv*rv
       mean = mean / n 
       var = (n/(n-1))*( S2 / n - mean*mean )

       return np.sqrt(var)*scipy.stats.norm.ppf(0.95)

To make it easy to test such codes I have provided an additional option
``limit`` for the chi2 test that converts the confidence interval that
is returned by such functions into a variance on which I can peform a
chi2 test. To test the function above you can thus write:

.. code:: python

   from AutoFeedback.randomclass import randomvar

   # We are going to test for a sample mean computed from 100 normal random variables here
   inputs, variables = [(100,)], []
   # This is once again doing the chi2 test but now the value returned from the function has to be converted from a confidence 
   # interval to a variance by doing the inverse of what is done in the final line of the example function above.  To do this 
   # tranformation you use the limit option as shown below.
   variables.append( randomvar( 0.0, variance=1, dist="chi2", dof=99, limit=0.90 ) )
   # And test by calling check_func
   assert( check_func( 'confidence_limit', inputs, variables ) )

The test above works because we set the ``transform`` property oof the
randomvar class equal to the following function:

.. code:: python

   def _confToVariance(self, value) :
       from scipy.stats import norm
       return ( value / norm.ppf( (1+self.limit)/2) )**2

This function inverts the transformation on the variance that was done
in the last line of student code above. The confidence interval that the
student provides is thus converted back into the variance. We can then
do the usual hypothesis test on the variance. Notice that when setting
up a randomvar object you can pass a function to the variable
``transform``. This feature is useful if you have asked the student to
calculate a function of a sample mean or sample variance as you can pass
a code for applying the inverse function to the student output and then
use AutoFeedback to do a hypothesis test on the sample mean or sample
variance that the student transformed.

Plotting random variables
-------------------------

Getting students to complete computer programming exercises is a good
way of getting them to generate plots that illustrate the behaviour of
mathematical objects. If students have a visual sense of what a concept
like convergence means it gives them a tool for making sense of the
formal, abstract definition when it is expressed symbolically. Much of
the functionality in AutoFeedback is thus geared towards testing the
plots that students produce.

In this section we thus illustrate how to test three plotting tasks that
we might ask students to complete:

Plotting a sample of random variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lets suppose that we want students to generate and plot a sample of
identical random variables using code something like this:

.. code:: python

   import matplotlib.pyplot as plt
   import numpy as np

   x, y = np.linspace(1,100,100), np.zeros(100)
   for i in range(100) : y[i] = np.random.uniform(0,1)

   plt.plot( x, y, 'ko' )
   plt.xlabel("Index")
   plt.ylabel("random variable")
   plt.showfig("myvariables.png")

We can test this code by using AutoFeedback as follows:

.. code:: python

   from AutoFeedback.plotchecks import check_plot
   from AutoFeedback.plotclass import line
   from AutoFeedback.randomclass import randomvar

   x, axislabels = np.linspace(1,100,100), ["Index", "random variable"]
   # Create a randomvar object using information on the distribution that was sampled
   var = randomvar( 0.5, variance=1/12, vmin=0, vmax=1 )
   # Now create a line object using plotclass and the random variable object that 
   # we just created  
   line1=line( x, var )

   # And check the students plot using check_plot
   assert( check_plot([line1],explabels=axislabels,explegend=False,output=True) )

The call to ``check_plot`` above checks the following things about the
student’s graph:

-  That the x coordinates of the points are the integers from 1 to 100.
-  That the y coordinates are all between 0 and 1.
-  That the x-axis label is “Index” and the y-axis label is “random
   variable”
-  (hypothesis test) That the sample mean of the 100 y coordinates is a
   sample from a normal distribution with :math:`\mathbb{E}(X)=0.5` and
   :math:`\textrm{var}(X)=1/1200`
-  (hypothesis test) That the sample variance of the 100 y coordinates
   is equal to 1/12.

Notice that if you are generating a discrete random variable you can
also use ``isinteger``. Adding this flag tells AutoFeedback to check
that all the y-coordinates should be integers.

Investigating convergence I: Sample mean
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once students can plot a sample of random variables the next obvious
thing to ask them to plot is a graph showing how the sample mean depends
on the sample size. The code to generate this plot is as follows:

.. code:: python

   import matplotlib.pyplot as plt
   import numpy as np

   S, x, y = 0, np.linspace(1,100,100), np.zeros(100)
   for i in range(100): 
       S = S + np.random.uniform(0,1)
       y[i] = S / x[i]

   plt.plot(x, y, 'ko')
   plt.xlabel("n")
   plt.ylabel("Sample mean")
   plt.showfig("mymean.png")


To test this student code you can use the ``meanconv`` option in
AutoFeedback as follows:

.. code:: python

   from AutoFeedback.plotchecks import check_plot
   from AutoFeedback.plotclass import line
   from AutoFeedback.randomclass import randomvar

   x, axislabels = np.linspace(1,100,100), ["n", "Sample mean"]
   # Create a randomvar object with meancov enabled
   var = randomvar( 0.5, variance=1/12, vmin=0, vmax=1, meancov=True )
   # Now create a line object using plotclass and the random variable object that
   # we just created
   line1=line( x, var )

   # And check the students plot using check_plot
   assert( check_plot([line1],explabels=axislabels,explegend=False,output=True) )


The code above checks:

-  That the x coordinates of the points are the integers from 1 to 100.
-  That the y coordinates are all between 0 and 1.
-  That the x-axis label is “n” and the y-axis label is “Sample mean”
-  (hypothesis test) That a subset of the y coordinates in the graph are
   samples from a normal random variable with :math:`\mathbb{E}(X)=0.5`
   and :math:`1/12/x` as would be expected. (We use a subset of the y
   coordinates here and not all of them because the likelihood of the
   test failing is high if we test all 100 coordinates)

Investigating convergence II: Sample variance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are numerous estimators for statistical quantities and you can ask
students to calculate and plot graphs of these quantities like the
graphs they produced for the sample mean in the previous section. For
example you might want students to look at the behaviour of the sample
variance. To draw a convergence graph for the sample variance students
would write a code like this one:

.. code:: python

   import matplotlib.pyplot as plt
   import numpy as np

   var = np.random.uniform(0,1)
   S, S2, x, y = var, var*var, np.linspace(2,101,100), np.zeros(100)
   for i in range(100) :
       var = np.random.uniform(0,1)
       S, S2 = S + var, S2 + var*var
       mean = S / x[i]
       y[i] = ( x[i] / (x[i]-1) )*( S2/x[i] - mean*mean )

   plt.plot( x, y, 'ko' )
   plt.xlabel("n")
   plt.ylabel("Sample variance")
   plt.showfig("mymean.png")

To then test this code you can use the following:

.. code:: python

   from AutoFeedback.plotchecks import check_plot
   from AutoFeedback.plotclass import line
   from AutoFeedback.randomclass import randomvar

   x, axislabels = np.linspace(2,101,100), ["n", "Sample varaiance"]
   # Create a randomvar object with meancov enabled.  Notice that we are testing the variance here so we use dist="chi2"
   var = randomvar( 0.5, variance=1/12, dist="chi2", meancov=True )
   # Now create a line object using plotclass and the random variable object that
   # we just created
   line1=line( x, var )

   # And check the students plot using check_plot
   assert( check_plot([line1],explabels=axislabels,explegend=False,output=True) )

Here AutoFeedback checks:

-  That the x coordinates of the points are the integers from 2 to 101.
-  That the x-axis label is “n” and the y-axis label is “Sample
   variance”
-  (hypothesis test) That when the test statistic :math:`U` is
   calculated for a subet of the y coordinates the resulting random
   variables are samples from a chi2 distribution with :math:`x-1`
   degrees of freedom.

Quoting the mean
~~~~~~~~~~~~~~~~

One of the key ideas that I want students to understand from my
statistics course is that when we are doing experiments we are
generating random variables. To make our experiments reproducible we
thus need to provide information on the distribution that we sampled. We
cannot just provide information on the results that were obtained. A
researcher testing if their results are the same as ours needs to be
able to determine the likelihood that his/her data are samples from the
statistical distribution that we obtained. I thus set students a number
of exercises that involve calculating confidence intervals or the widths
of error bars. In this section I will give examples of how you can test
student code for completing these tasks.

Calculating a confidence limit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Consider the function below:

.. code:: python

   import scipy.stats
   import numpy as np

   def conf_lim(n) :
       mean, S2 = 0, 0 
       for i in range(n) : 
           rv = np.random.normal(0,1)
           mean, S2 = mean + rv, S2 + rv*rv
       mean = mean / n
       var = (n/(n-1))*( S2/n - mean*mean )
       return mean + np.sqrt(var/n)*scipy.stats.norm.ppf(0.25), mean, mean + np.sqrt(var/n)*scipy.stats.norm.ppf(0.75)

This function estimates the sample mean and the sample variance for
:math:`n` random variables. This information is then used to calculate
estimates for the lower and upper quartiles for the distribution of the
mean. In addition, to returning the mean we can thus also quote an
interval and note that there is a 50% probability that the true mean
lies inside this range. Getting students to write code like this is
useful in terms of getting them to think about what confidence intervals
are.

To test the code above using AutoFeedback you would write something like
this:

.. code:: python

   from AutoFeedback.randomclass import randomvar

   # We are using 100 random variables to calculate our sample mean here
   inputs, variables = [(100,)], []
   # We now create our randomvar object using the option dist="conf_lim" to specify that we are expecting the 
   # students function to return three numbers much as we have done in the previous code.  Notice that we need to 
   # use dof to specify the number of degrees of freedom there are in the calculation of the variance and limit to 
   # specify what confidence limit we are quoting.
   variables.append( randomvar( 0.0, variance=1.0/100, dist="conf_lim", dof=99, limit=0.50 ) )
   # And test the function
   assert( check_func( 'conf_lim', inputs, variables ) )

The code above performs three hypothesis checks on the students code.

-  The test statistic :math:`T` is calculated from the second return
   value. This random variable should be a sample from a standard normal
   distribution.
-  The sample variance is computed from the first return value. The test
   statistic :math:`U` is then calculated from the sample variance. This
   random variable should be a sample from a chi2 distribution with 99
   degrees of freeom.
-  The sample variance is computed from the third return value. The test
   statistic :math:`U` is then calculated from the sample variance. This
   random variable should be a sample from a chi2 distribution with 9 9
   degrees of freeom.

### Quoting a mean and uncertainty

Instead of asking students to state a confidence interval explicitly as
they did in the previous task, we might as them to write a code like the
following one. This function returns the mean and a statistical
uncertainty for an 80% confidence interval.

.. code:: python

   import scipy.stats
   import numpy as np

   def uncertainty(n) :
       mean, S2 = 0, 0
       for i in range(n) :
           rv = np.random.normal(0,1)
           mean, S2 = mean + rv, S2 + rv*rv
       mean = mean / n
       var = (n/(n-1))*( S2/n - mean*mean )
       return mean, np.sqrt(var/n)*scipy.stats.norm.ppf(0.9)

To test this function using AutoFeedback you would write:

.. code:: python

   from AutoFeedback.randomclass import randomvar

   # We are using 100 random variables to calculate our sample mean here
   inputs, variables = [(100,)], []
   # We now create our randomvar object using the option dist="uncertainty" to specify that we are expecting the
   # students function to return three numbers much as we have done in the previous code.  Notice that we need to 
   # use dof to specify the number of degrees of freedom there are in the calculation of the variance and limit to 
   # specify what confidence limit we are quoting.
   variables.append( randomvar( 0.0, variance=1.0/100, dist="uncertainty", dof=99, limit=0.80 ) )
   assert( check_func( 'uncertainty', inputs, variables ) )

As in the previous section AutoFeedback will perform hypothesis tests on
the mean and variance that the student is quoting here.

Generating a histogram
----------------------

A final task that we might ask students to complete is to estimate a
histogram. The following code snippet indicates how this task is
achieved by repeatedly sampling from a binomial distribution:

.. code:: python

   import matplotlib.pyplot as plt
   import numpy as np

   nsamples = 1000000
   xvals, yvals = np.linspace(0,10,11), np.zeros(11)
   for i in range(nsamples) :
       xbin = int( np.random.binomial( 10, 0.5 ) )
       yvals[xbin] = yvals[xbin] + 1

   yvals = yvals / nsamples
   plt.bar( xvals, yvals, width=0.1 )
   plt.xlabel("Random variable")
   plt.ylabel("Fraction of occurances")
   plt.savefig("histo.png")    

The height of each bars in the histogram is an estimator for the
expectation of a Bernoulli random variable. Importantly, however, each
of these Bernoulli random variables has a different :math:`p` parameter.
When testing the code, we thus use a feature of AutoFeedback that we
have not used before. We use the fact that we can specify :math:`n`
dimensional vectors of expectations, variances and so on. If an
:math:`n`-dimensional vector of expectations is provided then
AutoFeedback expects to receive an :math:`n`-dimensional vector of
random variables from the student code. Any tests performed use the
first expectation to test the first value in the student’s vector, the
second expectation to test the second value and so on.

The code to test the program above would look like the following:

.. code:: python

   from AutoFeedback.plotchecks import check_plot
   from AutoFeedback.plotclass import line
   from AutoFeedback.randomclass import randomvar

   # Create lists to hold the x values, the expectations,
   # the variances, the lower bounds, the upper bounds and 
   # a bool to indicate that the expected values are not 
   # integers
   x, e, var, bmin, bmax, isi  = [], [], [], [], [], []
   for i in range(11) :
       x.append(i)
       pval = binom.pmf(i, 10, 0.5)
       e.append(pval)
       var.append(pval*(1-pval)/nsamples)
       bmin.append(0)
       bmax.append(1)
       isi.append(False)

   # Specify the axis labels
   axislabels = ["Random variable","Fraction of occurances"]
   # Use the information on the distribution that you have just included in 
   # the lists to create a randomvar object
   var = randomvar( e, variance=var, vmin=bmin, vmax=bmax, isinteger=isi )
   # Now create the line object
   line1=line( x, var )
   # And test using check_plot
   assert(check_plot([],exppatch=line1,explabels=axislabels,explegend=False,output=True))

The code above check the bars in the histograms the students have
produced. It checks that:

-  The x-coordinates of the bars are the numbers from 0 up to 10.
-  That the y-coordinates of the bars are between 0 and 1
-  (hypothesis tests) That the y-coordinates of the bars are consistent
   with being samples from a normal random variable with
   :math:`\mathbb{E}(X)=P(X=x)` and
   :math:`\mathbb{E}(X)=P(X=x)(1-P(X=x)) / n` where :math:`P(X=x)` is
   the probability mass function for the binomial random variable and
   :math:`n` is the number of samples.

Notice, last of all, that the feature we have used here to test the
histograms can be used when testing codes other than histograms. Anytime
that you are asking the students to produce a vector of non-identical
random variables you can test student code using the feature that has
been introduced in this last section. For example, you could also use
this feature to test code students are writing for looking at how the
variance of a sample mean that is computed from :math:`n` random
variables depends on the value of :math:`n`.
