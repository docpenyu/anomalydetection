import numpy as np

def time_series_moving_average(x):
    """
    序列x三小时内，从半个小时到三个小时的滑动平均与序列中最后一个时间点(即异常点判断)的差值
    Returns the difference between the last element of x and the smoothed value after Moving Average Algorithm
    The Moving Average Algorithm is M_{n} = (x_{n-w+1}+...+x_{n})/w, where w is a parameter
    The parameter w is chosen in {1, 6, 11, 16, 21, 26, 31, 36, 41, 46} and the set of parameters can be changed.
    WIKIPEDIA: https://en.wikipedia.org/wiki/Moving_average
    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: list with float
    """
    x = x.tolist()
    temp_list = []
    for w in range(1, min(12*3, len(x)),6):
        temp = np.mean(x[-w:])
        temp_list.append(temp)
    return list(np.array(temp_list) - x[len(x)-1])


def time_series_weighted_moving_average(x):
    """
    序列x三小时内，从半个小时到三个小时的带权滑动平均与序列中最后一个时间点(即异常点判断)的差值
    Returns the difference between the last element of x and the smoothed value after Weighted Moving Average Algorithm
    The Moving Average Algorithm is M_{n} = (1*x_{n-w+1}+...+(w-1)*x_{n-1}+w*x_{n})/w, where w is a parameter
    The parameter w is chosen in {1, 6, 11, 16, 21, 26, 31, 36, 41, 46} and the set of parameters can be changed.
    WIKIPEDIA: https://en.wikipedia.org/wiki/Moving_average
    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: list with float
    """
    x = x.tolist()
    temp_list = []
    for w in range(1,min(12*3, len(x)), 6):
        w = min(len(x), w)  # avoid the case len(value_list) < w
        coefficient = np.array(range(1, w + 1))
        temp_list.append((np.dot(coefficient, x[-w:])) / float(w * (w + 1) / 2))
    return list(np.array(temp_list) - x[len(x)-1])


def time_series_exponential_weighted_moving_average(x):
    """
    序列x三小时内，从半个小时到三个小时的EWMA与序列中最后一个时间点(即异常点判断)的差值
    w is chosen in {0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9}
    Returns the difference between the last element of x and the smoothed value after Exponential Moving Average Algorithm
    The Moving Average Algorithm is s[i] = alpha * x[i] + (1 - alpha) * s[i-1], where alpha is a parameter
    The parameter w is chosen in {0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9} and the set of parameters can be changed.
    WIKIPEDIA: https://en.wikipedia.org/wiki/Exponential_smoothing
    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: list with float
    """
    x = x.tolist()
    temp_list = []
    for j in range(1, 10):
        alpha = j / 10.0
        s = [x[0]]
        for i in range(1, len(x)):
            temp = alpha * x[i] + (1 - alpha) * s[-1]
            s.append(temp)
        temp_list.append(s[-1] - x[len(x)-1])
    return list(temp_list)

def time_series_double_exponential_weighted_moving_average(x):
    """
    序列x三小时内，从半个小时到三个小时的DEWMA与序列中最后一个时间点(即异常点判断)的差值
    Returns the difference between the last element of x and the smoothed value after Double Exponential Moving Average Algorithm
    The Moving Average Algorithm is s[i] = alpha * x[i] + (1 - alpha) * (s[i-1] + b[i-1]), b[i] = gamma * (s[i] - s[i-1]) + (1 - gamma) * b[i-1]
    where alpha and gamma are parameters.
    The parameter alpha is chosen in {0.1, 0.3, 0.5, 0.7, 0.9} and the set of parameters can be changed.
    The parameter gamma is chosen in {0.1, 0.3, 0.5, 0.7, 0.9} and the set of parameters can be changed.
    WIKIPEDIA: https://en.wikipedia.org/wiki/Exponential_smoothing
    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: list with float
    """
    x = x.tolist()
    temp_list = []
    for j1 in range(1, 10, 2):
        for j2 in range(1, 10, 2):
            alpha = j1 / 10.0
            gamma = j2 / 10.0
            s = [x[0]]
            b = [(x[3] - x[0]) / 3]  # s is the smoothing part, b is the trend part
            for i in range(1, len(x)):
                temp1 = alpha * x[i] + (1 - alpha) * (s[-1] + b[-1])
                s.append(temp1)
                temp2 = gamma * (s[-1] - s[-2]) + (1 - gamma) * b[-1]
                b.append(temp2)
            temp_list.append(s[-1] - x[len(x)-1])
    return list(temp_list)



def get_fitting_features(x):
    fitting_features = []
    fitting_features.extend(time_series_moving_average(x))
    fitting_features.extend(time_series_weighted_moving_average(x))
    fitting_features.extend(time_series_exponential_weighted_moving_average(x))
    fitting_features.extend(time_series_double_exponential_weighted_moving_average(x))
    return fitting_features