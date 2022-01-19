
from service_layer.services import *
from sklearn.linear_model import LinearRegression

def get_AI_service_monthly_secondary_sales_data():
    df = get_service_monthly_secondary_sales_data()
    reg = LinearRegression()
    reg.fit(df[['Year_Month']], df.SalesAmount)
    prediction_five_months = ['2113', '2114', '2115', '2116', '2117', '2118']
    prediction_five_integers = [{'Year_Month': 2113},
                                {'Year_Month': 2114},
                                {'Year_Month': 2115},
                                {'Year_Month': 2116},
                                {'Year_Month': 2117},
                                {'Year_Month': 2118}
                                ]
    inputs_df = pd.DataFrame(prediction_five_integers)
    predicted_values = reg.predict(inputs_df)
    inputs_df['Year_Month'] = prediction_five_months
    inputs_df['SalesAmount'] = predicted_values
    inputs_df['Months'] = ['Jan', 'Feb', "Mar", 'Apr', 'May', 'Jun']
    inputs_df['Years'] = ['2022', '2022', "2022", '2022', '2022', '2022']
    inputs_df['Month_Year'] = ['Jan 22', 'Feb 22', "Mar 22", 'Apr 22', 'May 22', 'Jun 22']
    inputs_df['Colors'] = '#FFFF00'
    df['Colors'] = '#FF00FF'
    frames = [df, inputs_df]
    result_df = pd.concat(frames)
    return result_df


