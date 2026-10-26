// Conservative cleanup: preserve selector order, media boundaries and specificity.
// Only remove earlier declarations shadowed by the same selector/property within
// the same block. Do not merge non-adjacent rules or shorthand/longhand pairs.
import fs from 'node:fs';
import postcss from 'postcss';
let removed = 0;
for (const file of fs.readdirSync('.').filter((name) => name.endsWith('.css'))) {
  const root = postcss.parse(fs.readFileSync(file, 'utf8'), { from: file });
  function clean(container) {
    const seen = new Map();
    for (const node of [...(container.nodes || [])].reverse()) {
      if (node.type === 'atrule' && !node.name.includes('keyframes')) clean(node);
      if (node.type !== 'rule') continue;
      const declarations = seen.get(node.selector) || new Set();
      for (const decl of [...node.nodes].reverse()) {
        if (decl.type !== 'decl') continue;
        const key = decl.prop + ':' + Boolean(decl.important);
        if (
          declarations.has(key) &&
          !decl.value.includes('-webkit-') &&
          !decl.value.includes('-moz-')
        ) {
          decl.remove();
          removed++;
        } else declarations.add(key);
      }
      seen.set(node.selector, declarations);
      if (node.nodes.length === 0) node.remove();
    }
  }
  clean(root);
  fs.writeFileSync(file, root.toString());
}
console.log(`Removed ${removed} shadowed CSS declarations; order retained.`);
