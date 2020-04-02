import logging
from pathlib import Path
import shutil
import json
import pdfkit
from jinja2 import Environment, FileSystemLoader
import colander
from dateutil.parser import parse
from jsonresume.schema.resume import Resume as ResumeSchema
import requests

env = Environment(loader=FileSystemLoader("templates"))


def main():
    # resume_data = json.load(open("data/resume.json", "r"))
    resume_data = download_json("aguinane", "5dc4e0eec034077b58fcf44add8e13c9")
    build_resume(resume_data)


def build_resume(resume_data: dict):
    validate_json_format(resume_data)
    env.filters["yearmonth"] = format_month
    template = env.get_template("resume.html")
    output_html = template.render(**resume_data)
    Path("build").mkdir(exist_ok=True)
    with open("build/resume.html", "w", encoding="utf-8") as fh:
        fh.write(output_html)
    copy_static_data()
    logging.info("Created html!")
    pdfkit.from_file("build/resume.html", "build/resume.pdf")


def download_json(user: str, gist_hash: str):
    """ Download resume.json github gist file"""
    filename = "resume.json"
    url = f"https://gist.githubusercontent.com/{user}/{gist_hash}/raw/{filename}"
    logging.info("Downloading %s", url)
    r = requests.get(url)
    r.raise_for_status()
    return r.json()


def format_month(value: str) -> str:
    try:
        dt = parse(value)
    except ValueError:
        return value
    month_desc = dt.strftime("%b %Y")
    return month_desc


def validate_json_format(resume_data):
    """ Validate schema """
    try:
        resume = ResumeSchema().deserialize(resume_data)
    except colander.Invalid:
        logging.exception("resume has invalid JSON format")
    else:
        logging.info("Resume structure: {}".format(resume))


def copy_static_data():
    """Copy static file"""

    shutil.copy("templates/bootstrap.min.css", "build/bootstrap.min.css")


if __name__ == "__main__":
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logger = logging.getLogger()  # Root Logger
    logging.basicConfig(level="INFO", format=LOG_FORMAT)
    main()
