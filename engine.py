from datetime import date

import adal
import requests

from config_parser import *


def get_access_token(config):
    context = adal.AuthenticationContext(authority=config['app_details']['authority_url'],
                                         validate_authority=True,
                                         api_version=None)
    token = context.acquire_token_with_username_password(resource=config['app_details']['resource_url'],
                                                         client_id=config['app_details']['client_id'],
                                                         username=config['powerbi']['username'],
                                                         password=config['powerbi']['password'])
    access_token = token.get('accessToken')
    return access_token


def get_response(url, header):
    response = requests.get(url=url, headers=header)
    r_status_code = response.status_code

    return (r_status_code, response)


def report_export_validator(group_name, group_dict, header):
    if len(group_dict['value']) > 0:
        for report in group_dict['value']:
            report_id = report['id']
            report_name = report['name']
            report_type = report['reportType']
            # chceck if it's powerbi report ------!!
            if report_type == 'PowerBIReport':
                export_pbix(group_name, report_id, report_name, header)
            else:
                print(f'{report_name} is not PowerBI Report..!!')
                continue
    else:
        print(f'No Reports Found in {group_name} workspace.')


def export_pbix(group_name, report_id, report_name, header):
    report_export_url = config['APIs']['get_reports_api'] + f'/{report_id}/Export'

    export_status, export_response = get_response(report_export_url, header)

    if export_status:
        print(f'{report_name} Exported Successfully.')

        export_date = date.today().strftime("%b-%d-%Y")
        export_file_name = group_name + '-' + report_name + '-' + export_date + '.pbix'
        export_full_path = config['download_reports']['path'] + f"\\{export_file_name}"
        with open(export_full_path, 'wb') as outfile:
            outfile.write(export_response.content)
    else:
        print(f'{group_name}:{report_name} Export failed. Response code:{export_status}')
