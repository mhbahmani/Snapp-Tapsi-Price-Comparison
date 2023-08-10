from jdatetime import datetime


def generate_today_panel_image_file_name(panel_id):
    return f"./panels/panel-{str(panel_id)}-{datetime.now().strftime('%Y-%m-%d')}.png"