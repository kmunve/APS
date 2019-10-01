try:
    import cPickle as pickle
except ImportError:
    import pickle
    print("Using pickle instead of cPickle!")

# Load model
with open('knn_model.pck', 'rb') as f:
    nbrs = pickle.load(f)