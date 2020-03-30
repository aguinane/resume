import logging
from pathlib import Path
import shutil
import json
import pdfkit
from jinja2 import Environment, FileSystemLoader
import colander
from jsonresume.schema.resume import Resume as ResumeSchema


env = Environment(loader=FileSystemLoader("templates"))


def main():
    json_file = open("data/resume.json", "r")
    resume_data = json.load(json_file)
    validate_json_format(resume_data)
    template = env.get_template("resume.html")
    output_html = template.render(**resume_data)
    Path("build").mkdir(exist_ok=True)
    with open("build/resume.html", "w", encoding="utf-8") as fh:
        fh.write(output_html)
    copy_static_data()
    logging.info("Created html!")
    pdfkit.from_file("build/resume.html", "build/resume.pdf")


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
