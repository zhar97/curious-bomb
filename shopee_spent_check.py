from requests import get
from sys import argv

headers = {
    'cookie': 'SPC_EC={SPC_EC}'.format(SPC_EC=argv[-1])
}

total = 0
order = 0
params = (('list_type', 4),)
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
            for value in details.values():
                if isinstance(value, dict) and value.get('info_card'):
                    print('found')
                    order_total = value['info_card']['final_total'] / 100000
                    total += order_total
                    order += 1
                    print(
                        order, ': ',
                        'RM ', total_order,
                        ' - ', 
                        value['info_card']['order_list_cards'][0]['items'][0]['name'],
                        sep=''
                    )
    offset = dat.get('next_offset', -1)

print('Calculation completed!')
print('GRAND TOTAL: RM', round(total * 100) / 100)
