from math import ceil


def execute(env):
    duration_in_years = ceil(float(env['_run_duration']) / 365.)
    env['_run_duration'] = str(int(duration_in_years))
