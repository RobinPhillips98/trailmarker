def sync_failure(*args, **kwargs):
    raise Exception("forced failure")


async def async_failure(*args, **kwargs):
    raise Exception("forced failure")
