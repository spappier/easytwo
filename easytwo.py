'''
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
'''

import click
import boto3
import botocore


INPUTS = {
    'private-ip': 'private-ip-address',
    'public-ip': 'ip-address',
    'ami': 'image-id',
    'subnet': 'subnet-id',
    'vpc': 'vpc-id',
    'type': 'instance-type',
    'state': 'instance-state-name',
    'az': 'availability-zone',
    'name': 'tag:Name',
}

OUTPUTS = {
    'id': 'instance_id',
    'az': 'az',
    'state': 'state',
    'type': 'instance_type',
    'public-ip': 'public_ip_address',
    'private-ip': 'private_ip_address',
    'ami': 'image_id',
    'vpc': 'vpc_id',
    'subnet': 'subnet_id',
}


def add_input_options(func):
    '''Decorate command to add dynamic options.'''

    output_choice = click.Choice(OUTPUTS.keys())

    func = click.option('--output', multiple=True, type=output_choice)(func)
    func = click.option('--tag', metavar='TAG VALUE', nargs=2, multiple=True)(func)

    for k in INPUTS:
        func = click.option('--{}'.format(k), metavar=k.upper(), multiple=True)(func)

    return click.option('--id', multiple=True)(func)


@click.command()
@add_input_options
def main(**kwargs):
    '''Easy EC2 Queries.'''

    output = kwargs.pop('output') or ('id',)

    filters = tuple(format_filters(kwargs))

    if len(filters) == 0:
        show_help_and_exit()

    try:
        instances = boto3.resource('ec2').instances.filter(
            InstanceIds=kwargs.pop('id'),
            Filters=filters,
        )

        for instance in instances:
            click.echo(' '.join(format_output(instance, output)))

    except botocore.exceptions.ClientError as e:
        click.echo(e)


def show_help_and_exit():
    '''Show help and quit.'''

    ctx = click.get_current_context()
    click.echo(ctx.get_help())
    ctx.exit()


def format_filters(filters):
    '''Convert filters to boto3 format.'''

    for tag_name, tag_value in filters.pop('tag'):
        yield dict(Name='tag:{}'.format(tag_name), Values=(tag_value,))

    for field, value in filters.items():
        if value == tuple():
            continue

        yield dict(Name=INPUTS[field.replace('_', '-')], Values=value)


def format_output(instance, outputs):
    '''Extract and yield outputs for an instance.'''

    for output in outputs:
        if output == 'az':
            yield get_instance_az(instance)
        elif output == 'state':
            yield get_instance_state(instance)
        else:
            yield getattr(instance, OUTPUTS[output])


def get_instance_az(instance):
    '''Extract instance availability zone.'''

    return instance.placement['AvailabilityZone']


def get_instance_state(instance):
    '''Extract instance state name.'''

    return instance.state['Name']
