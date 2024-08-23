class randomvar:
    """
    generic class for random variables.
    allows you to test if students are sampling
    from a distribution.

    Attributes
    ==========
    expectation : float/list/np.array
        the expectation/s for your random variable/s
    dist : str
        type of distribution to use in hypothesis testing can be normal/chi2/
        conf_lim/uncertainty
    variance : float/list/np.array
        the variance/s for your random variable/s
    vmin : float/list/np.array
        the lowest value the random variable can take
    vmax : float/list/np.array
        the highest value the random variable can take
    isinteger : bool/list of bools
        True if the random variable must take an integer value
    meanconv : bool
        True if the input value you are testing is a list containing
        sample means calculated from progressively larger and larger numbers
        of identical random variables
    dof : int
        number of degrees of freedom to use when calculating test statistic
        with chi2 distribution
    limit : size of confidence limit to use when checking confidence limits
    transform : a function to transform the student's output to a
                random variable we can do a hypothesis test on
    nsamples : when testing function the size of the sample to take in
               order to test the students code
    """

    def __init__(self, expectation, dist="normal", variance=0, vmin="unset",
                 vmax="unset", isinteger=False, meanconv=False, dof=-1,
                 limit=-1, transform=None, nsamples=1):
        self.expectation = expectation
        self.variance = variance
        self.distribution = dist
        self.isinteger = isinteger
        self.meanconv = meanconv
        self.lower = vmin
        self.upper = vmax
        self.diagnosis = "ok"
        self.output_component = ""
        self.dof = dof
        self.limit = limit
        self.transform = transform
        self.nsamples = nsamples
        self.pval = 0
        if limit > 0 and dist == "chi2":
            if self.transform is not None:
                raise RuntimeError(
                    "cannot set transform if you are using confidence limit")
            self.transform = self._confToVariance

    def __str__(self):
        """ This is what is printed if the print method is executed on an
        instance of randomclass: it's defined as it is so that when
        AutoFeedback prints out the expected value of a given variable we get
        something other than '<AutoFeedback.randomclass.randomvar>'"""

        return f"{self.distribution} random variable between {str(self.lower)}\
 and {str(self.upper)} with expectation {str(self.expectation)}"

    def __len__(self):
        """This is what is returned if the len method is executed on an
        instance of randomclass. The expected length is equal to the number
        of expectation values that have been provided"""
        if hasattr(self.expectation, "__len__"):
            return len(self.expectation)
        return 1

    def _check_for_bad_value(self, val, num):
        """check if the value is within the allowed range for the random
        variable and (if relevant) it is an integer

           Parameters
           ==========
           val : float/list/np.array
                 value/s of random variable generated by student
           num : int
                 index of random variable from expectation array or -1 if only
                 one expectation specificd
           """
        if num < 0:
            isint = self.isinteger
        else:
            isint = self.isinteger[num]
        if isint:
            from math import isclose
            if not isclose(val, round(val), abs_tol=10**-7):
                self.diagnosis = "integer"
                return False

        if self.lower == "unset" and self.upper == "unset":
            return True
        low, up = self.lower, self.upper
        if self.lower != "unset" and num >= 0:
            low = self.lower[num]
        if self.upper != "unset" and num >= 0:
            up = self.upper[num]

        if self.lower == "unset" and val > up:
            self.diagnosis = "range"
            return False
        elif self.lower == "unset":
            return True
        if val < low and self.upper == "unset":
            self.diagnosis = "range"
            return False
        elif self.upper == "unset":
            return True
        if val < low or val > up:
            self.diagnosis = "range"
            return False
        return True

    def _confToVariance(self, value):
        """convert a confidence interval into a variance

        Parameters
        ==========
        value : float
                value of confidence interval
        """
        from scipy.stats import norm
        if self.limit <= 0:
            raise RuntimeError("limit needs to be to do this task set")
        return (value / norm.ppf((1 + self.limit) / 2))**2

    def _get_statistic(self, value, expectation, variance, number):
        """calculate the test statistic

        Parameters
        ==========
        value : float
                value of random variable
        expectation : float
                      expectation of random variable
        variance : float
                   variance of random variable
        number : float
                 number of random variables that the average was computed from
        """
        if self.distribution == "normal":
            from math import sqrt
            if variance < 0:
                RuntimeError("invalid")
            return (value - expectation) / sqrt(variance / number)
        elif self.distribution == "chi2":
            if self.dof <= 0:
                raise RuntimeError(
                    """if running chi2 test the number of degrees of
freedom needs to be set""")
            return self.dof * value / variance
        return 1

    def _hypo_check(self, stat):
        """perform the hypothesis test

        Parameters
        ==========
        stat : float
               value of test statistic
        """
        if self.distribution == "normal" or self.distribution == "chi2":
            from AutoFeedback.utils import check_module
            check_module("scipy")
        if self.distribution == "normal":
            from scipy.stats import norm
            if stat > 0:
                pval = 2 * norm.cdf(-stat)
            else:
                pval = 2 * norm.cdf(stat)
        elif self.distribution == "chi2":
            if self.dof <= 0:
                raise RuntimeError(
                    """if runnign chi2 test the number of degrees of freedom
needs to be set""")
            from scipy.stats import chi2
            pval = chi2.cdf(stat, self.dof)
            if pval > 0.5:
                pval = 1 - chi2.cdf(stat, self.dof)
        else:
            return False

        if self.diagnosis == "hypothesis":
            if pval > self.pval:
                pval = self.pval
        self.pval = pval
        self.diagnosis = "hypothesis"
        return pval > 0.05

    def check_value(self, val):
        """check that the value is consistent with the specified distribution

        Parameters
        ==========
        val : float/list/nparray
              values to check if they are from specified distribution/s
        """
        if self.distribution == "conf_lim":
            if len(val) != 3:
                self.diagnosis = "conf_number"
                return False
            # Check the mean
            self.distribution = "normal"
            if not self._check_random_var(val[1], -1):
                self.distribution = "conf_lim"
                self.output_component = "mean from the "
                return False
            # Now check the limits
            self.distribution = "chi2"
            if not self._check_random_var(self._confToVariance(
                    val[1] - val[0]), -1):
                self.distribution = "conf_lim"
                self.output_component = "lower confidence limit from the "
                return False
            if not self._check_random_var(self._confToVariance(
                    val[2] - val[1]), -1):
                self.distribution = "conf_lim"
                self.output_component = "upper confidence limit from the "
                return False
            self.distribution = "conf_lim"
            return True
        elif self.distribution == "uncertainty":
            if len(val) != 2:
                self.diagnosis = "uncertainty_number"
                return False
            # Check the mean
            self.distribution = "normal"
            if not self._check_random_var(val[0], -1):
                self.distribution = "uncertainty"
                self.output_component = "mean from the "
                return False
            # Now check the uncertainty
            self.distribution = "chi2"
            if not self._check_random_var(self._confToVariance(val[1]), -1):
                self.distribution = "uncertainty"
                self.output_component = "uncertainty from the "
                return False
            self.distribution = "uncertainty"
            return True
        else:
            if hasattr(self.expectation, "__len__"):
                if len(val) != len(self.expectation):
                    self.diagnosis = "number"
                    return False
                for n, v in enumerate(val):
                    if not self._check_random_var(v, n):
                        return False
                return True
            else:
                return self._check_random_var(val, -1)

    def _check_random_var(self, val, num):
        """check that a value is consistent with one of the specified
        distributions


        Parameters
        ==========
        val : float/list/nparray
              values to check if they are from the specified distribution
        num : int
              index of expectation array that we are using when testing if this
              is from correct distribution
        """
        if hasattr(val, "__len__"):
            for v in val:
                vv = v
                if self.transform is not None:
                    vv = self.transform(v)
                if not self._check_for_bad_value(vv, num):
                    return False
        else:
            vv = val
            if self.transform is not None:
                vv = self.transform(val)
            if not self._check_for_bad_value(vv, num):
                return False
        if hasattr(val, "__len__"):
            if num != -1 or self.transform is not None:
                raise RuntimeError(
                    "This function should never be called this way")
            if self.meanconv:
                from math import floor
                nn, stride = 0, int(floor(len(val) / 30))
                for vv in val:
                    nn = nn + 1
                    if nn % stride != 0:
                        continue
                    self.dof = nn
                    stat = self._get_statistic(
                        vv, self.expectation, self.variance, nn)
                    if not self._hypo_check(stat):
                        return False

                return True
            else:
                # Check on expectation
                mean = sum(val) / len(val)
                var = self.variance
                if self.variance == 0:
                    S2 = 0
                    for v in val:
                        S2 = S2 + v * v
                    var = (len(val) / (len(val) - 1)) * \
                        (S2 / len(val) - mean * mean)
                stat = self._get_statistic(
                    mean, self.expectation,
                    var, len(val))
                if not self._hypo_check(stat):
                    return False
                if self.variance == 0:
                    return True
                # Now check on variance
                self.distribution, S2, self.dof = "chi2", 0, len(val) - 1
                for v in val:
                    S2 = S2 + v * v
                var = (len(val) / self.dof) * (S2 / len(val) - mean * mean)
                stat = self._get_statistic(
                    var, self.expectation,
                    self.variance, len(val))
                if not self._hypo_check(stat):
                    self.distribution = "normal"
                    return False
                self.distribution = "normal"
                return True
        else:
            vv = val
            if self.transform is not None:
                vv = self.transform(val)

            if num < 0:
                stat = self._get_statistic(
                    vv, self.expectation, self.variance, 1)
            else:
                stat = self._get_statistic(
                    vv, self.expectation[num], self.variance[num], 1)

        return self._hypo_check(stat)

    def get_error(self, obj):
        """get the error message when the check fails

        Parameters
        ==========
        obj : str
              description of object that is not producing correct random
              variables
        """
        error_message = ""
        if self.diagnosis == "integer":
            error_message = f"""The {obj} should only take integer values
             You should be generating integer valued discrete random variables
             Your random variables should thus only ever take integer values
             """
        elif self.diagnosis == "range":
            error_message = f"""The {obj} fall outside the allowed range of
values for this type of random variable"""
            if self.lower == "unset":
                error_message += f"""\n The random variable should be less
 than or equal to  {self.upper}"""
            elif self.upper == "unset":
                error_message += f"""\n The random variable should be greater
 than or equal to {self.lower}"""
            else:
                error_message += f"""\n The random variable should be between
 {self.lower} and {self.upper}"""
        elif self.diagnosis == "hypothesis":
            error_message = f"""The {self.output_component}{obj} appear to be
sampled from the wrong distribution

            To test if you generating a random variable from the correct
            distribution the test code performs a hypothesis test.  The null
            hypothesis in this test is that you are sampling from the desired
            distribution and the alternative is that you are not sampling the
            correct distribution.  The size of the critical region is
            determined using a a significance level of 1%.  There is thus a
            small probability that you will fail on this test even if your code
            is correct. If you see this error only you should thus run the
            calculation again to check whether the hypothesis test is giving a
            type I error.  If you fail this test twice your code is most likely
            wrong.
            """
        elif self.diagnosis == "number":
            error_message = f"""The {obj} is not generating the correct number
of random variables

            You should be generating a vector that contains multiple random
            variables in this object
            """
        elif self.diagnosis == "conf_number":
            error_message = f"""The {obj} is not generating the correct number
of random variables.

            {obj} should return three random variables.  The first of these
            is the lower bound for the confidence limit.  The second is the
            sample mean and the third is the upper bound for the confidence
            limit
            """
        elif self.diagnosis == "uncertainty_number":
            error_message = f"""The {obj} is not generating the correct number
of random variables.

            {obj} should return two random variables.  The first of these
            is the sample mean and the second is the width of the error bar
            for the specified confidence interval around the sample mean
            """
        return error_message
