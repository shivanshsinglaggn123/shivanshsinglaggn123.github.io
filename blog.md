---
layout: page
title: Blog
permalink: /blog/
---

<ul class="post-list">
{% assign posts_sorted = site.posts | sort: 'date' | reverse %}
{% for post in posts_sorted %}
  <li>
    <span class="post-meta">{{ post.date | date: "%b %-d, %Y" }}</span>
    <h3>
      <a class="post-link" href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
    </h3>
  </li>
{% endfor %}
</ul>
