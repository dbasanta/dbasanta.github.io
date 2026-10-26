---
layout: default
title: Home
description: The CancerEvo Group develops mathematical and computational models of cancer ecology, evolution, treatment response, and resistance.
---

<section class="home-intro">
  <h1 class="home-title">CancerEvo</h1>
  <p class="home-sub">Cancer ecology &amp; evolution</p>
  <p class="home-affil"><a href="{{ site.imo_url }}" target="_blank" rel="noopener noreferrer">Integrated Mathematical Oncology</a> &middot; <a href="{{ site.moffitt_url }}" target="_blank" rel="noopener noreferrer">Moffitt Cancer Center</a></p>
</section>


<nav class="icon-grid" aria-label="Site sections">
  <a class="tile" href="{{ '/research' | relative_url }}" style="--c: #D9483B; --c-ink: #B8362B">
    {% include icons/bone-ecosystem.svg %}
    <span>Research</span>
  </a>
  <a class="tile" href="{{ '/publications' | relative_url }}" style="--c: #E58A1F; --c-ink: #9E560A">
    {% include icons/cell-fusion.svg %}
    <span>Publications</span>
  </a>
  <a class="tile" href="{{ '/team' | relative_url }}" style="--c: #B0418F; --c-ink: #B0418F">
    {% include icons/stromal-niche.svg %}
    <span>Team</span>
  </a>
  <a class="tile" href="{{ '/models' | relative_url }}" style="--c: #2E9655; --c-ink: #23794A">
    {% include icons/hybrid-model.svg %}
    <span>Models &amp; Code</span>
  </a>
  <a class="tile" href="{{ '/outreach' | relative_url }}" style="--c: #1592A6; --c-ink: #0F7180">
    {% include icons/evolutionary-game.svg %}
    <span>Outreach</span>
  </a>
  <a class="tile" href="{{ '/about' | relative_url }}" style="--c: #2F5AB4; --c-ink: #2F5AB4">
    {% include icons/evolutionary-rescue.svg %}
    <span>About</span>
  </a>
</nav>
