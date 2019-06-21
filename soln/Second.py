# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 
# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.
# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.
import numpy as np, pandas as pd, os
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_selection import VarianceThreshold
from sklearn.svm import NuSVC
from sklearn.metrics import roc_auc_score
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from sklearn.covariance import GraphicalLasso
from sklearn.mixture import GaussianMixture

from sklearn.cluster import KMeans
from tqdm import tqdm
from sklearn.pipeline import Pipeline
import warnings
import pickle
warnings.filterwarnings('ignore')


train = pd.read_csv('../input/train.csv')
test = pd.read_csv('../input/test.csv')

train.head()
cols = [c for c in train.columns if c not in ['id', 'target']]
cols.remove('wheezy-copper-turtle-magic')


def get_mean_cov(x,y):
    #print(x.shape)
    ms_list = []
    ps_list = []
    
    # Label equals to One
    ones = (y==1).astype(bool)
    model = GraphicalLasso()
    x2 = x[ones]
    kmeans = GaussianMixture(n_components=3, init_params='random', covariance_type='full')
    new_label = kmeans.fit_predict(x2)

    for elem in range(3):
        index = np.where(new_label == elem)
        tmp_df = x2[index]
        #print(tmp_df.shape)
        model.fit(tmp_df)
        p1 = model.precision_
        m1 = model.location_
        ms_list.append(m1)
        ps_list.append(p1)
    
    # Label equals to Zero
    onesb = (y==0).astype(bool)
    x2b = x[onesb]
    kmeans = GaussianMixture(n_components=3, init_params='random', covariance_type='full')
    new_label = kmeans.fit_predict(x2b)
    model = GraphicalLasso()
    for elem in range(3):
        index = np.where(new_label == elem)
        tmp_df = x2b[index]

        model.fit(tmp_df)
        p1 = model.precision_
        m1 = model.location_
        ms_list.append(m1)
        ps_list.append(p1)
        

    ms = np.stack(ms_list)
    ps = np.stack(ps_list)
    return ms, ps

def get_mean_cov2(x,y):
    #print(x.shape)
    ms_list = []
    ps_list = []
    
    # Label equals to One
    ones = (y==1).astype(bool)
    model = GraphicalLasso()
    x2 = x[ones]
    kmeans = KMeans(n_clusters=3, random_state=0).fit(x2)
    new_label = kmeans.labels_

    for elem in range(3):
        index = np.where(new_label == elem)
        tmp_df = x2[index]
        #print(tmp_df.shape)
        model.fit(tmp_df)
        p1 = model.precision_
        m1 = model.location_
        ms_list.append(m1)
        ps_list.append(p1)
    
    # Label equals to Zero
    onesb = (y==0).astype(bool)
    x2b = x[onesb]
    kmeans = KMeans(n_clusters=3, random_state=0).fit(x2b)
    new_label = kmeans.labels_
    model = GraphicalLasso()
    for elem in range(3):
        index = np.where(new_label == elem)
        tmp_df = x2b[index]

        model.fit(tmp_df)
        p1 = model.precision_
        m1 = model.location_
        ms_list.append(m1)
        ps_list.append(p1)
        

    ms = np.stack(ms_list)
    ps = np.stack(ps_list)
    return ms, ps

def get_mean_cov3(x,y):
    #print(x.shape)
    ms_list = []
    ps_list = []
    
    # Label equals to One
    ones = (y==1).astype(bool)
    model = GraphicalLasso()
    x2 = x[ones]
    kmeans = KMeans(n_clusters=3, random_state=0,algorithm='elkan').fit(x2)
    new_label = kmeans.labels_

    for elem in range(3):
        index = np.where(new_label == elem)
        tmp_df = x2[index]
        #print(tmp_df.shape)
        model.fit(tmp_df)
        p1 = model.precision_
        m1 = model.location_
        ms_list.append(m1)
        ps_list.append(p1)
    
    # Label equals to Zero
    onesb = (y==0).astype(bool)
    x2b = x[onesb]
    kmeans = KMeans(n_clusters=3, random_state=0,algorithm='elkan').fit(x2b)
    new_label = kmeans.labels_
    model = GraphicalLasso()
    for elem in range(3):
        index = np.where(new_label == elem)
        tmp_df = x2b[index]

        model.fit(tmp_df)
        p1 = model.precision_
        m1 = model.location_
        ms_list.append(m1)
        ps_list.append(p1)
        

    ms = np.stack(ms_list)
    ps = np.stack(ps_list)
    return ms, ps
    
