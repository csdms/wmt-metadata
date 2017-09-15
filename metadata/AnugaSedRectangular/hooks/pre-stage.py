"""A hook for modifying parameter values read from the WMT client."""

from wmt.utils.hook import yaml_dump


def apply_boundary_condition(env, side='left'):
    boundary = env['_boundary_condition_' + side].encode('utf-8')
    if boundary == 'Dirichlet':
        bc = []
        bc.append(boundary)
        bc.append(float(env['_bc_' + side + '_dirichlet_stage']))
        bc.append(float(env['_bc_' + side + '_dirichlet_x_momentum']))
        bc.append(float(env['_bc_' + side + '_dirichlet_y_momentum']))
    else:
        bc = boundary

    return bc


def execute(env):
    """Perform pre-stage tasks for running a component.

    Parameters
    ----------
    env : dict
      A dict of component parameter values from WMT.

    """
    boundary_conditions = {}
    boundaries = ['left', 'right', 'top', 'bottom']
    for side in boundaries:
        boundary_conditions[side] = apply_boundary_condition(env, side)
    env['dict_of_boundary_conditions'] = str(boundary_conditions)

    # For debugging
    yaml_dump('_env.yaml', env)
