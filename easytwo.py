"""
Usage: easytwo [OPTIONS]

  Easy EC2 Queries.

Options:
  --id TEXT
  --name NAME
  --az AZ
  --state STATE
  --type TYPE
  --vpc VPC
  --ami AMI
  --public-ip PUBLIC-IP
  --private-ip PRIVATE-IP
  --tag TAG VALUE
  --output [id|az|state|type|public-ip|private-ip|ami|vpc|subnet]
  --help
"""

import click
import boto3
import botocore

import extractors


INPUTS = {
    "private-ip": "private-ip-address",
    "public-ip": "ip-address",
    "ami": "image-id",
    "subnet": "subnet-id",
    "vpc": "vpc-id",
    "type": "instance-type",
    "state": "instance-state-name",
    "az": "availability-zone",
    "name": "tag:Name",
}

OUTPUTS = {
    "id": extractors.default("instance_id"),
    "name": extractors.tag("Name"),
    "az": extractors.az,
    "state": extractors.state,
    "type": extractors.default("instance_type"),
    "public-ip": extractors.default("public_ip_address"),
    "private-ip": extractors.default("private_ip_address"),
    "launch-time": extractors.launch_time,
    "ami": extractors.default("image_id"),
    "vpc": extractors.default("vpc_id"),
    "subnet": extractors.default("subnet_id"),
}

DEFAULT_OUTPUT_VALUE = "none"


def add_input_options(func):
    """Decorate command to add dynamic options."""

    output_choice = click.Choice(OUTPUTS.keys())

    func = click.option("--output", multiple=True, type=output_choice)(func)
    func = click.option("--tag", metavar="TAG VALUE", nargs=2, multiple=True)(func)
    func = click.option(
        "--state",
        default=["running"],
        multiple=True,
        help="Instance State, defaults to running.",
    )(func)

    for k in INPUTS:
        func = click.option("--{}".format(k), metavar=k.upper(), multiple=True)(func)

    return click.option("--id", multiple=True)(func)


@click.command()
@add_input_options
def main(**kwargs):
    """Easy EC2 Queries."""

    output = kwargs.pop("output") or ("id",)

    instance_ids = kwargs.pop("id")
    filters = tuple(format_filters(kwargs))

    if len(filters) == 0 and len(instance_ids) == 0:
        show_help_and_exit()

    try:
        instances = boto3.resource("ec2").instances.filter(
            InstanceIds=instance_ids, Filters=filters
        )

        for instance in instances:
            click.echo(" ".join(format_output(instance, output)))
    except botocore.exceptions.ClientError as e:
        click.echo(e)


def show_help_and_exit():
    """Show help and quit."""

    ctx = click.get_current_context()
    click.echo(ctx.get_help())
    ctx.exit()


def format_filters(filters):
    """Convert filters to boto3 format."""

    for tag_name, tag_value in filters.pop("tag"):
        yield dict(Name="tag:{}".format(tag_name), Values=(tag_value,))

    for field, value in filters.items():
        if value == tuple():
            continue

        yield dict(Name=INPUTS[field.replace("_", "-")], Values=value)


def format_output(instance, outputs):
    """Extract and yield outputs for an instance."""

    for output in outputs:
        yield OUTPUTS[output](instance) or DEFAULT_OUTPUT_VALUE
