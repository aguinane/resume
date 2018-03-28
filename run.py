from pathlib import Path
from collections import OrderedDict
import yaml
import pdfkit
import shutil
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))


def main():
    resume_data  = read_yaml('data/config.yaml')
    template = env.get_template('resume.html')
    output_html = template.render(**resume_data)
    with open("build/resume.html", "w", encoding='utf-8') as fh:
        fh.write(output_html)

    copy_static_data()
    pdfkit.from_file('build/resume.html', 'build/resume.pdf')

def read_yaml(filename):
    with open(filename, 'rt') as stream:
        return yaml.load(stream) or OrderedDict()


def copy_static_data():
    """Copy static file"""

    shutil.copy('templates/bootstrap.min.css', 'build/bootstrap.min.css')

if __name__ == '__main__':
    main()
