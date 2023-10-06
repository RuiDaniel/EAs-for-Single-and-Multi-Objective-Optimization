import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV


def MLP_training(X_train, y_train):
    mlp_gs = MLPRegressor(max_iter=1000, verbose=False)
    parameter_space = {
        'regressor__activation': ['tanh', 'relu'],
        'regressor__solver': ['sgd', 'adam'],
        'regressor__alpha': [0.001, 0.05, 0.01],
        'regressor__learning_rate_init': [0.01, 0.1, 0.05],
        'regressor__learning_rate': ['constant', 'adaptive'],
        'regressor__hidden_layer_sizes': [(12,12,12),(10,10,10),(6,4,2), (4,5,4),(4,3,3),(8),(9,6),(8,7,6)]
    }
    
#   Size of Input layer = 5 > Size of Hidden layer  > Size of Output layer = 1
#   Size of Hidden layer = 2/3 Size of Input layer + Size of Output layer = 4
#   Size of Hidden layer < 2x Size of Input layer = 10

    # Create a pipeline with StandardScaler and MLPRegressor
    pipeline = Pipeline([
        ('scaler', StandardScaler()),  # Normalization step
        ('regressor', mlp_gs)  # MLPRegressor step
    ])

    clf = GridSearchCV(pipeline, parameter_space, n_jobs=-1, cv=5, verbose=False)
    clf.fit(X_train, y_train) # X is train samples and y is the corresponding labels

    print('Best parameters found:\n', clf.best_params_)
    
    return clf

def MLP_testing(clf, X_test, y_test): 
    y_true, y_pred = y_test , clf.predict(X_test)

    print('Results on the test set:')
    print('Mean Squared Error = {}'.format(mean_squared_error(y_true, y_pred)))
    print('Root Mean Squared Error = {}'.format(mean_absolute_error(y_true, y_pred)))
    print('Mean Absolute Error = {}'.format(mean_squared_error(y_true, y_pred, squared=False)))
    
    return y_pred
    
    
df = pd.read_csv('Proj1_TestS_GeneratedData.csv', encoding='utf-8')
# df = df.drop(columns=['V_MemoryUsage','V_ProcessorLoad','V_InpNetThroughput','V_OutNetThroughput','V_OutBandwidth','V_Latency', 'InpNetThroughput'])
# print(df)

y = (np.array(df['CLP_variation']))
# print(y)

X = (np.array(df))[:,:-1]

# print(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

X_train2 = X_train
X_test2 = X_test
# MemoryUsage:0,ProcessorLoad: 1,InpNetThroughput: 2,OutNetThroughput: 3,OutBandwidth: 4,Latency: 5
# V_MemoryUsage: 6,V_ProcessorLoad: 7,V_InpNetThroughput: 8,V_OutNetThroughput: 9,
# V_OutBandwidth: 10,V_Latency: 11,CLP_variation: 12


X_train = np.delete(X_train, [1,5,6,7,8,9,10],axis=1)
X_test = np.delete(X_test, [1,5,6,7,8,9,10],axis=1)

print(X_train)

clf = MLP_training(X_train, y_train)

ypred = MLP_testing(clf, X_test, y_test)

df2 = pd.DataFrame()
df2['MemoryUsage'] = X_test2[:,0]
df2['ProcessorLoad'] = X_test2[:,1]
df2['InpNetThroughput'] = X_test2[:,2]
df2['OutNetThroughput'] = X_test2[:,3]
df2['OutBandwidth'] = X_test2[:,4]
df2['Latency'] = X_test2[:,5]
df2['V_MemoryUsage'] = X_test2[:,6]
df2['V_ProcessorLoad'] = X_test2[:,7]
df2['V_InpNetThroughput'] = X_test2[:,8]
df2['V_OutNetThroughput'] = X_test2[:,9]
df2['V_OutBandwidth'] = X_test2[:,10]
df2['V_Latency'] = X_test2[:,11]
df2['CLP_variation'] = y_test
df2['CLPVariation_pred'] = ypred


df2.to_excel('MLP_Results.xlsx', index=False)
df2.to_csv('MLP_Results.csv', index=False, encoding='utf-8')
