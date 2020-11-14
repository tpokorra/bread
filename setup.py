from setuptools import find_packages, setup


def readme():
    with open("README.rst") as f:
        return f.read()


setup(
    name="bread",
    version="0.1",
    description="basx Browse-Read-Edit-Add-Delete engine for django, reworked version",
    long_description=readme(),
    url="https://basx.dev",
    author="basx Software Development Co., Ltd.",
    author_email="info@basx.dev",
    license="Private",
    install_requires=[
        "Django",
        "python-dateutil",
        "django-crispy-forms",
        "django-filepreview @ hg+https://hg.basx.dev/pythonpackages/django-filepreview",
        "django-ckeditor",
        "django-model-utils",
        "django-extensions",
        "django-filter",
        "django-guardian",
        "django-dynamic-preferences",
        "django-dynamic-fixture",
        "django-compressor",
        "django-libsass",
        "django-markdown2",
        "django-countries",
        "django-money[exchange]",
        "pygraphviz",
        "Pillow",
        "easy_thumbnails",
        "django-image-cropping",
        "openpyxl",
        "WeasyPrint",
        "ffmpeg-python",
        "celery <5.0,>=4.4",
        "django-celery-results",
        "django-celery-beat",
        "Arpeggio",
    ],
    setup_requires=["setuptools_scm"],
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
)