# INITIALIZE VARIABLES
cols = [c for c in train.columns if c not in ['id', 'target']]
cols.remove('wheezy-copper-turtle-magic')
oof = np.zeros(len(train))
preds = np.zeros(len(test))

# BUILD 512 SEPARATE MODELS
for i in tqdm(range(512)):
    # ONLY TRAIN WITH DATA WHERE WHEEZY EQUALS I
    train2 = train[train['wheezy-copper-turtle-magic']==i]
    test2 = test[test['wheezy-copper-turtle-magic']==i]
    idx1 = train2.index; idx2 = test2.index
    train2.reset_index(drop=True,inplace=True)
    
    # FEATURE SELECTION (USE APPROX 40 OF 255 FEATURES)
    # IMPORTANT: SCALER ARE NEEDED FOR KMEANS
    pipe = Pipeline([('vt', VarianceThreshold(threshold=2)), ('scaler', StandardScaler())])
    train3 = pipe.fit_transform(train2[cols])
    test3 = pipe.fit_transform(test2[cols])   

    # STRATIFIED K-FOLD
#    skf = StratifiedKFold(n_splits=5, random_state=42, shuffle=True)
#    for train_index, test_index in skf.split(train3, train2['target']):
        
        # MODEL AND PREDICT WITH GMM
    ms, ps = get_mean_cov(train3,train2['target'].values)
    gm = GaussianMixture(n_components=6, init_params='random', covariance_type='full', tol=0.001, reg_covar=0.001, max_iter=100, n_init=1,means_init=ms, 
                         precisions_init=ps)
    #gm = GaussianMixture(n_components=6, init_params='random', covariance_type='full', tol=0.001, reg_covar=0.001, max_iter=100, n_init=1,means_init=ms)
    gm.fit(np.concatenate([train3,test3],axis = 0))
    oof[idx1] = np.sum(gm.predict_proba(train3)[:,:3], axis = 1)
    preds[idx2] += np.sum(gm.predict_proba(test3)[:,:3], axis = 1)
    #if i==10:break 
    #print(roc_auc_score(train2['target'], oof[idx1]))
    #break

# PRINT CV AUC
auc = roc_auc_score(train['target'],oof)
print('QDA scores CV =',round(auc,5))





oof = np.zeros(len(train))
preds2 = np.zeros(len(test))

for i in tqdm(range(512)):
    # ONLY TRAIN WITH DATA WHERE WHEEZY EQUALS I
    train2 = train[train['wheezy-copper-turtle-magic']==i]
    test2 = test[test['wheezy-copper-turtle-magic']==i]
    idx1 = train2.index; idx2 = test2.index
    train2.reset_index(drop=True,inplace=True)
    
    # FEATURE SELECTION (USE APPROX 40 OF 255 FEATURES)
    # IMPORTANT: SCALER ARE NEEDED FOR KMEANS
    pipe = Pipeline([('vt', VarianceThreshold(threshold=2)), ('scaler', StandardScaler())])
    train3 = pipe.fit_transform(train2[cols])
    test3 = pipe.fit_transform(test2[cols])   

    # STRATIFIED K-FOLD
#    skf = StratifiedKFold(n_splits=5, random_state=42, shuffle=True)
#    for train_index, test_index in skf.split(train3, train2['target']):
        
        # MODEL AND PREDICT WITH GMM
    ms, ps = get_mean_cov2(train3,train2['target'].values)
    gm = GaussianMixture(n_components=6, init_params='random', covariance_type='full', tol=0.001, reg_covar=0.001, max_iter=100, n_init=1,means_init=ms, 
                         precisions_init=ps)
    #gm = GaussianMixture(n_components=6, init_params='random', covariance_type='full', tol=0.001, reg_covar=0.001, max_iter=100, n_init=1,means_init=ms)
    gm.fit(np.concatenate([train3,test3],axis = 0))
    oof[idx1] = np.sum(gm.predict_proba(train3)[:,:3], axis = 1)
    preds2[idx2] += np.sum(gm.predict_proba(test3)[:,:3], axis = 1)
    #print(roc_auc_score(train2['target'], oof[idx1]))
    #break
