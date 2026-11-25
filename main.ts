// Entry point: copy the pre-rendered front page to the output directory.
// The image is rendered by render.py (Pillow, no network use); this driver
// only copies it, so the output is byte-identical on every run.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const out = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
mkdirSync(out, { recursive: true });
const here = dirname(fileURLToPath(import.meta.url));
copyFileSync(join(here, "entry.png"), join(out, "entry.png"));
