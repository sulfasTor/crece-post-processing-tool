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
    df["CITY"].head()
    fig = None
    return fig_to_base64(fig)


def generate_online_dist(df: DataFrame) -> str:
    fig = None
    return fig_to_base64(fig)


def generate_report(df: DataFrame) -> Dict[str, str]:
    generate_location_dist(df)


def fig_to_base64(fig) -> str:
    imgBytes = io.BytesIO()
    fig.savefig(imgBytes, format='jpg')
    imgBytes.seek(0)
    b64Img = base64.b64encode(imgBytes.read()).decode()

    return b64Img