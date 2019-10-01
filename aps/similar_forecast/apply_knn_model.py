from aps.similar_forecast.preprocessing import load_test_train_data

try:
    import cPickle as pickle
except ImportError:
    import pickle
    print("Using pickle instead of cPickle!")


X_train, y_train, X_test, y_test = load_test_train_data()

# Load model
with open('knn_model.pck', 'rb') as f:
    nbrs, scaler = pickle.load(f)


i = 254
distances, indices = nbrs.kneighbors(scaler.transform(X_test[i,:].reshape(1,-1)))
#print(y_pred, y_test[i])
print(distances, indices)
print("Input:")
print("Region: {}".format(y_test[i, :][0]), "Date: {}".format(y_test[i, :][2]))

print("\nSuggestions:")
for k in range(len(indices[0])):
    #print("Region: {}".format(y_train[indices[0][k], :][0]), "Date: {}".format(dt.datetime.fromtimestamp(y_train[indices[0][k], :][1])))
    print("Region: {}".format(y_train[indices[0][k], :][0]), "Date: {}".format(y_train[indices[0][k], :][2]))
