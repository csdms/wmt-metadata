"""A hook for modifying parameter values read from the WMT client."""

def execute(env):
    env['model_output__opt_time_interval'] = env['_update_time_step']
