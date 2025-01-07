

{% if "navigation.footer" in features %}
{% if page.previous\_page or page.next\_page %}
{% if page.meta and page.meta.hide %}
{% set hidden = "hidden" if "footer" in page.meta.hide %}
{% endif %}

{% if page.previous\_page %}
{% set direction = lang.t("footer.previous") %}
[{% set icon = config.theme.icon.previous or "material/arrow-left" %}
{% include ".icons/" ~ icon ~ ".svg" %}

{{ direction }}

{{ page.previous\_page.title }}](%7B%7B%20page.previous_page.url%20%7C%20url%20%7D%7D)
{% endif %}

{% if page.next\_page %}
{% set direction = lang.t("footer.next") %}
[{{ direction }}

{{ page.next\_page.title }}

{% set icon = config.theme.icon.next or "material/arrow-right" %}
{% include ".icons/" ~ icon ~ ".svg" %}](%7B%7B%20page.next_page.url%20%7C%20url%20%7D%7D)
{% endif %}

{% endif %}
{% endif %}

[Main index](./index.html) | [Topics index](./topics.html) | [Keywords index](./keywords.html) | [Graphical index](./graphical_index.html) | [Full index](./full_index.html)

{% include "partials/copyright.html" %}

{% if config.extra.social %}
{% include "partials/social.html" %}
{% endif %}
