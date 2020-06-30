# loocvRF
#### A solution for leave-one-person-out-cross-validation random forests in Python
### This resource is part of the DBDP. Read more about the DBDP [here](dbdp.org).
#
 [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

##### **Author:** [Brinnae Bent](https://runsdata.org)

##
The DBDP is created by the **BIG IDEAS Lab** at Duke University: http://dunn.pratt.duke.edu/
If you use the DBDP in your work, please cite the DBDP: dbdp.org.

### Motivation

The motivation behind this project was the development of a random forest model with a leave-one-person-out-cross-validation (LOOCV) validation method. This general framework has been used in multiple studies, and is provided here in its general frame for you to use.  

### Dependencies
pandas, numpy, matplotlib.pyplot, [sklearn](https://scikit-learn.org/stable/) 

### Instructions

Here is a sample of how to use this function
```python
%run loocvRF.py     #make sure this file is in your local directory and run

# Import data
data = pd.read_csv('Test_RFLOOCV.csv')

# loocvRF() function
errors, RMSE, RMSEstd, MAPE, MAPEstd, importances = loocvRF(data=data, idcolumn='ID', outcomevar='Outcome', dropcols=['Feature6'], numestimators=1000, fs=0.02)

# importanceplot() function
importanceplot(importances, '2', 'filepathout')
}
```

### Documentation of Functions
```python
    """
        loocvRf()
        Main loocv RF function that calls other functions to do RF feature selection, training, and testing. 

        Args:
          data (pandas DataFrame): This is a dataframe containing each participant's features and outcome variables
          idcolumn (string): This is the column name of your column containing your participant number or ID (case sensitive)
          outcomevar (string): This is the column name of your outcome variable (case sensitive)
          dropcols (list): This is a list containing strings of each column you wish to drop in your dataframe. Default is empty list [].
          numestimators (integer): The number of trees you want built in your RF. Default=1000.
          fs (float): The cutoff importance for feature selection. Anything below this importance will be removed for the RF training.
          
        Returns:
            errors (list): This is a list with the absolute error between the predicted value and actual value for each fold.
            meanrmse (float): This is the mean root mean squared error (RMSE) over all of the folds
            stdrmse (float): This is the standard deviation of the root mean squared error (RMSE) over all of the folds
            meanrmse (float): This is the mean mean average percent error (MAPE) over all of the folds
            meanrmse (float): This is the standard deviation of the mean average percent error (MAPE) over all of the folds
            importances(pandas DataFrame): This is a pandas DataFrame with 3 columns: value (feature), importances (importance of the feature), and id (fold over which this feature importance was derived)
            
    """
    
    """
        importanceplot()
        Function that takes importances DataFrame as an input and outputs a bar chart of the importances of a defined fold. 

        Args:
          importances (pandas DataFrame): This is a dataframe outputed by loocvRF function that contains the feature importances for each fold
          ID (string): The fold over which you would like the plot
          filepathout (string): The filepath where you would like the plot saved to.
          
        Returns:
          The figure is returned as a .png file in the filepathout defined in args.
    
            
    """
```



### Issues

Please open a new "Issue", describe your problem, and tag the package author in the Issue.


License
----

Apache 2.0

***
Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
