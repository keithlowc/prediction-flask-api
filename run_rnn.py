from rnn import PredictionModel

def rq_test_func(ticker):
    model = PredictionModel(ticker.lower())
    today, tommorrow = model.main()
    difference = model.calculate_difference(today,tommorrow)
    return today, tommorrow, difference, ticker


# from rnn_new import PredictionModel

# def rq_test_func(ticker):
#     model = PredictionModel(ticker.lower())
#     today, tommorrow, date, original_data, total_test_predict = model.main()
#     difference = model.calculate_difference(today,tommorrow)
#     return today, tommorrow, difference, ticker, date, original_data, total_test_predict


