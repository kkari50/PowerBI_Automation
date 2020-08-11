from engine import *

access_token = get_access_token(config)
header = {'Authorization': f'Bearer {access_token}'}

# ----------My workspace--------------
my_group_r_Status, my_group_reports_response = get_response(config['APIs']['get_reports_api'], header)
my_group_reports_dict = my_group_reports_response.json()
my_group_name = 'My_Workspace'

report_export_validator(my_group_name, my_group_reports_dict, header)

# ---------Other workspaces-----------
group_response_code, group_response = get_response(config['APIs']['get_groups_api'], header)

groups_dict = group_response.json()

if len(groups_dict['value']) > 0:
    for group in groups_dict['value']:
        group_id = group['id']
        group_name = group['name']
        # get report details here--------!!
        reports_url = config['APIs']['get_groups_api'] + f'/{group_id}/reports'
        g_report_status_c, g_reports_response = get_response(reports_url, header)
        g_reports_dict = g_reports_response.json()

        report_export_validator(group_name, g_reports_dict, header)
