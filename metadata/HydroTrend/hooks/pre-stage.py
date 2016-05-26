from math import ceil


def execute(env):
    duration_in_years = ceil(float(env['run_duration']) / 365.)
    env['run_duration'] = str(int(duration_in_years))
