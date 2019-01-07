import fix_yahoo_finance as yf
from keras.models import Sequential
from keras.layers import LSTM, TimeDistributed,Dense,Dropout,Activation
from keras.optimizers import Adam
import numpy as np
from pandas_datareader import data as pdr
import csv
import time
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import math
import datetime

todays_date = str(datetime.datetime.today().strftime('%Y-%m-%d'))

class PredictionModel:
    def __init__(self,ticker):
        self.ticker = ticker

    def create_dataset(self,dataset, look_back=1):
        dataX, dataY = [], []
        for i in range(len(dataset)-look_back-1):
            a = dataset[i:(i+look_back), 0]
            dataX.append(a)
            dataY.append(dataset[i + look_back, 0])
        return np.array(dataX), np.array(dataY)

    def main(self):
        yf.pdr_override()
        data = pdr.get_data_yahoo(self.ticker, start="2017-01-01", end=todays_date)
        data.to_csv('haha.csv')

        dates = []
        closes = []
        with open('haha.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                date = row[0]
                close = row[4]

                dates.append(date)
                closes.append(close)

        dates.pop(0)
        closes.pop(0)
        new_closes= []
        for item in closes:
            new_closes.append(float(item))

        X_train = new_closes[0:len(new_closes)]

        X_train = np.array(X_train)

        data = X_train.reshape((len(X_train),1))
        
        
        today_price = data[len(data)-1,0]
        
        scaler = MinMaxScaler(feature_range=(0, 1))

        X_train = X_train.reshape((len(X_train),1))

        scaler = MinMaxScaler(feature_range=(0, 1))
        X_train = scaler.fit_transform(X_train)

        train_size = int(len(X_train) * 0.80)
        test_size = len(X_train) - train_size
        train, test = X_train[0:train_size,:], X_train[train_size:len(X_train),:]
        print(len(train), len(test))

        look_back = 1
        trainX, trainY = self.create_dataset(train, look_back)
        testX, testY = self.create_dataset(test, look_back)

        trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
        testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

        model = Sequential()
        model.add(LSTM(4, input_shape=(1, look_back)))
        model.add(Dense(1))

        model.compile(loss='mse', optimizer='adam')
        model.fit(trainX, trainY, epochs=10, batch_size=1, verbose=2)

        trainPredict = model.predict(trainX)
        testPredict = model.predict(testX)

        trainPredict = scaler.inverse_transform(trainPredict)
        trainY = scaler.inverse_transform([trainY])
        testPredict = scaler.inverse_transform(testPredict)
        testY = scaler.inverse_transform([testY])

        trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))

        testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))

        trainPredictPlot = np.empty_like(X_train )
        trainPredictPlot[:, :] = np.nan
        trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict

        testPredictPlot = np.empty_like(X_train )
        testPredictPlot[:, :] = np.nan
        testPredictPlot[len(trainPredict)+(look_back*2)+1:len(X_train )-1, :] = testPredict
        today_closing_price = X_train[X_train.shape[0]-1,:]

        today_closing_price=today_closing_price.reshape(1,1)
        today_closing_price = np.reshape(today_closing_price, (today_closing_price.shape[0], 1, today_closing_price.shape[1]))
        trainPredict_tomorrow= model.predict(today_closing_price)
        trainPredict_tomorrow= scaler.inverse_transform(trainPredict_tomorrow)

        return today_price , trainPredict_tomorrow

    def calculate_difference(self,today,tommorrow):
        total = (float(tommorrow) - float(today)) / 100
        return total

if __name__ == '__main__':
    ticker = input('Input Stock Ticker from Yahoo finance list: ')
    model = PredictionModel(ticker)
    today, tommorrow = model.main()
    total = model.calculate_difference(today,tommorrow)
    print("Today's closing price is: " + str(today) + '\n')
    print("Tommorrow's closing price prediction is " + str(tommorrow) + '\n')
    print('The percentage difference is: ' + str(total))
    print('If percentage difference is positive take as gain - Otherwise take as a loss')
