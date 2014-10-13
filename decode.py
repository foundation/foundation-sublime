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
  'sp': 'small-pu',
  'mp': 'medium-pu',
  'lp': 'large-pu',
  'xp': 'xlarge-pu',
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
    # Given the string sg1(sg2)
    # sg1 is the base_column, and (sg2) is the nested row
    base_column = column.split('(', 1)[0]
    nested_row = re.findall(r'\(.*\)', column)

    # Opening tag for column
    output += '%s<div class="' % column_indent

    # Processing breakpoint classes
    sizes = re.findall(re_size, base_column)
    for size in sizes:
      bp, number = size[:2], size[2:]
      if 'p' in bp:
        # Pull (negative number)
        if '-' in number:
          output += '%sll-%s' % (BREAKPOINTS[bp], number[1:])
        # Push (positive number)
        else:
          output += '%ssh-%s' % (BREAKPOINTS[bp], number)
      else:
        output += '%s-%s' % (BREAKPOINTS[bp], number)
      output += ' '
    output += 'columns">\n'

    # Nested rows
    if nested_row:
      # Pull the first result out of the re search, and strip the parentheses from the string
      output += parse_row(nested_row[0][1:-1], depth + 1)
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
  rows = re.findall(re_row, input)

  # Processing rows
  for row in rows:
    output += parse_row(row, 0)

  print output

unencode('sg12mg6lo4lp2(sg12,sg6(sg12))|sg12')
