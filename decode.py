import re

# | = new row
# , = new column

# sm, md, lg, xl
# so, mo, lo, xo
# sp, mp, lp, xp

BREAKPOINTS = {
  'sg': 'small',
  'mg': 'medium',
  'lg': 'large',
  'xg': 'xlarge',
  'so': 'small-offset',
  'mo': 'medium-offset',
  'lo': 'large-offset',
  'xo': 'xlarge-offset',
  'sc': 'small-centered',
  'mc': 'medium-centered',
  'lc': 'large-centered',
  'xc': 'xlarge-centered',
}

# Regular expressions for finding column sizes and column clusters
re_size   = r"[a-z]{2}-?[1-9]*(?:\(.*\))?"
re_column = r"(?:"+re_size+")+"
re_row    = r"(?:"+re_column+",*)+"

def parse_row(input, depth):
  row_indent = '\t' * (depth * 2)
  column_indent = row_indent + '\t'

  columns = re.findall(re_column, input)

  # Opening tag for row
  output = '%s<div class="row">\n' % row_indent

  # Processing columns
  for column in columns:
    string = column.split('>', 1)
    base_column = string[0]
    nested_row  = string[1] if len(string) > 1 else None

    sizes = re.findall(re_size, base_column)

    # Opening tag for column
    output += '%s<div class="' % column_indent

    # Processing breakpoint classes
    for size in sizes:
      bp, number = size[:2], size[2:]
      output += '%s-%s ' % (BREAKPOINTS[bp], number)
    output += 'columns">\n'

    # Nested rows
    if nested_row is not None:
      output += parse_row(nested_row, depth + 1)
    else:
      # Insert a blank line if there's no nested row
      output += '%s\n' % column_indent

    # Closing tag for column
    output += '%s</div>\n' % column_indent

  # Closing tag for row
  output += '%s</div>\n' % row_indent
  return output

def unencode(input):
  output = ''
  rows = input.lower().split('|')

  # Processing rows
  for row in rows:
    output += parse_row(row, 0)

  print output

unencode('sg12mg6lo4>')