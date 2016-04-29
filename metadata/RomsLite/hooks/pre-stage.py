import os
import shutil


def execute(env):
    """Perform pre-stage tasks for running a component.

    Parameters
    ----------
    env : dict
      A dict of component parameter values from WMT.

    """
    env['number_of_steps'] = int(round(float(env['_run_duration']) /
                                       float(env['time_step'])))

    env['_update_time_step'] = float(env['_run_duration'])
