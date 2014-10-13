# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
import re
import pprint

class foundationParser(HTMLParser):
  # This is a dictionary that stores the structure of our HTML
  tree = []
  # This is an internal counter of what depth the HTML is at
  depth = -1

  selfClosingTags = ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'keygen', 'link', 'menuitem', 'meta', 'param', 'source', 'track', 'wbr']

  def getTree(self):
    self.prune(self.tree)
    return self.tree

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

def encodeGrid(tree, root=True):
  def parseClass(cls):
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
        if isPull:
          output += '-'+term
        else:
          output += term

    # If this class is for column sizing, insert the missing "g"
    if noFeature:
      output = output[0] + 'g' + output[1:]

    return output

  output = ''
  for elem in tree:
    # If it's a column, get the classes
    if 'column' in elem['classes']:
      classes = elem['classes'].split(' ')
      for cls in classes:
        output += parseClass(cls)

    # If the element has children, encode those nodes as well
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
   
   <nav class="top-bar" data-topbar>
  <ul class="title-area">
     
    <li class="name">
      <h1>
        <a href="#">
          Top Bar Title
        </a>
      </h1>
    </li>
    <li class="toggle-topbar menu-icon"><a href="#"><span>menu</span></a></li>
  </ul>

  <section class="top-bar-section">
     
    <ul class="right">
      <li class="divider"></li>
      <li class="has-dropdown">
        <a href="#">Main Item 1</a>
        <ul class="dropdown">
          <li><label>Section Name</label></li>
          <li class="has-dropdown">
            <a href="#" class="">Has Dropdown, Level 1</a>
            <ul class="dropdown">
              <li><a href="#">Dropdown Options</a></li>
              <li><a href="#">Dropdown Options</a></li>
              <li><a href="#">Level 2</a></li>
              <li><a href="#">Subdropdown Option</a></li>
              <li><a href="#">Subdropdown Option</a></li>
              <li><a href="#">Subdropdown Option</a></li>
            </ul>
          </li>
          <li><a href="#">Dropdown Option</a></li>
          <li><a href="#">Dropdown Option</a></li>
          <li class="divider"></li>
          <li><label>Section Name</label></li>
          <li><a href="#">Dropdown Option</a></li>
          <li><a href="#">Dropdown Option</a></li>
          <li><a href="#">Dropdown Option</a></li>
          <li class="divider"></li>
          <li><a href="#">See all →</a></li>
        </ul>
      </li>
      <li class="divider"></li>
      <li><a href="#">Main Item 2</a></li>
      <li class="divider"></li>
      <li class="has-dropdown">
        <a href="#">Main Item 3</a>
        <ul class="dropdown">
          <li><a href="#">Dropdown Option</a></li>
          <li><a href="#">Dropdown Option</a></li>
          <li><a href="#">Dropdown Option</a></li>
          <li class="divider"></li>
          <li><a href="#">See all →</a></li>
        </ul>
      </li>
    </ul>
  </section>
</nav>

 


 

<div class="row">

   
  <div class="large-9 columns">

    <h3>Get in Touch!</h3>
    <p>We'd love to hear from you. You can either reach out to us as a whole and one of our awesome team members will get back to you, or if you have a specific question reach out to one of our staff. We love getting email all day <em>all day</em>.</p>

    <div class="section-container tabs" data-section>
      <section class="section">
        <h5 class="title"><a href="#panel1">Contact Our Company</a></h5>
        <div class="content" data-slug="panel1">
          <form>
            <div class="row collapse">
              <div class="large-2 columns">
                <label class="inline">Your Name</label>
              </div>
              <div class="large-10 columns">
                <input type="text" id="yourName" placeholder="Jane Smith">
              </div>
            </div>
            <div class="row collapse">
              <div class="large-2 columns">
                <label class="inline"> Your Email</label>
              </div>
              <div class="large-10 columns">
                <input type="text" id="yourEmail" placeholder="jane@smithco.com">
              </div>
            </div>
            <label>What's up?</label>
            <textarea rows="4"></textarea>
            <button type="submit" class="radius button">Submit</button>
          </form>
        </div>
      </section>
      <section class="section">
        <h5 class="title"><a href="#panel2">Specific Person</a></h5>
        <div class="content" data-slug="panel2">
          <ul class="large-block-grid-5">
            <li><a href="mailto:mal@serenity.bc.reb"><img src="http://placehold.it/200x200&text=[person]">Mal Reynolds</a></li>
            <li><a href="mailto:zoe@serenity.bc.reb"><img src="http://placehold.it/200x200&text=[person]">Zoe Washburne</a></li>
            <li><a href="mailto:jayne@serenity.bc.reb"><img src="http://placehold.it/200x200&text=[person]">Jayne Cobb</a></li>
            <li><a href="mailto:doc@serenity.bc.reb"><img src="http://placehold.it/200x200&text=[person]">Simon Tam</a></li>
            <li><a href="mailto:killyouwithmymind@serenity.bc.reb"><img src="http://placehold.it/200x200&text=[person]">River Tam</a></li>
            <li><a href="mailto:leafonthewind@serenity.bc.reb"><img src="http://placehold.it/200x200&text=[person]">Hoban Washburne</a></li>
            <li><a href="mailto:book@serenity.bc.reb"><img src="http://placehold.it/200x200&text=[person]">Shepherd Book</a></li>
            <li><a href="mailto:klee@serenity.bc.reb"><img src="http://placehold.it/200x200&text=[person]">Kaywinnet Lee Fry</a></li>
            <li><a href="mailto:inara@guild.comp.all"><img src="http://placehold.it/200x200&text=[person]">Inarra Serra</a></li>
          </ul>
        </div>
      </section>
    </div>
  </div>

   


   


  <div class="large-3 columns">
    <h5>Map</h5>
     
    <p>
      <a href="" data-reveal-id="mapModal"><img src="http://placehold.it/400x280"></a><br/>
      <a href="" data-reveal-id="mapModal">View Map</a>
    </p>
    <p>
      123 Awesome St.<br/>
      Barsoom, MA 95155
    </p>
  </div>
   
</div>

 


 

<footer class="row">
  <div class="large-12 columns">
    <hr/>
    <div class="row">
      <div class="large-6 columns">
        <p>© Copyright no one at all. Go to town.</p>
      </div>
      <div class="large-6 columns">
        <ul class="inline-list right">
          <li><a href="#">Link 1</a></li>
          <li><a href="#">Link 2</a></li>
          <li><a href="#">Link 3</a></li>
          <li><a href="#">Link 4</a></li>
        </ul>
      </div>
    </div>
  </div>
</footer>

 



 

<div class="reveal-modal" id="mapModal">
  <h4>Where We Are</h4>
  <p><img src="http://placehold.it/800x600"/></p>

   
  <a href="#" class="close-reveal-modal">×</a>
</div>
  
  
   
"""

parser = foundationParser()
parser.feed(syntax)
tree = parser.getTree()
pp = pprint.PrettyPrinter()
# pp.pprint(tree)
print encodeGrid(tree)
