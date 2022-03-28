from requests import get
from pandas import DataFrame, read_html, to_datetime
from numpy import float32
from datetime import datetime
from sys import argv

prices = read_html(get(
    'https://www.asnb.com.my/dpv2_thedisplay-printnewBM.php'
).content)[0]
prices.columns = [cols[0] for cols in prices.columns]
prices.drop(
    index=prices.loc[
        ~prices['NAB (RM)'].str.replace('.', '', regex=False)\
            .str.isnumeric()
    ].index,
    inplace=True
)
prices.reset_index(drop=True, inplace=True)
prices['NAB (RM)'] = prices['NAB (RM)'].astype(float32, copy=False)
prices.rename(columns={'PRODUK': 'Product',
                       'NAB (RM)': 'NAV (MYR)'},
              inplace=True)
prices['Date'] = datetime.today().date()
prices.sort_values(['Date', 'NAV (MYR)', 'Product'],
                   ascending=[False, True, True],
                   inplace=True)
portfolio = DataFrame(
    data=[['ASB'                , 1, 0.5*2*3**(-1)],
          ['ASN Sara 2'         , 1, 0.5*3**(-1)  ],
          ['ASM 3'              , 3, 0.25         ],
          ['ASN Imbang 3 Global', 3, 0.25         ]],
    columns=['Product', 'Package', 'Proportion']
)
portfolio['Proportion'] = portfolio['Proportion'].astype(float32,
                                                         copy=False)
portfolio = portfolio.merge(
    prices.drop_duplicates('Product', keep='first'),
    on='Product',
    copy=False
)
def get_funds_distribution(total_funds):
    portfolio['Funds (MYR)'] = portfolio['Proportion']\
                               * portfolio['NAV (MYR)']**(-1)\
                               * total_funds
    portfolio['Funds (MYR)'] = portfolio['Funds (MYR)']\
        .astype(int, copy=False)
    print(portfolio)
get_funds_distribution(float(argv[1]))