# PRINT CV AUC
auc = roc_auc_score(train['target'],oof)
print('QDA scores CV =',round(auc,5))








oof = np.zeros(len(train))
preds3 = np.zeros(len(test))

for i in tqdm(range(512)):
    # ONLY TRAIN WITH DATA WHERE WHEEZY EQUALS I
    train2 = train[train['wheezy-copper-turtle-magic']==i]
    test2 = test[test['wheezy-copper-turtle-magic']==i]
    idx1 = train2.index; idx2 = test2.index
    train2.reset_index(drop=True,inplace=True)
    
    # FEATURE SELECTION (USE APPROX 40 OF 255 FEATURES)
    # IMPORTANT: SCALER ARE NEEDED FOR KMEANS
    pipe = Pipeline([('vt', VarianceThreshold(threshold=2)), ('scaler', StandardScaler())])
    train3 = pipe.fit_transform(train2[cols])
    test3 = pipe.fit_transform(test2[cols])   

    # STRATIFIED K-FOLD
#    skf = StratifiedKFold(n_splits=5, random_state=42, shuffle=True)
#    for train_index, test_index in skf.split(train3, train2['target']):
        
        # MODEL AND PREDICT WITH GMM
    ms, ps = get_mean_cov(train3,train2['target'].values)
    gm = GaussianMixture(n_components=6, init_params='kmeans', covariance_type='full', tol=0.001, reg_covar=0.001, max_iter=100, n_init=1,means_init=ms, 
                         precisions_init=ps)
    #gm = GaussianMixture(n_components=6, init_params='random', covariance_type='full', tol=0.001, reg_covar=0.001, max_iter=100, n_init=1,means_init=ms)
    gm.fit(np.concatenate([train3,test3],axis = 0))
    oof[idx1] = np.sum(gm.predict_proba(train3)[:,:3], axis = 1)
    preds3[idx2] += np.sum(gm.predict_proba(test3)[:,:3], axis = 1)
    #print(roc_auc_score(train2['target'], oof[idx1]))
    #break
# PRINT CV AUC
auc = roc_auc_score(train['target'],oof)
print('QDA scores CV =',round(auc,5))








oof = np.zeros(len(train))
preds4 = np.zeros(len(test))

for i in tqdm(range(512)):
    # ONLY TRAIN WITH DATA WHERE WHEEZY EQUALS I
    train2 = train[train['wheezy-copper-turtle-magic']==i]
    test2 = test[test['wheezy-copper-turtle-magic']==i]
    idx1 = train2.index; idx2 = test2.index
    train2.reset_index(drop=True,inplace=True)
    
    # FEATURE SELECTION (USE APPROX 40 OF 255 FEATURES)
    # IMPORTANT: SCALER ARE NEEDED FOR KMEANS
    pipe = Pipeline([('vt', VarianceThreshold(threshold=2)), ('scaler', StandardScaler())])
    train3 = pipe.fit_transform(train2[cols])
    test3 = pipe.fit_transform(test2[cols])   

    # STRATIFIED K-FOLD
#    skf = StratifiedKFold(n_splits=5, random_state=42, shuffle=True)
#    for train_index, test_index in skf.split(train3, train2['target']):
        
        # MODEL AND PREDICT WITH GMM
    ms, ps = get_mean_cov2(train3,train2['target'].values)
    gm = GaussianMixture(n_components=6, init_params='kmeans', covariance_type='full', tol=0.001, reg_covar=0.001, max_iter=100, n_init=1,means_init=ms, 
                         precisions_init=ps)
    #gm = GaussianMixture(n_components=6, init_params='random', covariance_type='full', tol=0.001, reg_covar=0.001, max_iter=100, n_init=1,means_init=ms)
    gm.fit(np.concatenate([train3,test3],axis = 0))
    oof[idx1] = np.sum(gm.predict_proba(train3)[:,:3], axis = 1)
    preds4[idx2] += np.sum(gm.predict_proba(test3)[:,:3], axis = 1)
    #print(roc_auc_score(train2['target'], oof[idx1]))
    #break
# PRINT CV AUC
auc = roc_auc_score(train['target'],oof)
print('QDA scores CV =',round(auc,5))






