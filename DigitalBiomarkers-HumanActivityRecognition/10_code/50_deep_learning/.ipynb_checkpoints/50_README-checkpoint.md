**Data sources:**
1. Our data - https://www.nature.com/articles/s41746-020-0226-6
2. PAMAP2 - https://archive.ics.uci.edu/ml/datasets/PAMAP2+Physical+Activity+Monitoring
   We used PAMAP2 to test the validity of our deep learning models.

51_model_templates: 
- Processing data for model setup

52_pytorch_models:
- STEP (Duke Data):
   CNN (windowed) and ANN (not windowed) notebooks.
   The ANN has a voting mechanism to classify an entire block of 40 timepoints (a window) as the majority classifier of those timepoints.
- PAMAP2:
   Same ANN format as in the corresponding TensorFlow model.

53_tensorflow_models:
- STEP (Duke Data):
  CNN (windowed) and ANN (not windowed) model notebooks. There are also variations of the ANN that include rolled data or data with feature engineering.
- PAMAP2:
  CNN (windowed) and ANN (not windowed) model notebooks
These models are the same except the data input.

**Feel free to use other data sources as well: feature_engineered, rolled, or super_window.**
