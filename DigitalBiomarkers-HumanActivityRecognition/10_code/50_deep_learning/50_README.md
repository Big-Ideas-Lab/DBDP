**Data sources:**
1. Our data - https://www.nature.com/articles/s41746-020-0226-6
2. PAMAP2 - https://archive.ics.uci.edu/ml/datasets/PAMAP2+Physical+Activity+Monitoring
   We used PAMAP2 to test the validity of our deep learning models.

51_model_templates: 
   - Processing data for model setup
   
52_pytorch_models:
   - STEP (Duke Data):
  
      ANN (not windowed) notebooks.
    
   - PAMAP2:
  
      Same ANN format as in the corresponding TensorFlow model.
  
53_tensorflow_models:

   - STEP (Duke Data):
   
         There are three different models that build on each other in terms of complexity.

         1. 10_ANN which is our Artificial Neural Network which classifies individual timepoints

         2. 20_ANN_WFE which uses features that have been engineered from 30_end_pre_processing/32_engineer_features/33_feature_engineering.ipynb. 

         3. 30_ANN_WFE_Vote which uses a voting schema to classify minute windows. 

  - PAMAP2:
 
         ANN (not windowed) model notebooks.

These models are the same except the data input.

**Feel free to use other data sources as well: feature_engineered, rolled, or super_window.**
