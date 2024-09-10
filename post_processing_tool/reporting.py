import base64
import io
import os
from datetime import datetime
from typing import Dict, List

from pandas import DataFrame
from jinja2 import Environment, FileSystemLoader
import matplotlib.pyplot as plt


def render_template(
        context:Dict,
        template_path:str,
        template_dir:str="./"
) -> str:
    template = Environment(
        loader=FileSystemLoader(template_dir)
    ).get_template(template_path)

    report = template.render(context)

    return report


def generate_location_dist(df: DataFrame) -> str:
    plt.cla()
    df = df["CITY"].dropna().str.upper().value_counts().nlargest(10)
    plt.bar(range(len(df)), df.values, align='center', color='black')
    plt.xticks(range(len(df)), df.index.values, size='small', rotation=45)
    plt.xlabel("Cities")
    plt.ylabel("Frequency")
    plt.title("Cities Frequency")

    return write_fig(plt, "format_cities_img.png")


def generate_format_dist(df: DataFrame) -> str:
    plt.cla()
    df["IN_SITE"].hist(grid=False, color="black", width=0.7)
    plt.xlabel("Format")
    plt.ylabel("Frequency")
    plt.title("Format Frequency")

    return write_fig(plt, "format_hist_img.png")


def get_stats(df: DataFrame) -> List:
    return [
        df.shape[0],
        df['last_changed'].min(),
        df['last_changed'].max()
    ]


def generate_report(df: DataFrame, template_path) -> Dict[str, str]:
    location_img_path = generate_location_dist(df)
    format_img_path = generate_format_dist(df)
    s = get_stats(df)

    context = {
        "syncIntervalWeeks": os.environ.get("CRECE_SYNC_INTERVAL_WEEKS", 2),
        "formatChartImgPath": format_img_path,
        "citiesChartImgPath": location_img_path,
        "numberSubscribers": s[0],
        "fromDate": s[1],
        "toDate": s[2],
    }
    report = render_template(context, template_path)
    return report


def write_fig(plt, fig_name) -> str:
    plt.savefig(fig_name)

    return fig_name


def fig_to_base64(plt) -> str:
    imgBytes = io.BytesIO()
    plt.savefig(imgBytes, format='jpg')
    imgBytes.seek(0)
    b64Img = base64.b64encode(imgBytes.read()).decode()

    return b64Img

def write_html(html, html_path):
    with open(html_path, 'w') as f:
        f.write(html)
    print(f"### Succesfully wrote HTML file to path: {html_path}")