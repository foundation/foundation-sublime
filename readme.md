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
