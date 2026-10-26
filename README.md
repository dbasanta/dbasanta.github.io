# David Basanta - Personal Website

A modern, fast-loading Jekyll website for the CancerEvo Group at Moffitt Cancer Center.

## Features

- Clean, minimal design optimized for fast loading
- Responsive layout that works on all devices
- Team/group members section
- Research highlights
- Contact information and social media links

## Setup

1. Install Jekyll and dependencies:
   ```bash
   bundle install
   ```

2. Run the site locally:
   ```bash
   bundle exec jekyll serve
   ```

3. Visit `http://localhost:4000` in your browser

## Customization

### Update Team Members

Edit the `team.md` file to add your postdocs and PhD students information:
- Replace placeholder names with actual team member names
- Add their research interests
- Add their email addresses
- Optionally add photos by placing them in `assets/images/` and referencing them in the team member sections

### Adding Photos

Phone photos record where they were taken (GPS) and the camera used. Strip that before committing:
```bash
python3 _tools/image_metadata.py assets/images/team/new-photo.jpg
```
To have git refuse commits of photos that still carry metadata, run once in your clone (needs `pip install pillow`):
```bash
git config core.hooksPath _tools/hooks
```
Size photos for how they are displayed: team portraits are 400×400 px plus an 800×800 `_large` version for high-density screens (see `team.md`); the homepage photo has 1000 px and 2000 px versions.

### Publications

The Publications page is generated from `_data/publications.yml`, newest first. Each entry has:
- `title`, `authors` (comma-separated, as "Family Initials"), `venue`, `details`, `year`, `date` (for ordering within a year) and `doi`
- `group_authors`: the authors to show in bold (current and former CancerEvo members, written exactly as in `authors`)
- `summary`: one or two sentences describing the paper
- `theme`: `bone`, `stroma`, `selection` or `methods` (the tag linking to the Research page; leave it out if none fits)
- optional `preprints` (`server`, `url`) and `blog_posts` (`site`, `title`, `url`)

To add a paper, copy an existing entry and edit it. Only published papers are listed, not preprints.

### Styling

All styles are in `assets/css/style.css`. The design uses CSS variables for easy customization:
- `--primary-color`: Main color for headers and navigation
- `--accent-color`: Color for links and highlights
- `--text-color`: Main text color
- `--bg-color`: Background color

## Deployment

### GitHub Pages

1. Push this repository to GitHub
2. Go to repository Settings → Pages
3. Select the branch to deploy (usually `main`)
4. Your site will be available at `https://yourusername.github.io`

### Custom Domain

Add a `CNAME` file with your custom domain name.

## License

MIT License - feel free to use and modify for your own academic website.
