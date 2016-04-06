#!/usr/bin/env python

import io
import json
import yaml
import semver
import click
import logging
import tempfile
import os
import requests

options = {
    "dry_run": False,
    "human": True
}


def get_version():
    version = None

    for f in ["package.json", "bower.json"]:
        with io.open(f, "r") as jf:
            config = json.load(jf)

        vs = config["version"]
        if version is None:
            version = vs
        elif semver.compare(vs, version) > 0:
            if options["human"]:
                click.echo("{} had larger version. {} > {}".format(f, vs, version))
            version = vs

    for f in ["meta.yaml", "construct.yaml"]:
        with io.open(f, "r") as yf:
            config = yaml.load(yf)

        if "package" in config:
            vs = config["package"]["version"]
        else:
            vs = config["version"]

        if version is None:
            version = vs
        elif semver.compare(vs, version) > 0:
            if options["human"]:
                click.echo("{} had larger version. {} > {}".format(f, vs, version))
            version = vs

    return version


def write_version(version):
    if options["dry_run"]:
        if options["human"]:
            click.echo("Skipped write of version {} due to dry run flag.".format(version))  # noqa
        return False

    for f in ["package.json", "bower.json"]:
        with io.open(f, "r") as jf:
            config = json.load(jf)
        config["version"] = version

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tfh:
            tfp = tfh.name
            json.dump(config, tfh, indent=2)
        os.rename(tfp, f)

    for f in ["meta.yaml", "construct.yaml"]:
        with io.open(f, "r") as yf:
            config = yaml.load(yf)

        if "package" in config:
            config["package"]["version"] = version
        else:
            config["version"] = version

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tfh:
            tfp = tfh.name
            yaml.dump(config, tfh, default_flow_style=False)
        os.rename(tfp, f)


def update_meta_source(url, etag):
    with io.open("meta.yaml", "r") as yf:
        config = yaml.load(yf)

    config["source"]["url"] = url
    config["source"]["md5"] = etag
    config["source"]["fn"] = url.split("/")[-1]

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tfh:
        tfp = tfh.name
        yaml.dump(config, tfh, default_flow_style=False)
    os.rename(tfp, "meta.yaml")
    if options["human"]:
        click.echo("Updating source to md5 {}.".format(etag))
    else:
        click.echo(etag)


def get_pypi_hash(version):
    url = "https://pypi.python.org/packages/source/i/idigbio-media-appliance/idigbio-media-appliance-{}.tar.gz".format(version)
    r = requests.head(url)
    return (url, r.headers["ETag"].replace("\"", ""))


@click.group()
@click.option('--dry-run/--no-dry-run', default=False)
@click.option('--human/--no-human', default=True)
def version(**kwargs):
    options.update(kwargs)


@version.command()
def pypi():
    v = get_version()
    url, etag = get_pypi_hash(v)
    update_meta_source(url, etag)


@version.command()
def get():
    v = get_version()
    if options["human"]:
        click.echo("Package version is {}".format(v))
    else:
        click.echo(v)


@version.group()
def bump():
    pass


@bump.command()
def major():
    v = get_version()
    nv = semver.bump_major(v)
    if options["human"]:
        click.echo("{} -> {}".format(v, nv))
    else:
        click.echo(nv)
    write_version(nv)


@bump.command()
def minor():
    v = get_version()
    nv = semver.bump_minor(v)
    if options["human"]:
        click.echo("{} -> {}".format(v, nv))
    else:
        click.echo(nv)
    write_version(nv)


@bump.command()
def patch():
    v = get_version()
    nv = semver.bump_patch(v)
    if options["human"]:
        click.echo("{} -> {}".format(v, nv))
    else:
        click.echo(nv)
    write_version(nv)

if __name__ == '__main__':
    version()
