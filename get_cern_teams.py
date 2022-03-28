from requests import get
from pandas import read_json, json_normalize, concat
from numpy import nan
from regex import compile as re_compile

cookies = {
    'LBLEVEL2': 'greybook-tomcat-prod-tomcat-0',
    'LBLEVEL1': 'k8s_ais_prod_b-Node2',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'DNT': '0',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://greybook.cern.ch/institute/list',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

for ipage in range(10):
    params = (('query', ''                 ),
              ('page' , str(ipage)         ),
              ('size' , '1000'             ),
              ('sort' , 'instituteName,asc'))

    response = read_json(get(
        'https://greybook.cern.ch/api/teams/search/search',
        headers=headers,
        params=params,
        cookies=cookies
    ).content)
    try:
        teams = concat([teams,
                        json_normalize(
                            response.loc['results', ['_embedded']]
                        ).T],
                        axis='index',
                        ignore_index=True,
                        copy=False)
    except NameError:
        teams = json_normalize(response.loc['results', ['_embedded']]).T
    if ipage == response.loc['totalPages', 'page'] - 1:
        break
teams.rename(columns={0: ''}, inplace=True)
teams = json_normalize(teams[''])
teams.replace({None: nan}, inplace=True)
teams.drop(index=teams.loc[teams['inGreybook']=='N'].index,
           columns=['_links.self.href',
                    'inGreybook'      ],
           inplace=True)
team_id = re_compile(r'https:\/\/greybook\.cern\.ch\/.*\/?teams\/(?P<team_id>\d+)')
teams['teamId'] = teams['_links.team.href'].apply(
    lambda link: int(team_id.match(link).group('team_id'))\
        if team_id.match(link) else nan
)
teams.set_index('teamId', inplace=True)
teams.sort_index(inplace=True)
uk_teams = teams.loc[
      teams['countryName'].isin(('United Kingdom',))
#     & (  teams['instituteName'].isin(('University of Leeds',
#                                       'University of Warwick',
#                                       'University of Sheffield',
#                                       'Lancaster University',
#                                       'University College London',
#                                       'Imperial College',
#                                       'Department of Physics and Astronomy UCL'))
#        | teams['instituteParentName'].isin(('University of Leeds',
#                                             'University of Warwick',
#                                             'University of Warwick ',
#                                             'University of Sheffield',
#                                             'Lancaster University',
#                                             'Lancaster University ',
#                                             'Imperial College')))
]
uk_teams.loc[:, ~uk_teams.isnull().all()].to_clipboard()

# University of Leeds;
# University of Warwick;
# University of Sheffield;
# Lancaster University;
# University College London | University of London ;
# Imperial College;
# Physics Department | Lancaster University ;
# Department of Physics and Astronomy UCL | University of London ;
# Department of Physics | University of Warwick ;