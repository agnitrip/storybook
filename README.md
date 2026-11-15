# Stories by Adhuna

Short picture stories for young readers, written and illustrated by Adhuna.

- `index.html`: the bookshelf, with one card and a "Read the story" button per story
- `story.html?id=<story-id>`: the reader, one page at a time with Back/Next, swipe, arrow keys, page dots, and a "Read to me" button
- `stories.js`: every story's title, author, and page text, plus the picture each page uses
- `stories/<story-id>/pages/`: the pictures

## Adding Adhuna's drawings

1. Photograph or scan each page and save it as `stories/bee-and-flower/pages/01.jpg`, `02.jpg`, and so on. Pictures are shown wide (4:3), so landscape drawings fit best.
2. In `stories.js`, change that page's `image` from `.svg` to `.jpg`.

The `.svg` pictures are placeholders made by `tools/make_placeholder_art.py` (bee story), `tools/make_sleepover_art.py` (sleepover story), and `tools/make_winter_art.py` (winter story).

## Adding a new story

Copy the `bee-and-flower` block in `stories.js`, give it a new `id`, and put its pictures in `stories/<new-id>/pages/`. The bookshelf picks it up automatically.

After editing `stories.js`, bump the `?v=` number on its `<script>` tag in `index.html` and `story.html` so browsers load the new version instead of a cached one.

## Run locally

```bash
python3 -m http.server 8771
```

Then open http://localhost:8771.
