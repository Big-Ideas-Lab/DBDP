
<img src="https://user-images.githubusercontent.com/43549914/73490467-9c906000-437a-11ea-9452-76ea8f8a1ceb.png" alt="drawing" width="400" hspace="30"/><img src="https://user-images.githubusercontent.com/43549914/73490405-77035680-437a-11ea-94c8-bbc555f443f0.png" alt="drawing" width="400"/>


# Human Activity Recognition using Physiological Data from Wearables
## Created By: Kush Gulati, Annie Hirsch, Noah Lanier, Nathan Warren
***

Human activity recognition (HAR) is a rapidly expanding field with a variety of applications from biometric authentication to developing home-based rehabilitation for people suffering from traumatic brain injuries. While HAR is traditionally performed using accelerometry data, a team of students led by researchers in the BIG IDEAS Lab will explore HAR with physiological data from wrist wearables. Using deep learning methods, students will extract features from wearable sensor data to classify human activity. The student team will develop a reproducible machine learning model that will be integrated into the Big Ideas Lab Digital Biomarker Discovery Pipeline (DBDP), which is a source of code for researchers and clinicians developing digital biomarkers from wearable sensors and mobile health technologies.

This project is in partnership with the Rhodes Information Iniative Data+ undergraduate summer research program. For more information on this project : https://bigdata.duke.edu/projects/human-activity-recognition-using-physiological-data-wearables
For more information on Data+: https://bigdata.duke.edu/data

## Project Summary
Traditional Human Activity Recognition (HAR) utilizes accelerometry (movement) data to classify activities. This summer, Team #4 examined using physiological sensors to improve HAR accuracy and generalizability. The team developed ML models that are going to be available open source in the Digital Biomarker Discovery Pipeline (DBDP) to enable other researchers and clinicians to make useful insights in the field of HAR.

In sum, the goal of the Human Activity Recognition Team is to create a predictive model that:
1. __Takes in multimodal data from mechanical sensors (such as accelerometers) and physiological sensors (such as electrodermal sensors and pulse oximeters).__
2. __Classifies human activity (Rest, Deep Breathing, Walking, Typing) at high accuracy and precision, while being generalizable and adaptable to other HAR datasets.__
## Background
Many HAR models only use one or two kinds of mechanical sensor data as inputs to infer behaviors (Dernbach, 2012; Kwapisz, 2011; Zeng, 2014). Our model is the first to incorporate several kinds of physiological data as well as one kind of mechanical sensor data. The model uses Blood Volume Pulse (physiological), Electrodermal Activity (physiological), Skin Temperature (physiological), and 3-axis accelerometry (mechanical). 

With our novel approach to using both mechanical and physiological data for activity recognition, we could possibly provide more detailed insight into user behavior and habits. Thus, our aim to make our model flexible enough to work well with other HAR datasets could help in providing better care for chronic diseases that often require major lifestyle changes for patients and monitoring vulnerable patients over long periods of time such as elderly patients or patients in intensive care. Because our model is multimodal, including a range of different types of physiological and mechanical data can aid in the effort of making care more personalized and/or effective. Lastly, using elements of multi-attribute classification, which is the inclusion contextual data such as age and gender to further tailor HAR models to each user, could improve the model’s accuracy for new datasets that include demographic data (Lara, 2013).

