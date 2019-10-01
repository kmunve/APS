from sklearn import preprocessing
from sklearn.neighbors import NearestNeighbors

try:
    import cPickle as pickle
except ImportError:
    import pickle
    print("Using pickle instead of cPickle!")


# Load data
with open('knn_preprocessed.pck', 'rb') as f:
    X, y = pickle.load(f)

split_index = 300
X_train = X[:-split_index, :]
X_test = X[-split_index:, :]

y_train = y[:-split_index, :]
y_test = y[-split_index:, :]

print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)


# Normalize the other numeric features
scaler = preprocessing.StandardScaler().fit(X_train)
#scaler.transform(X_train)


# Apply k-nearest neighbor classification
nbrs = NearestNeighbors(n_neighbors=3, algorithm='ball_tree').fit(scaler.transform(X_train))


# Store model
with open('knn_model.pck', 'wb') as f:
    pickle.dump(nbrs, f)