# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
import sublime, sublime_plugin, re

class foundationParser(HTMLParser):
  # This is a dictionary that stores the structure of our HTML
  tree = []
  # This is an internal counter of what depth the HTML is at
  depth = -1

  selfClosingTags = ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'keygen', 'link', 'menuitem', 'meta', 'param', 'source', 'track', 'wbr']

  def __init__(self, string):
    HTMLParser.__init__(self)
    self.feed(string)
    self.close()
    self.reset()

  def getTree(self):
    self.prune(self.tree)
    return self.tree
    self.tree = []

  def getLastChild(self, tree, depth):
    for i in range(depth):
      # Sometimes this tree searcher goes out of range but it's all good
      try:
        tree = tree[-1]['children']
      except IndexError:
        pass
    return tree

  # This method is run when the parser encounters an opening tag
  def handle_starttag(self, tag, attrs):
    attrlist = dict(attrs)

    # Skip self-closing tags because it's the worst
    if any(x in tag for x in self.selfClosingTags):
      return

    # We have to go deeper
    self.depth += 1

    # No class? Forget it
    if not 'class' in attrlist:
      return
    # Or skip this tag if it doesn't have any grid classes
    if not any(x in attrlist['class'].split(' ') for x in ['row', 'column', 'columns']):
      return

    # Create a new object for this element
    elem = {
      'classes': attrlist['class'],
      'children': [],
    }

    # If we're at the root of the HTML (depth == 0), append the node to the base object
    if self.depth is 0:
      self.tree.append(elem)
    # Otherwise, find the last node at the current depth and append the node as a child
    else:
      self.getLastChild(self.tree, self.depth).append(elem)

  # This method is run when the parser encounters a closing tag
  def handle_endtag(self, tag):
    # Skip self-closing tags because it's the worst
    if any(x in tag for x in self.selfClosingTags):
      return

    # Move up one depth level
    self.depth -= 1

  # Prune rows with no children to keep the final output of the encoder more clean
  def prune(self, tree):
    for i, elem in enumerate(tree):
      # Recursively search for more rows
      if len(elem['children']) > 0:
        self.prune(elem['children'])
      # If the element is a row with no children, remove it from the tree
      elif 'row' in elem['classes']:
        del tree[i]

class FoundationGridEncodeCommand(sublime_plugin.TextCommand):
  def parseClass(self, cls):
    output = ''

    re_class = r'(small|medium|large|xlarge){1}-((centered|offset|push|pull)-?)?[\d]*'
    pattern = re.compile(re_class)

    sizeClasses = ['small', 'medium', 'large', 'xlarge']
    featureClasses = ['offset', 'centered', 'push', 'pull']

    # The class must have a breakpoint keyword in it
    if pattern.search(cls) is None:
      return output

    # Alright, figure out what the breakpoint is
    classes = cls.split('-')
    isPull = False
    noFeature = True

    for term in classes:
      # This is a breakpoint class
      if any(x in term for x in sizeClasses):
        output += term[0]
      # This is a feature class
      if any(x in term for x in featureClasses):
        noFeature = False
        isPull = term == 'pull'
        output += term[0]
      # This is a sizing class
      if term.isdigit():
        # Add a leading zero
        if len(term) == 1:
          term = '0'+term
        if isPull:
          output += '-'+term
        else:
          output += term

    # If this class is for column sizing, insert the missing "g"
    if noFeature:
      output = output[0] + 'g' + output[1:]

    return output

  def encodeGrid(self, tree, root=True):
    output = ''
    for elem in tree:
      # If it's a column, get the classes
      if 'column' in elem['classes']:
        classes = elem['classes'].split(' ')
        for cls in classes:
          output += self.parseClass(cls)

      # If the element has children, encode those nodes as well
      if elem['children']:
        nestedOutput = self.encodeGrid(elem['children'], False)
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

  def run(self, edit):
    selections = self.view.sel()
    for selection in selections:
      # Get the HTML from the selection
      edit = self.view.begin_edit('foundation-grid')
      string = self.view.substr(selection)

      # print "Feeding the parser:\n%s" % string

      # Feed it to the parser
      parser = foundationParser(string)
      tree = parser.getTree()

      # print "The parser returned:\n%s" % tree

      # Now encode it
      code = self.encodeGrid(tree)
      self.view.replace(edit, selection, code)
      self.view.end_edit(edit)