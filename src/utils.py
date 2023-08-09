from jdatetime import datetime


def generate_today_panel_image_file_name():
    return f"./panels/Average-panel-{datetime.now().strftime('%Y-%m-%d')}.png"