import pandas as pd


def read_remote_csv(csv_file_url: str) -> pd.DataFrame:
    """
    Reads a remote CSV file and returns a list of lists.
    """
    file_id = csv_file_url.split('/')[-2]
    download_link = 'https://drive.google.com/uc?export=download&id=' + file_id
    df = pd.read_csv(download_link, encoding='utf-16')

    return df


def read_remote_html(html_file_url: str) -> str:
    """
    Reads a remote HTML file and returns its content.
    """
    file_id = html_file_url.split('/')[-2]
    download_link = 'https://drive.google.com/uc?export=download&id=' + file_id
    df = pd.read_csv(download_link, encoding='utf-8')

    html = ''

    for element in df.values:
        html = html + element[0] + '\n'

    return html
