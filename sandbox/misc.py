from random import normalvariate

def resample(mean, sd, min = 0, max = 100):
    x = normalvariate(mean, sd)
    while not (min <= x <= max):
        x = normalvariate(mean, sd)
    return x

def limitedNormal(mu, sigma=None):
   """
       returns a random score from a normal (bell) distribution in
       which the mean, mu, is supplied by the caller, and in which the
       standard deviation, sigma, is computed such that 3-sigma does
       not drop below 0 [for mu < 50] or rise above 100 [for mu > 50]
       sigma is shown as a parameter but is not used -- it permits
       using the same arguments for all three *Normal() methods
   """
   if mu < 50.0:
       sigma = mu / 3.0
   else:
       sigma = (100.0 - mu) / 3.0
   return r.normalvariate(mu, sigma)