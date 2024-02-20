# this module is used for training NN
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd
import random
import numpy as np

df=pd.read_csv('outcomes.csv')
# scores happened to not be registered sometimes
# df = df.dropna(subset=['score'])
# df.to_csv('outcomes.csv',index=False)

# nn finally were trained without accomodating for a draw possibility (indicated as 0)
df = df[df['score'] != 0]

x=df.drop(columns=['score'])
y=df['score']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2,random_state=73)

# Create an MLPRegressor
mlp_regressor = MLPRegressor(hidden_layer_sizes=(200), max_iter=2000, solver='lbfgs')

# Train the model
mlp_regressor.fit(X_train, y_train)

# Make predictions on the test set
predictions = mlp_regressor.predict(X_test)

# Evaluate the model using mse as evaluation
mse = mean_squared_error(y_test, predictions)
print()
print(f'MSE: {mse}')
# for this model mse: 0.0011633

#saving the model
import joblib

joblib.dump(mlp_regressor, 'mlp_regressor_model_lbgs1_nodraw.joblib')
