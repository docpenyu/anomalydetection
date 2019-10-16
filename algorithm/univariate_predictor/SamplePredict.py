from .swa import SWA_class
from .ewma import EWMA_class
from .linearregression import LR_class
from .arima import Arima_class
from .PredictModel import PredictModel

class SamplePredictRes:
    def __init__(self,predictmethond):
        self.predictmethod = predictmethond


    def predictres(self,**kwargs):
        e = PredictModel(**kwargs)

        if (self.predictmethod == 'MA'):
            e = SWA_class(**kwargs)

        elif (self.predictmethod == 'EWMA'):
            e = EWMA_class(**kwargs)

        elif (self.predictmethod == 'LR'):
            e = LR_class(**kwargs)

        elif (self.predictmethod == 'ARIMA'):
            e = Arima_class(**kwargs)

        e.createdata()
        predf = e.predict()
        return predf

