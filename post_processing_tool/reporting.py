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
        template_dir:str="./templates"
) -> str:
    template = Environment(
        loader=FileSystemLoader(template_path)
    ).get_template(template_path)

    report = template.render(context)

    return report


def generate_location_dist(df: DataFrame) -> str:
    plt.cla()
    df = df["CITY"].dropna().str.upper().value_counts().nlargest(10)
    plt.bar(range(len(df)), df.values, align='center')
    plt.xticks(range(len(df)), df.index.values, size='small', rotation=45, color='black')
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


def generate_report(df: DataFrame) -> Dict[str, str]:
    location_dif = generate_location_dist(df)
    format_fig = generate_format_dist(df)

    


def fig_to_base64(plt) -> str:
    imgBytes = io.BytesIO()
    plt.savefig(imgBytes, format='jpg')
    imgBytes.seek(0)
    b64Img = base64.b64encode(imgBytes.read()).decode()

    return b64Img