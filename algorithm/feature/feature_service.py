from algorithm.feature import statistical_feature
from algorithm.feature import fitting_feature

def extract_features(time_series):
    s_features = statistical_feature.get_statistical_features(time_series)
    f_features = fitting_feature.get_fitting_features(time_series)
    features = s_features + f_features
    return features
