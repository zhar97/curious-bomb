from requests import get
from sys import argv

headers = {
    'cookie': 'SPC_EC={SPC_EC}'.format(SPC_EC=argv[-1])
}

totals = []
for list_type in (3, 4):
    total = 0
    order = 0
    params = (('list_type', list_type),)
    offset = 0

    while offset >= 0:
        response = get(
            'https://shopee.com.my/api/v4/order/get_order_list', 
            headers=headers, 
            params=params + (('offset', offset),)
        )
    
        dat = response.json()['data']
    
        if dat.get('details_list'):
            for details in dat['details_list']:
                if isinstance(details, dict) and details.get('info_card'):
                    order_total = details['info_card']['final_total'] / 100000
                    total += order_total
                    order += 1
                    print(
                        order, ': ',
                        'RM ', order_total,
                        ' - ', 
                        details['info_card']['order_list_cards'][0]['items'][0]['name'],
                        sep=''
                    )
        offset = dat.get('next_offset', -1)
    
    totals.append(total)
    print('TOTAL: RM', round(total, 2), 
          end=2*'\n')

print('Calculation Completed!')
print('GRAND TOTAL: RM', round(totals[0], 2), 
      '+ RM', round(totals[1], 2), '(refunded)')
