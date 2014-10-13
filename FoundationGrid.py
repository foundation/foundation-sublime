import sublime, sublime_plugin, re

class FoundationGridDecodeCommand(sublime_plugin.TextCommand):
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

  # Regular expressions for finding grid classes, columns, and rows
  re_class   = r"[a-z]{2}-?[1-9]*(?:\(.*\))?"
  re_column = r"(?:"+self.re_class+")+"
  re_row    = r"(?:"+self.re_column+",*)+"

  def parse_row(input, depth):
    row_indent = '\t' * (depth * 2)
    column_indent = row_indent + '\t'

    columns = re.findall(self.re_column, input)

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
      sizes = re.findall(self.re_class, base_column)
      for size in sizes:
        bp, number = size[:2], size[2:]
        if 'p' in bp:
          # Pull (negative number)
          if '-' in number:
            output += '%sll-%s' % (self.BREAKPOINTS[bp], number[1:])
          # Push (positive number)
          else:
            output += '%ssh-%s' % (self.BREAKPOINTS[bp], number)
        else:
          output += '%s-%s' % (self.BREAKPOINTS[bp], number)
        output += ' '
      output += 'columns">\n'

      # Nested rows
      if nested_row:
        # Pull the first result out of the re search, and strip the parentheses from the string
        output += self.parse_row(nested_row[0][1:-1], depth + 1)
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
    rows = re.findall(self.re_row, input)

    # Processing rows
    for row in rows:
      output += self.parse_row(row, 0)

    print output

  def run(self, edit):
    selections = self.view.sel()
    for selection in selections:
      edit = self.view.begin_edit('foundation-grid')
      string = self.view.substr(selection)
      self.view.replace(edit, selection, self.unencode(string))
      self.view.end_edit(edit)