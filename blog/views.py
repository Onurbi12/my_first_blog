# -*- coding: latin-1 -*-
from django.shortcuts import render, get_object_or_404
from django.core.files import File

# from .models import Post
# from django.utils import timezone
# from .forms import PostForm
# from django.shortcuts import redirect
import re
import os
import pandas as pd
from bs4 import BeautifulSoup
from colour import Color


def main_page(request):
    folder_path = os.path.dirname(os.path.abspath(__file__))
    csv_data = os.path.join(folder_path, "data/donnee_tracking.csv")
    df = pd.read_csv(csv_data, delimiter=";")
    df = df.drop_duplicates(subset="Nom du template")
    templates = []
    for template in df["Nom du template"]:
        templates.append(template)
    print(templates)
    return render(request, "blog/base.html", {"templates": templates})


def data_prep():
    folder_path = os.path.dirname(os.path.abspath(__file__))
    csv_data = os.path.join(folder_path, "data/donnee_tracking.csv")
    html_name = "différent_lien.html"
    df = pd.read_csv(csv_data, delimiter=";")
    df = df[df["Nom du template"] == html_name]
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
        max_pct = int(max(percent_list))
    sorted_list = sorted(zip(url_list, percent_list), key=lambda x: x[1])
    return [sorted_list, max_pct]


def new_html(request):
    folder_path = os.path.dirname(os.path.abspath(__file__))
    html_template = os.path.join(
        folder_path, "templates/blog/different_lien.html"
    )
    with open(html_template, "r",) as html_t:
        html_test = File(html_t)
        html_string = html_test.read()

    link_nb = 0

    red = Color("red")
    colors = list(red.range_to(Color("green"), data_prep()[1]))
    colors_hex = []
    for color in colors:
        colors_hex.append(color.hex_l)

    for url, pct in data_prep()[0]:
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
                pct * 2.5,
                pct * 2.5,
                colors_hex[pct - 1],
                pct * 2.5,
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
                pct * 2.5,
                pct * 2.5,
                colors_hex[pct - 1],
                pct * 2.5,
                colors_hex[pct - 1],
            )
        )
        print(link_nb, pct)
        html_string = str(soup)

    new_template = os.path.join(folder_path, "templates/blog/test2.html")
    with open(new_template, "w") as html_t:
        html_test = File(html_t)
        html_test.write(html_string)

    return render(request, "blog/test2.html")


# new_html()


def akema_temp(request):
    folder_path = os.path.dirname(os.path.abspath(__file__))
    html_template = os.path.join(folder_path, "templates/blog/test.html")
    with open(html_template, "r",) as html_t:
        html_test = File(html_t)
        html_string = html_test.read()

    new_string = re.sub(
        r"(<a.*?</a>)",
        r'<span class="url" style="background-color: red;">\1</span>',
        html_string,
        flags=re.MULTILINE | re.DOTALL,
    )

    new_template = os.path.join(folder_path, "templates/blog/test2.html")
    with open(new_template, "w",) as html_t:
        html_test = File(html_t)
        html_test.write(new_string)

    return render(request, "blog/test2.html")


def graphic(request):
    return render(request, "blog/test2.html")
