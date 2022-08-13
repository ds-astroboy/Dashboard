
from service_layer.services import *
from sklearn.linear_model import LinearRegression

def get_AI_service_monthly_secondary_sales_data():
    data = get_service_monthly_secondary_sales_data()
    # df = data[(data.Year_Month != "2106") & (data.Year_Month != "2107") & (data.Year_Month != "2108") & (data.Year_Month != "2109")]
    df = data
    reg = LinearRegression()
    reg.fit(df[['Year_Month']], df.SalesAmount)
    prediction_five_months = ['2208']
    prediction_five_integers = [{'Year_Month': 2208}]
    inputs_df = pd.DataFrame(prediction_five_integers)
    predicted_values = reg.predict(inputs_df)
    inputs_df['Year_Month'] = prediction_five_months
    inputs_df['SalesAmount'] = predicted_values
    inputs_df['Months'] = ['Aug']
    inputs_df['Years'] = ['2208']
    inputs_df['Month_Year'] = ['22 Aug']
    inputs_df['Colors'] = '#FFFF00'
    df['Colors'] = '#FF00FF'
    frames = [df, inputs_df]
    result_df = pd.concat(frames)
    return result_df