Our data was collected from Bent, et. al 2020: ["Investigating sources of inaccuracy in wearable optical heart rate sensors"](https://www.nature.com/articles/s41746-020-0226-6).


## Project Stages

| Deliverable |  Status |
| ------ | ------ | 
|Literature Review on Human Activity Recognition|Completed|
|Data Cleaning|Completed|
|Exploratory Data Analysis|Completed|
|Random Forest Model|Completed|
|Deep Learning Models|Completed|
|Documentation|In Progress|
## This Repo Contains:
* Literature Review
* Data Cleaning 
* Exploratory Data Analysis 
* Time Series Preprocessing
* Deep Learning Models
* Random Forest Model

## Built With

* [Python](https://www.python.org/) - Primary language for building end-to-end data to model pipeline
* [Pytorch](https://github.com/pytorch/pytorch) - Python library used for tensor computation and deep neural networks 
* [TensorFlow](https://github.com/tensorflow/tensorflow) - Python library for neural network and deep learning
* [Dataiku](https://www.dataiku.com/) - Automated platform powers both self-service analytics and the operationalization of our baseline machine learning model
* [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/) - Our team's primary interface to develop the project in Python
* [Tableau](https://www.tableau.com/) - Visualization tool for outliers, summary statistics, etc. 

## Contributors

* Brinnae Bent (Project Manager)
* Kush Gulati: [LinkedIn](https://www.linkedin.com/in/kush-gulati-duke/), [Github](https://github.com/kg227-dev)
* Annie Hirsch: [LinkedIn](https://www.linkedin.com/in/annie-h-50539b13b/), [Github](https://github.com/aihirsch) 
* Noah Lanier: [Github](https://github.com/Noah-Lanier)
* Nathan Warren: [LinkedIn](https://www.linkedin.com/in/nathan-warren-ds/), [Github](https://github.com/Nathan2Warren)



## License
This project was developed under the Big Ideas Lab - see their [webpage](http://dunn.pratt.duke.edu/) for more details.
We aspire to make our work open source, as a part of an overarching Digital Biomarker Discovery Pipeline. 
## Code Resources
| Author | Model Name | Model Description | Github Link | Paper Link 
| ------ | ------ | ------ | ------ | ------ 
| Ordóñez, 2016 | DeepConvLSTM | DeepConvLTSM combines CNN with LTSM 	recurrent layers. Has a dense layer structure. This model uses a deep convolutional neural network to extract features and a recurrent neural network to learn time dependencies. | [GitHub (from authors)](https://github.com/sussexwearlab/DeepConvLSTM)          [GitHub (Pytorch)](https://github.com/dspanah/Sensor-Based-Human-Activity-Recognition-DeepConvLSTM-Pytorch) | [Deep Convolutional and LSTM Recurrent Neural Networks for Multimodal Wearable Activity Recognition](https://www-mdpi-com.proxy.lib.duke.edu/1424-8220/16/1/115)
| Singh, 2020 | DeepConvLSTM w/ self-attention | Similar to the Ordonez model, but also includes an attention layer in addition to the CNN, RNN, LTSM and dense layer structure. | [GitHub](https://github.com/isukrit/encodingHumanActivity) | [Deep ConvLSTM with self-attention for human activity decoding using wearables](https://arxiv.org/abs/2005.00698)
| Ma, 2019 | AttnSense | AttentionSense model uses a convolutional layer for each sensor, followed by an attention layer for each sensor which applies an attention weight for each sensor. Stacked GRUs extract important temporal features. Softmax to find probability of each classification. | [GitHub](https://github.com/angelhunt/AttnSense) | [AttnSense: Multi-level Attention Mechanism For Multimodal Human Activity Recognition](https://www.ijcai.org/Proceedings/2019/0431.pdf)
| Yao, 2017 | DeepSense | DeepSense uses CNN → RNN with GRUs. CNN extracts local sensor features, while the RNN extracts temporal features. This model is the state-of-the-art model in Heterogeneous dataset, which used a CNN network to extract features of each sensor and combined them by another merge convolutional layer, then it used a LSTM network to learn time dependencies. | [GitHub](https://github.com/zhezh/DeepSense) | [DeepSense: A Unified Deep Learning Framework for Time-Series Mobile Sensing Data Processing](https://arxiv.org/abs/1611.01942)

## References

1. A. Reiss and D. Stricker. Introducing a New Benchmarked Dataset for Activity Monitoring. The 16th IEEE International Symposium on Wearable Computers (ISWC), 2012.
2. Bent, B., Goldstein, B.A., Kibbe, W.A. et al. Investigating sources of inaccuracy in wearable optical heart rate sensors. npj Digit. Med. 3, 18 (2020). https://doi.org/10.1038/s41746-020-0226-6
3. Ma, H., Li, W., Zhang, X., Gao, S., & Lu, S. (2019). AttnSense: Multi-level Attention Mechanism For Multimodal Human Activity Recognition. Proceedings of the Twenty-Eighth International Joint Conference on Artificial Intelligence. doi: 10.24963/ijcai.2019/431
4. Ordóñez, F., & Roggen, D. (2016). Deep Convolutional and LSTM Recurrent Neural Networks for Multimodal Wearable Activity Recognition. Sensors, 16(1), 115. doi: 10.3390/s16010115
5. Singh, S. P., Lay-Ekuakille, A., Gangwar, D., Sharma, M. K., & Gupta, S. (2020). Deep ConvLSTM with self-attention for human activity decoding using wearables. ArXiv, abs/2005.00698.
6. Yao, S., Hu, S., Zhao, Y., Zhang, A., & Abdelzaher, T. (2017). DeepSense. Proceedings of the 26th International Conference on World Wide Web. doi: 10.1145/3038912.3052577



