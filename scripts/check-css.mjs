import fs from 'node:fs';
import postcss from 'postcss';
for (const file of fs.readdirSync('.').filter((name) => name.endsWith('.css'))) {
  postcss.parse(fs.readFileSync(file, 'utf8'), { from: file });
}
