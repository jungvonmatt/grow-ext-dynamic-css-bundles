# grow-ext-inline-text-assets
Extension for the static-site generator Grow that enables you to add textual asset dependencies via calls from your template.

## Concept
This extension comes in handy if you want to use inline stylesheets for your project. To do so you could simply configure a asset bundle that you can then add files to just by calls from your templates.

And only for the files that are really needed in your template, instead of using pre-configured bundles.

## Usage
### Initial setup
1. Create an `extensions.txt` file within your pod.
1. Add to the file: `git+git://github.com/jungvonmatt/grow-ext-inline-text-assets`
1. Run `grow install`.
1. Add the following section to `podspec.yaml`:

```yaml
ext:
- extensions.inline_text_assets.InlineTextAssetsExtension:
    bundles:
        - name: 'styles'
          method: 'addCssFile'
        - name: 'icons'
          method: 'useIcon'
```

This configuration adds two bundles to your documents that can be used in your templates with for example

```jinja2
{% if headline %}
{{ doc.styles.addCssFile('/css/headlines.css', 99) }}
<h1>{{ headline }}</h1>
{% endif %}
```

```jinja2
<style amp-custom>
{{ doc.styles.emit() }}
</style>
```
