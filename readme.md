# Morse Code for Foundation

This is a Sublime Text plugin that allows you to expand a shorthand grid syntax into full HTML, à la Emmet. Learn more about all of its features [here](http://zurb.com/playground/foundation-morse-code).

## Installing

Install using [Package Control](https://sublime.wbond.net/installation). It's not yet in the package registry, so you can install it by selecting "Package Control: Add Repository" in the command palette and pasting in this URL:

```
https://github.com/zurb/foundation-sublime.git
```

## Example

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

## Known Issues

- The decoder will output a little funny if you break Foundation rules, like putting a column directly inside a column, a row directly inside a row, or a row and column as siblings.
- If you run the encoder multiple times, all the previous HTML that's been parsed is also processed and output. I have *no idea why*, because every time you run the command it only feeds the parser the HTML you have selected, and somehow old HTML is persisting between runs of the command.