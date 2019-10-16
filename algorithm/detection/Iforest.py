import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime
from os import listdir
import time,datetime
from esconn import esinteracton
from algorithm.TrainModel import TrainModel
from algorithm.model_setting import PATH
from algorithm.feature import feature_service
import pickle

class Iforest_class(TrainModel):
    def __init__(self,nodelists=None,metrics=None,train_start=None,train_end=None,test_start=None,test_end=None,nodename=None,modelname=None,
                 seed=42,timesteps=12*3,timefeature=-1):
        super(Iforest_class,self).__init__(nodelists,metrics,train_start,train_end,test_start,test_end,nodename,modelname)
        self.seed = seed
        self.timesteps = int(timesteps)
        self.timefeature = int(timefeature)
        self.path = PATH+self.modelname+'.sav'

    def create_train_data_onenode(self,nodename):
        """
        对单个node进行训练数据集构建
        :return:
        """
        starttime = int(round(time.mktime(self.train_start.timetuple())) * 1000)
        endtime = int(round(time.mktime(self.train_end.timetuple())) * 1000)
        mdata = esinteracton.search_bulk(index='search_ganglia',
                                         query_json=esinteracton.search_nodename_timestamp_queryjson(
                                             nodename=nodename, starttime=starttime, endtime=endtime,
                                             metrics=self.metrics))
        dfone = esinteracton.mdata_dataframe(mdata)
        dfone.dropna(axis=0, how='any', inplace=True)
        Train_Data = self.getTrainData(dfone)
        # Train_Data = np.array(Train_Data)
        return Train_Data

    def create_time_train_date_onenode(self,nodename):
        """
        提取了时序特征的训练集
        :param nodename:
        :return: DataFrame
        """
        starttime = int(round(time.mktime(self.train_start.timetuple())) * 1000)
        endtime = int(round(time.mktime(self.train_end.timetuple())) * 1000)
        dfone = esinteracton.search_nodename_timestamp_dataframe_miss(nodename=nodename,starttime=starttime,endtime=endtime,metrics=self.metrics)
        columns = dfone.columns.values.tolist()
        columns.remove('timestamp')
        columns.remove('nodename')
        trainlist = []
        for i in range(self.timesteps,len(dfone)):
            if(dfone.ix[i-self.timesteps:i].isnull().values.any()):
                pass
            else:
                tlist = []
                for colunm in columns:
                    tlist.extend(dfone.ix[i:i][colunm])
                    tlist.extend(feature_service.extract_features(dfone.ix[i-self.timesteps:i][colunm]))
                trainlist.append(tlist)
        Train_Data = np.array(trainlist)
        return Train_Data


    def create_train_data(self):
        if(self.timefeature == 1):
            Train_Data = self.create_time_train_date_onenode(self.nodelists[0])
            for nodename in self.nodelists[1:]:
                X = self.create_time_train_date_onenode(nodename)
                Train_Data = np.concatenate((Train_Data, X), axis=0)
        else:
            Train_Data = self.create_train_data_onenode(self.nodelists[0])
            for nodename in self.nodelists[1:]:
                X = self.create_train_data_onenode(nodename)
                Train_Data = np.concatenate((Train_Data,X),axis=0)
        return Train_Data

    def getTestTime(self,dataframe):
        """
        生成time的时间戳
        :param dataframe:
        :return:
        """
        time = dataframe['timestamp'].tolist()
        return time

    def create_test_data_onenode(self, nodename):
        starttime = int(round(time.mktime(self.test_start.timetuple())) * 1000)
        endtime = int(round(time.mktime(self.test_end.timetuple())) * 1000)
        mdata = esinteracton.search_bulk(index='search_ganglia',
                                         query_json=esinteracton.search_nodename_timestamp_queryjson(
                                             nodename=nodename, starttime=starttime, endtime=endtime,
                                             metrics=self.metrics))
        dfone = esinteracton.mdata_dataframe(mdata)
        df = pd.isnull(dfone)
        index = np.where(df)[0]
        columns = np.where(df)[1]
        for i in range(len(index)):
            notnan = index[i]
            while(np.isnan(dfone.ix[notnan,columns[i]]) and notnan>=0):
                notnan = notnan - 1
            if(notnan == -1):
                notnan = index[i]
                while(np.isnan(dfone.ix[notnan,columns[i]])):
                    notnan = notnan + 1
                dfone.ix[index[i], columns[i]] = dfone.ix[notnan, columns[i]]
            else:
                dfone.ix[index[i], columns[i]] = dfone.ix[notnan, columns[i]]
        Test_Data = self.getTestData(dfone)
        Test_Time = self.getTestTime(dfone)
        return Test_Data,Test_Time

    def create_time_test_data_onenode(self, nodename):
        starttime = int(round(time.mktime(self.test_start.timetuple())) * 1000)
        endtime = int(round(time.mktime(self.test_end.timetuple())) * 1000)
        mdata = esinteracton.search_bulk(index='search_ganglia',
                                         query_json=esinteracton.search_nodename_timestamp_queryjson(
                                             nodename=nodename, starttime=starttime, endtime=endtime,
                                             metrics=self.metrics))
        dfone = esinteracton.mdata_dataframe(mdata)
        df = pd.isnull(dfone)
        index = np.where(df)[0]
        columns = np.where(df)[1]
        #处理缺失值
        for i in range(len(index)):
            notnan = index[i]
            while (np.isnan(dfone.ix[notnan, columns[i]]) and notnan >= 0):
                notnan = notnan - 1
            if (notnan == -1):
                notnan = index[i]
                while (np.isnan(dfone.ix[notnan, columns[i]])):
                    notnan = notnan + 1
                dfone.ix[index[i], columns[i]] = dfone.ix[notnan, columns[i]]
            else:
                dfone.ix[index[i], columns[i]] = dfone.ix[notnan, columns[i]]

        Test_Time = self.getTestTime(dfone)[self.timesteps:]
        columns = dfone.columns.values.tolist()
        columns.remove('timestamp')
        columns.remove('nodename')
        trainlist = []
        for i in range(self.timesteps, len(dfone)):
            tlist = []
            for colunm in columns:
                tlist.extend(dfone.ix[i:i][colunm])
                tlist.extend(feature_service.extract_features(dfone.ix[i - self.timesteps:i][colunm]))
            trainlist.append(tlist)
        Test_Data = np.array(trainlist)
        return Test_Data, Test_Time

    def buildmodel(self):
        model = IsolationForest(n_estimators=100, max_samples=256, contamination=0.0001, behaviour='new', verbose=1,n_jobs=1,random_state=self.seed)
        return model

    def train(self,Train_data):
       model = self.buildmodel()
       model.fit(Train_data)
       self.save(model)
       return model

    def predict_test(self,model):
        if(self.timefeature == -1):
            Test_Data, Test_Time = self.create_test_data_onenode(nodename=self.nodename)
        else:
            Test_Data, Test_Time = self.create_time_test_data_onenode(nodename=self.nodename)
        Test_Data_Label = model.predict(Test_Data)
        predf = pd.DataFrame(Test_Data_Label, columns=['label'])
        print(len(predf))
        print(len(Test_Time))
        predf['timestamp'] = Test_Time
        return predf

    def load(self):
        model = pickle.load(open(self.path, 'rb'))
        return model

    def save(self,model):
        pickle.dump(model, open(self.path, 'wb'))

    def getTestData(self,dataframe):
        TestData = self.getTrainData(dataframe=dataframe)
        return TestData

    def predictres(self,model):
        predictresult = {}
        if (self.timefeature == -1):
            Test_Data, Test_Time = self.create_test_data_onenode(nodename=self.nodename)
        else:
            Test_Data, Test_Time = self.create_time_test_data_onenode(nodename=self.nodename)
        Test_Data_Label = model.predict(Test_Data)
        predf = pd.DataFrame(Test_Data_Label, columns=['label'])
        predf['timestamp'] = Test_Time
        print(predf[predf['label']==-1])
        predictresult['detdf'] = predf
        Test_Data_Score = list(model.score_samples(Test_Data) * -1)
        predictresult['Test_Data_Score'] = Test_Data_Score
        label = predf['label'].tolist()
        anomalylist = [i for i in range(len(label)) if label[i] == -1]
        predictresult['anomalylist'] = anomalylist
        return predictresult


    def anomalyscore(self, model):
        if(self.timefeature==-1):
            Test_Data, Test_Time = self.create_test_data_onenode(nodename=self.nodename)
        else:
            Test_Data, Test_Time = self.create_time_test_data_onenode(nodename=self.nodename)
        Test_Data_Score = list(model.score_samples(Test_Data)*-1)
        return Test_Data_Score

    def anomalylocation(self,model):
        predf = self.predict_test(model=model)
        label = predf['label'].tolist()
        anomalylist = [i for i in range(len(label)) if label[i] == -1]
        return anomalylist


