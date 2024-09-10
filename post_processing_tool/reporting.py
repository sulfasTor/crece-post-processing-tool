import base64
import io
import os
from datetime import datetime
from typing import Dict

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

    return fig_to_base64(plt)


def generate_format_dist(df: DataFrame) -> str:
    plt.cla()
    df["IN_SITE"].hist(grid=False, color="black", width=0.7)
    plt.xlabel("Format")
    plt.ylabel("Frequency")
    plt.title("Format Frequency")

    return fig_to_base64(plt)


def generate_report(df: DataFrame, template_path) -> Dict[str, str]:
    location_b64_img = generate_location_dist(df)
    format_b64_img = generate_format_dist(df)

    context = {
        "syncIntervalWeeks": os.environ.get("CRECE_SYNC_INTERVAL_WEEKS", 2),
        "formatChartImg": format_b64_img,
        "citiesChartImg": location_b64_img,
    }
    report = render_template(context, template_path)
    return report


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