def build_header(col_name, val_len, default_len):
    num_spaces = val_len + default_len - (len(col_name) + 1)
    return '| ' + col_name + ' ' * num_spaces


def create_table(team_name, stats):
    """
    | Team             | GP | W  | T | L | GF | GA | GD | P  |
    | 1. Bayern Munich | 22 | 14 | 4 | 4 | 62 | 24 | 38 | 46 |
    """
    # build header for team first
    table = build_header('team', len(team_name) + len(str(stats['pos'])), 4)

    # then loop over everthing else
    for key, value in stats.items():
        if key != 'pos':
            table += build_header(key, len(value), 2)

    table += '|'

    return f'```{table}```'
