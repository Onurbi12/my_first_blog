# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.files import File

import re
import os
import pandas as pd
from bs4 import BeautifulSoup
from colour import Color


template_name = ""
csv_filename = "donn\xe9e_tracking.csv"


from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string

from weasyprint import HTML, CSS


def templates():
    """Get the existing html templates in donnée_tracking.csv."""
    folder_path = os.path.dirname(os.path.abspath(__file__))
    csv_data = os.path.join(folder_path, "data", csv_filename)
    df = pd.read_csv(csv_data, delimiter=";", encoding="utf-8")
    df = df.drop_duplicates(subset="Nom du template")
    templates = []
    temp_nb = 0
    for template in df["Nom du template"]:
        temp_nb += 1
        templates.append((template, temp_nb))
    return templates


def data_prep():
    """Get the urls and click percent from one particular template."""
    global template_name
    folder_path = os.path.dirname(os.path.abspath(__file__))
    csv_data = os.path.join(folder_path, "data", csv_filename)
    df = pd.read_csv(csv_data, delimiter=";")
    df = df[df["Nom du template"] == template_name.encode("utf-8")]
    df = df.drop_duplicates(subset="lien cliquer")

    links_clics = df[["lien cliquer", "total clique"]]
    links_clics["percent_clics"] = (
        links_clics["total clique"] * 100 / links_clics["total clique"].sum()
    )
    url_list = []
    percent_list = []
    for url in links_clics["lien cliquer"]:
        url_list.append(url)
        percent_list.append(
            int(
                links_clics["percent_clics"][
                    links_clics["lien cliquer"] == url
                ]
            )
        )
        max_pct = max(percent_list)
    sorted_list = sorted(zip(url_list, percent_list), key=lambda x: x[1])
    return [sorted_list, max_pct]


def color_span():
    """Create hexadecimal color span for data vizualization."""
    red = Color("red")
    colors = list(red.range_to(Color("green"), data_prep()[1]))
    colors_hex = []
    for color in colors:
        colors_hex.append(color.hex_l)
    return colors_hex


def diameter_size(pct):
    """Limit diameter size between 25 and 125px."""
    return pct + 25


def new_html():
    """Modify the html template for data vizualization."""
    global template_name
    folder_path = os.path.dirname(os.path.abspath(__file__))
    html_template = os.path.join(folder_path, "templates/blog", template_name)
    with open(html_template, "r",) as html_t:
        html_test = File(html_t)
        html_string = html_test.read()

    link_nb = 0
    colors_hex = color_span()

    for url, pct in data_prep()[0]:
        diameter = diameter_size(pct)
        link_nb += 1
        new_string = re.sub(
            r'(<a href="{}".*?>.*?</a>)'.format(url),
            r'\1<div class="url{}">{}%</div>'.format(link_nb, pct),
            html_string,
            flags=re.MULTILINE | re.DOTALL,
        )

        soup = BeautifulSoup(new_string, features="html.parser")
        soup.style.append(
            """.url{} {{
            height: {}px;
            width: {}px;
            background-color: {};
            border-radius: 50%;
            display: inline-block;
            line-height: {}px;
            text-align: center;
            vertical-align: middle;
            color: {};}}
        """.format(
                link_nb,
                diameter,
                diameter,
                colors_hex[pct - 1],
                diameter,
                colors_hex[pct - 1],
            )
        )
        soup.style.append(
            """.url{}:hover {{
            height: {}px;
            width: {}px;
            background-color: {};
            border-radius: 50%;
            display: inline-block;
            line-height: {}px;
            text-align: center;
            vertical-align: middle;
            color: black;
            font-weight: bold;}}
        """.format(
                link_nb,
                diameter,
                diameter,
                colors_hex[pct - 1],
                diameter,
                colors_hex[pct - 1],
            )
        )
        html_string = str(soup)
    return html_string


def main_page(request):
    """Render main page."""
    temp_list = templates()
    return render(request, "blog/base.html", {"templates": temp_list})


def akema_temp(request, temp_nb):
    """Render modified html template."""
    global template_name
    template_name, _ = templates()[int(temp_nb) - 1]

    folder_path = os.path.dirname(os.path.abspath(__file__))
    new_template = os.path.join(folder_path, "templates/blog/result.html")
    with open(new_template, "w") as html_t:
        html_test = File(html_t)
        html_test.write(new_html())

    return render(request, "blog/result.html")


def html_to_pdf_view(request):
    html_string = render_to_string("blog/result.html")

    html = HTML(string=html_string)
    html.write_pdf(
        target="blog/mypdf.pdf",
        stylesheets=[
            CSS(
                string="""@page {
    size: A4;
    margin: 0in 1.44in 0.2in 0.44in;
}"""
            )
        ],
    )

    fs = FileSystemStorage("blog")
    with fs.open("mypdf.pdf") as pdf:
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
        return response
