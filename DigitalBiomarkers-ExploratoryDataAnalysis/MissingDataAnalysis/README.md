# Missing Data Analysis

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

If you use this method in your work, please cite the DBDP: dbdp.org and the references at the bottom of this page.

### Description

Visualization of the percent missingness per day and per hour for each subject present in the dataframe.


<img width="1104" alt="missingdataplot" src="https://user-images.githubusercontent.com/43549914/88846630-e20bd980-d1b3-11ea-95f3-ae151f775a2e.PNG">


### Instructions

Inputs to the function:

```sh
**Input:**
* Missing_Data_Plot.R script : plt_missing_data() function takes 4 inputs 
  * df = a dataframe that has at least 3 columns:
    * `subject_id` (character)
    * `tod` (numeric), this is the epoch time column
    * `measure` (numeric), this is the signal magnitude column
  * hertz of data collection (for example,if there is one measurement made per second, input `1`) 
  * lubridate standard `timezone` (for example,`America/New_York`) 
  * number of days worth of data in dataframe as numeric
```
```sh
**Output:**
Missing_Data_Plot.R script: plot that gives 1 subplot per unique `subject_id`, x axis is number of days present in the time range of the given dataframe, y axis is 0-23 (hour of the day)

```

Dependencies:

```sh
R 
```


### References

Here you should list any references you used to create this code.


License
----

Apache 2.0



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