oof = np.zeros(len(train))
preds5 = np.zeros(len(test))

for i in tqdm(range(512)):
    # ONLY TRAIN WITH DATA WHERE WHEEZY EQUALS I
    train2 = train[train['wheezy-copper-turtle-magic']==i]
    test2 = test[test['wheezy-copper-turtle-magic']==i]
    idx1 = train2.index; idx2 = test2.index
    train2.reset_index(drop=True,inplace=True)
    
    # FEATURE SELECTION (USE APPROX 40 OF 255 FEATURES)
    # IMPORTANT: SCALER ARE NEEDED FOR KMEANS
    pipe = Pipeline([('vt', VarianceThreshold(threshold=2)), ('scaler', StandardScaler())])
    train3 = pipe.fit_transform(train2[cols])
    test3 = pipe.fit_transform(test2[cols])   

    # STRATIFIED K-FOLD
#    skf = StratifiedKFold(n_splits=5, random_state=42, shuffle=True)
#    for train_index, test_index in skf.split(train3, train2['target']):
        
        # MODEL AND PREDICT WITH GMM
    ms, ps = get_mean_cov3(train3,train2['target'].values)
    gm = GaussianMixture(n_components=6, init_params='random', covariance_type='full', tol=0.001, reg_covar=0.001, max_iter=100, n_init=1,means_init=ms, 
                         precisions_init=ps)
    #gm = GaussianMixture(n_components=6, init_params='random', covariance_type='full', tol=0.001, reg_covar=0.001, max_iter=100, n_init=1,means_init=ms)
    gm.fit(np.concatenate([train3,test3],axis = 0))
    oof[idx1] = np.sum(gm.predict_proba(train3)[:,:3], axis = 1)
    preds5[idx2] += np.sum(gm.predict_proba(test3)[:,:3], axis = 1)
    #print(roc_auc_score(train2['target'], oof[idx1]))
    #break
# PRINT CV AUC
auc = roc_auc_score(train['target'],oof)
print('QDA scores CV =',round(auc,5))






oof = np.zeros(len(train))
preds6 = np.zeros(len(test))

for i in tqdm(range(512)):
    # ONLY TRAIN WITH DATA WHERE WHEEZY EQUALS I
    train2 = train[train['wheezy-copper-turtle-magic']==i]
    test2 = test[test['wheezy-copper-turtle-magic']==i]
    idx1 = train2.index; idx2 = test2.index
    train2.reset_index(drop=True,inplace=True)
    
    # FEATURE SELECTION (USE APPROX 40 OF 255 FEATURES)
    # IMPORTANT: SCALER ARE NEEDED FOR KMEANS
    pipe = Pipeline([('vt', VarianceThreshold(threshold=2)), ('scaler', StandardScaler())])
    train3 = pipe.fit_transform(train2[cols])
    test3 = pipe.fit_transform(test2[cols])   

    # STRATIFIED K-FOLD
#    skf = StratifiedKFold(n_splits=5, random_state=42, shuffle=True)
#    for train_index, test_index in skf.split(train3, train2['target']):
        
        # MODEL AND PREDICT WITH GMM
    ms, ps = get_mean_cov3(train3,train2['target'].values)
    gm = GaussianMixture(n_components=6, init_params='kmeans', covariance_type='full', tol=0.001, reg_covar=0.001, max_iter=100, n_init=1,means_init=ms, 
                         precisions_init=ps)
    #gm = GaussianMixture(n_components=6, init_params='random', covariance_type='full', tol=0.001, reg_covar=0.001, max_iter=100, n_init=1,means_init=ms)
    gm.fit(np.concatenate([train3,test3],axis = 0))
    oof[idx1] = np.sum(gm.predict_proba(train3)[:,:3], axis = 1)
    preds6[idx2] += np.sum(gm.predict_proba(test3)[:,:3], axis = 1)
    #print(roc_auc_score(train2['target'], oof[idx1]))
    #break
# PRINT CV AUC
auc = roc_auc_score(train['target'],oof)
print('QDA scores CV =',round(auc,5))





# SUBMIT
sub = pd.read_csv('../input/sample_submission.csv')
sub['target'] = (preds+preds2+preds3+preds4+preds5+preds6)/6
sub.to_csv('submission.csv',index=False)
