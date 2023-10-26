import functools


def default(key):
    """Gets a key from the instance."""

    def extract_attr(instance, key):
        return getattr(instance, key)

    return functools.partial(extract_attr, key=key)


def tag(tag):
    """Extract the value of a given tag for the instance object."""

    def extract_tag(instance, tag):
        try:
            return [d["Value"] for d in instance.tags if d["Key"] == tag][0]
        except (IndexError, TypeError):
            return DEFAULT_OUTPUT_VALUE

    return functools.partial(extract_tag, tag=tag)


def az(instance):
    """Extract instance availability zone."""

    return instance.placement["AvailabilityZone"]


def state(instance):
    """Extract instance state name."""

    return instance.state["Name"]


def launch_time(instance):
    """Extract and format instance launch time."""

    return instance.launch_time.strftime("%Y-%m-%dT%H:%M:%S")
