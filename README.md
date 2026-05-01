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

### Add Publications

You can create a new `publications.md` page or add publications to the `research.md` page.

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
