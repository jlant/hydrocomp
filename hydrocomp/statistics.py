# -*- coding: utf-8 -*-
"""
:Module: statistics.py

:Author: Jeremiah Lant
 
:Email: jlant@usgs.gov

:Purpose: 
Calculate the following statistics:

    - Nash-Sutcliffe
    - R Squared Coefficient
    - Mean Squared Error
    - Absolute Error
    - Relative Error
    - Percent Error
    - Percent Difference

"""

import numpy as np

def absolute_error(x, x_true):
    """
    Compute the absolute error between two arrays 
            
    *Parameters:*    
        x : array of data
        x_true : array of true data 
    
    *Return:*
        error : array of error
            
    *Example:*
    
    >>> import numpy as np
    
    >>> model_data = np.array([55.5, 62.1, 65.3, 64.4, 61.2])
    
    >>> observed_data = np.array([55.7, 62.0, 65.5, 64.7, 61.1])
    
    >>> absolute_error(x = model_data, x_true = observed_data)
    
    array([-0.2,  0.1, -0.2, -0.3,  0.1])   
    
    """
    
    # compute error
    error = x - x_true
    
    return error

def mean_squared_error(x, x_true):
    """ 
    Compute the mean square error between two arrays 
            
    *Parameters:*      
        x : array of data
        x_true : array of true data 
    
    *Return:*
        mse : value of mean square error
            
    *Example:*
    
    >>> import numpy as np
    
    >>> model_data = np.array([55.5, 62.1, 65.3, 64.4, 61.2])
    
    >>> observed_data = np.array([55.7, 62.0, 65.5, 64.7, 61.1])
    
    >>> mean_squared_error(x = model_data, x_true = observed_data)
    
    0.038000000000000228    
    
    """
     
    # compute error
    error = absolute_error(x, x_true)
    
    mse = np.mean(error**2)
    
    return mse

def relative_error(x, x_true):
    """    
    Compute the relative change between two arrays 
            
    *Parameters:*     
        x : array of data
        
        x_true : array of true data 
    
    *Return:*
        error : array of relative change
            
    *Example:*
    
    >>> import numpy as np
    
    >>> model_data = np.array([55.5, 62.1, 65.3, 64.4, 61.2])
    
    >>> observed_data = np.array([55.7, 62.0, 65.5, 64.7, 61.1])
    
    >>> relative_error(x = model_data, x_true = observed_data)
    
    array([-0.00359066,  0.0016129 , -0.00305344, -0.00463679,  0.00163666])    
    
    """
    
    # compute percent error
    error = absolute_error(x, x_true) / x_true
    
    return error

def percent_error(x, x_true):
    """    
    Compute the percent error between two arrays 
            
    *Parameters:*  
        x : array of data
        
        x_true : array of true data 
    
    *Return:*
        error : array of error

    *Example:*
    
    >>> import numpy as np
    
    >>> model_data = np.array([55.5, 62.1, 65.3, 64.4, 61.2])
    
    >>> observed_data = np.array([55.7, 62.0, 65.5, 64.7, 61.1])
    
    >>> percent_error(x = model_data, x_true = observed_data)

    array([-0.35906643,  0.16129032, -0.30534351, -0.46367852,  0.16366612])

    """ 
    
    # compute percent error
    error = relative_error(x, x_true) * 100
    
    return error

def percent_difference(x, x_true):
    """    
    Compute the percent diference between two arrays 
            
    *Parameters:*     
        x : array of data
        
        x_true : array of true data 
    
    *Return:*
        percent_diff : array of error

    *Example:*
    
    >>> import numpy as np
    
    >>> model_data = np.array([55.5, 62.1, 65.3, 64.4, 61.2])
    
    >>> observed_data = np.array([55.7, 62.0, 65.5, 64.7, 61.1])
    
    >>> percent_difference(x = model_data, x_true = observed_data)
    
    array([-0.35971223,  0.16116035, -0.3058104 , -0.464756  ,  0.1635323 ])

    """ 
    
    # compute percent difference
    avg = np.average((x, x_true), axis = 0)
    
    percent_diff = ((x - x_true)/avg) * 100
    
    return percent_diff

def r_squared(modeled, observed):
    """  
    Compute the Coefficient of Determination. Used to indicate how well
    data points fit a line or curve. Use numpy.coeff for computation.
                        
    *Parameters:*   
        modeled : array of modeled values
        
        observed : array of observed value
    
    *Return:*
    
        coefficient : model efficiency coefficient

    *Example:*

    >>> import numpy as np
    
    >>> model_data = np.array([55.5, 62.1, 65.3, 64.4, 61.2])
    
    >>> observed_data = np.array([55.7, 62.0, 65.5, 64.7, 61.1])
    
    >>> r_squared(modeled = model_data, observed = observed_data)
    
    0.99768587638100936

    """     
    
    r = np.corrcoef(modeled, observed)[0, 1]
    
    coefficient = r**2    
    
    return coefficient


def nash_sutcliffe(modeled, observed):
    """   
    Compute the Nash-Sutcliffe (model efficiency coefficient). Used to 
    assess the predictive power of hydrological models.
                
    E = 1 - sum((observed - modeled) ** 2)) / (sum((observed - mean_observed)**2 )))
            
    *Parameters:*     
        observed : array of observed discharges
        
        modeled : array of modeled discharges 
    
    *Return:*
        coefficient : model efficiency coefficient

    *Example:*
    
    >>> import numpy as np
    
    >>> model_data = np.array([55.5, 62.1, 65.3, 64.4, 61.2])
    
    >>> observed_data = np.array([55.7, 62.0, 65.5, 64.7, 61.1])
    
    >>> nash_sutcliffe(modeled = model_data, observed = observed_data)

    0.99682486631016043

    """     
    
    # compute mean value of the observed array
    mean_observed = np.mean(observed)

    # compute numerator and denominator
    numerator = sum((observed - modeled) ** 2)
    denominator = sum((observed - mean_observed)**2)

    # compute coefficient
    coefficient = 1 - (numerator/denominator)
    
    return coefficient

def main():
    """
    Script of computing statistics on a sample of modeled and observed data.
    """
    
    model_data = np.array([55.5, 62.1, 65.3, 64.4, 61.2])
    observed_data = np.array([55.7, 62.0, 65.5, 64.7, 61.1])
    
    print '** Sample Data **'
    print 'Modeled data: %s' % model_data
    print 'Observed data: %s' % observed_data
    print ''    
    print '** Statistics **'
    print 'Absolute error: %s' % absolute_error(x = model_data, x_true = observed_data)
    print 'Relative error: %s' % relative_error(x = model_data, x_true = observed_data)
    print 'Mean squared error: %s' % mean_squared_error(x = model_data, x_true = observed_data)
    print 'Percent error: %s' % percent_error(x = model_data, x_true = observed_data)
    print 'Percent difference: %s' % percent_difference(x = model_data, x_true = observed_data)
    print 'R squared: %s' % r_squared(modeled = model_data, observed = observed_data)
    print 'Nash-Sutcliffe: %s' % nash_sutcliffe(modeled = model_data, observed = observed_data)
    
    
if __name__ == "__main__":
    
    # call main
    main()





    
    
        
    
    