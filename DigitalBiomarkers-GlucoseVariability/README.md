Please note- this is not the repo for the package. (Please see links below for installation of this Python package). For extensibility, we provide all functions from the package in this repository. https://github.com/brinnaebent/cgmquantify

*This method is featured in our recent publication on the DBDP:*
> Bent, B., Wang, K., Grzesiak, E., Jiang, C., Qi, Y., Jiang, Y., Cho, P., Zingler, K., Ogbeide, F.I., Zhao, A., Runge, R., Sim, I., Dunn, J. (2020). The Digital Biomarker      Discovery Pipeline: An open source software platform for the development of digital biomarkers using mHealth and wearables data. Journal of Clinical and Translational Science, 1-28. doi:10.1017/cts.2020.511 ([Link to Open Access Article](https://www.cambridge.org/core/journals/journal-of-clinical-and-translational-science/article/digital-biomarker-discovery-pipeline-an-open-source-software-platform-for-the-development-of-digital-biomarkers-using-mhealth-and-wearables-data/A6696CEF138247077B470F4800090E63))


# cgmquantify: python package for analyzing glucose and glucose variability
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Continuous glucose monitoring (CGM) systems provide real-time, dynamic glucose information by tracking interstitial glucose values throughout the day. Glycemic variability, also known as glucose variability, is an established risk factor for hypoglycemia (Kovatchev) and has been shown to be a risk factor in diabetes complications. Over 20 metrics of glycemic variability have been identified.

Here, we provide functions to calculate glucose summary metrics, glucose variability metrics (as defined in clinical publications), and visualizations to visualize trends in CGM data.

#### [User Guide](https://github.com/brinnaebent/cgmquantify/wiki/User-Guide)
#### [Issue Tracking](https://github.com/brinnaebent/cgmquantify/issues)

#### Installation:
* **Recommended:** pip install cgmquantify
* If above does not work: pip install git+git://github.com/brinnaebent/cgmquantify.git
* git clone [repo](https://github.com/brinnaebent/cgmquantify.git)

#### Dependencies: (these will be downloaded upon installation with pip)
pandas, numpy, matplotlib, statsmodels, datetime

>Coming soon -
>* Currently only supports Dexcom CGM, more CGM coming soon
>* Integration with food logs, myFitnessPal food logs
>* Machine Learning methods for discovering trends in CGM data
