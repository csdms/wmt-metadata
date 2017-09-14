"""A hook for modifying parameter values read from the WMT client."""

from wmt.utils.hook import yaml_dump


max_sides = 8


def apply_boundary_condition(env, side='side1'):
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
    env['boundary_filename'] = env['_boundary_filename']

    sides = []
    for i in range(max_sides):
        name = 'side' + str(i+1)
        if env['_boundary_condition_' + name] != 'Off':
            sides.append(name)

    boundary_tags = {}
    for i, side in enumerate(sides):
        boundary_tags[side] = [i]
    env['dict_of_boundary_tags'] = str(boundary_tags)

    boundary_conditions = {}
    for side in sides:
        boundary_conditions[side] = apply_boundary_condition(env, side)
    env['dict_of_boundary_conditions'] = str(boundary_conditions)

    yaml_dump('_env.yaml', env)
