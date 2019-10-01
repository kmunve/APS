from sklearn import preprocessing
from sklearn.neighbors import NearestNeighbors
from aps.similar_forecast.preprocessing import load_test_train_data

try:
    import cPickle as pickle
except ImportError:
    import pickle
    print("Using pickle instead of cPickle!")


X_train, y_train, X_test, y_test = load_test_train_data()

# Normalize the other numeric features
scaler = preprocessing.StandardScaler().fit(X_train)
#scaler.transform(X_train)


# Apply k-nearest neighbor classification
nbrs = NearestNeighbors(n_neighbors=3, algorithm='ball_tree').fit(scaler.transform(X_train))


# Store model
with open('knn_model.pck', 'wb') as f:
    pickle.dump((nbrs, scaler), f)
