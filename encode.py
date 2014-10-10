from HTMLParser import HTMLParser
import pprint

class foundationParser(HTMLParser):
  # This is a dictionary that stores the structure of our HTML
  tree = []
  # This is an internal counter of what depth the HTML is at
  depth = -1

  def getTree(self):
    return self.tree

  def getLastChild(self, l):
    for i in range(self.depth):
      l = l[-1]['children']
    return l

  # This method is run when the parser encounters an opening tag
  def handle_starttag(self, tag, attrs):
    attrlist = dict(attrs)
    # Skip this tag if it doesn't have any grid classes
    if not any(x in attrlist['class'] for x in ['row', 'column', 'columns']):
      return

    # Create a new object for this element
    elem = {
      'classes': attrlist['class'],
      'children': [],
    }

    # We have to go deeper
    self.depth += 1
    # If we're at the root of the HTML (depth == 0), append the node to the base object
    if self.depth is 0:
      self.tree.append(elem)
    # Otherwise, find the last node at the current depth and append the node as a child
    else:
      self.getLastChild(self.tree).append(elem)

  # This method is run when the parser encounters a closing tag
  def handle_endtag(self, tag):
    # Move up one depth level
    self.depth -= 1

def encodeGrid(tree, root=True):
  CLASSES = {
    'small-12': 'sg12',
    'small-8': 'sg8',
  }

  output = ''
  for elem in tree:
    # Debugging
    print "Element '%s' has '%s' children." % (elem['classes'], len(elem['children']))

    # If it's a column, get the classes
    if 'column' in elem['classes']:
      classes = elem['classes'].split(' ')
      for cls in classes:
        if cls in CLASSES:
          output += CLASSES[cls]

    # We have to go deeper
    if elem['children']:
      nestedOutput = encodeGrid(elem['children'], False)
      # The children of a row are wrapped in parentheses
      if not root and 'row' in elem['classes']:
        nestedOutput = '(%s)' % nestedOutput
      output += nestedOutput

    # Add an appropriate separator if the element is not the last of the bunch
    if elem is not tree[-1]:
      # Rows are separated by a pipe
      if 'row' in elem['classes']:
        output += '|'
      # Columns are separated by a comma
      elif 'column' in elem['classes']:
        output += ','

  return output

syntax = """
  <div class="row">
    <div class="small-8 columns">
      <div class="row">
        <div class="small-12 columns"></div>
        <div class="small-12 columns"></div>
      </div>
    </div>
  </div>
  <div class="row">
    <div class="small-8 columns">
      <div class="row">
        <div class="small-12 columns"></div>
        <div class="small-12 columns"></div>
      </div>
    </div>
  </div>
"""

parser = foundationParser()
parser.feed(syntax)
tree = parser.getTree()
print encodeGrid(tree)