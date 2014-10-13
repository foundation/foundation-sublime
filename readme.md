# Foundation Shorthand

This is a plugin for Sublime Text which allows you to expand grid shorthand into HTML with tab triggers.

Example:

```
sg12mg4,sg12mg8
```

Expands to:

```html
<div class="row">
  <div class="small-12 medium-4 columns">
  </div>
  <div class="small-12 medium-8 columns">
  </div>
</div>
```

Right now it's not actually a plugin. Test the output by running:

```bash
python encode.py
python unencode.py
```

Good luck have Batman

## Checklist

**Decoder**
- Parses rows, columns, and classes using regular expressions
- Translates class keywords into proper classes: sizing, offset, center, push, pull
- ~~Properly indents final HTML~~

**Encoder**
- ~~Parses a string of HTML into a structured object~~
- ~~Outputs grid elements with proper nesting and delimiters~~
- ~~Outputs all possible classes: sizing, offset, center, push, pull~~
- Handles edge cases: ~~rows with no children~~, rows directly inside rows

## Regular expression

This is the regular expression used to find grid classes.

```
[a-z]{2}     # Two lowercase letters
-?          # Zero or one hyphens
[1-9]*       # Zero or more numbers
(?:
  \(.*\)     # A left parentheses, any content, and a right parentheses
)?           # The above pattern is optional
```
