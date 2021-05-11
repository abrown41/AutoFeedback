class randomvar :
   def __init__( self, expectation, variance=0, vmin="unset", vmax="unset", isinteger=False ) :
       self.expectation = expectation
       self.variance = variance
       self.isinteger = isinteger
       self.lower=vmin
       self.upper=vmax
       self.diagnosis="ok"

   def check_for_bad_value( self, val ) :
       if self.isinteger : 
          from math import isclose
          if not isclose(val,round(val),abs_tol=10**-7)  : 
             self.diagnosis="integer"
             return(False)
       if self.lower=="unset" and val>self.upper : 
          self.diagnosis="range"
          return(False)
       elif self.lower=="unset" :
          return(True)
       if val<self.lower and self.upper=="unset" : 
          self.diagnosis="range"
          return(False)
       elif self.upper=="unset" : 
          return(True)
       if val<self.lower or val>self.upper : 
          self.diagnosis="range" 
          return(False)
       return(True)

   def check_value( self, val ) :
       if hasattr(val,"__len__") :
          for v in val : 
              if not self.check_for_bad_value(v) : return(False)
       elif not self.check_for_bad_value(val) : return(False)
       from math import sqrt
       from scipy.stats import norm
       if hasattr(val,"__len__") : stat = ( sum(val)/len(val) - self.expectation ) / sqrt(self.variance/len(val))
       else : stat = ( val - self.expectation ) / sqrt(self.variance)

       if stat>0 : pval = 2*norm.cdf(-stat)
       else : pval = 2*norm.cdf(stat)

       if pval<0.01 :
             self.diagnosis="hypothesis" 
             return(False)
       self.diagnosis="ok"
       return(True)

   def get_error( self, obj ) :
       error_message=""
       if self.diagnosis=="integer" :
             error_message="The " + obj + " should only take integer values" +"""
             You should be generating integer valued discrete random variables 
             Your random variables should thus only ever take integer values
             """
       elif self.diagnosis=="range" :
            error_message="The " + obj + " fall outside the allowed range of values for this type of random variable"
            if self.lower=="unset" : error_message += "\n The random variable should be less than or equal to " + str(self.upper)
            elif self.upper=="unset" : error_message += "\n The random variable should be greater than or equal to " + str(self.lower) 
            else : error_message += "\n The random variable should be between " + str(self.lower) + " and " + str(self.upper) 
       elif self.diagnosis=="hypothesis" :
            error_message="The " + obj +" appear to be sampled from the wrong distribution" + """
            To test if you generating a random variable from the correct distribution the test code 
            performs a hypothesis test.  The null hypothesis in this test is that you are sampling from the desired distribution 
            and the alternative is that you are not sampling the correct distribution.  The size of the critical region is determined using a 
            a significance level of 1%.  There is thus a small probability that you will fail on this test even if your code is correct.
            If you see this error only you should thus run the calculation again to check whether the hypothesis test is giving a type I
            error.  If you fail this test twice your code is most likely wrong.
            """
       return(error_message)
      
