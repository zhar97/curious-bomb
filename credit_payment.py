from pandas import date_range, DataFrame, Series
from numpy import nan
from datetime import datetime, timedelta
from matplotlib.pyplot import show, ylim, legend
from sys import argv
params = {param.lstrip('-'): argv[pos+1] for pos, param in enumerate(argv[1:], start=1) if param.startswith('-')}
def simulate_min_credit_payment(
    outstanding, 
    min_ratio=0.05, 
    interest_pa=0.18
):
    _outstanding = outstanding
    day = datetime.today()
    total_payment_expected = int(1.0*min_ratio**(-1))
    total_payment = 0
    sim_df = DataFrame(
        data=[[outstanding, nan]],
        columns=['outstanding', 'paid'],
        index=Series(
            data=[day - timedelta(days=1)], 
            name='date'
        )
    )
    while day:
        if day.day == datetime.today().day:
            try:
                to_pay = round(
                    outstanding*(total_payment_expected-total_payment)**(-1), 
                    2
                )
            except ZeroDivisionError:
                break
            outstanding -= to_pay
            total_payment += 1
        else:
            to_pay = nan
        if outstanding < 0:
            outstanding = 0
        outstanding *= 1 + interest_pa*(day.replace(year=day.year+1) - day).days**(-1)
        sim_df.loc[day] = [round(outstanding, 2), to_pay]
        if round(outstanding, 2) <= 0:
            break
        day += timedelta(days=1)
    sim_df['paid'] = sim_df['paid'].cumsum()
    return sim_df, round(sim_df['paid'].iloc[-1] - _outstanding, 2), sim_df.index.max() - sim_df.index.min()
simulation = simulate_min_credit_payment(
    outstanding=float(params.get('outstanding', 1000)), 
    min_ratio=float(params.get('min_ratio', 0.05)),
    interest_pa=float(params.get('interest_pa', 0.18))
)
simulation[0].resample(rule='M', kind='period')['outstanding'].min().plot()
simulation[0].resample(rule='M', kind='period')['paid'].max().plot()
ylim([0, simulation[0].resample(rule='M', kind='period')['paid'].max().max()])
legend()
print('total interest is', simulation[1], 'for', simulation[2])
if params.get('save'):
    if not params.get('save').upper in ('FALSE', '0'):
        simulation[0].to_csv(params.get('save'))
    else:
        show()
else:
    show()