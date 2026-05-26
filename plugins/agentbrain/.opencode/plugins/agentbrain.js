/**
 * Agent Brain plugin activation hook.
 *
 * Registers bundled skills and injects the bootstrap gate once per session so
 * requests route through Agent Brain before free-form implementation.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const MARKER = 'AGENTBRAIN_BOOTSTRAP_LOADED';
let bootstrapCache = undefined;

const stripFrontmatter = (content) => {
  const match = content.match(/^---\n[\s\S]*?\n---\n([\s\S]*)$/);
  return match ? match[1] : content;
};

const pluginRoot = () => path.resolve(__dirname, '../..');

const bootstrapContent = () => {
  if (bootstrapCache !== undefined) return bootstrapCache;

  const root = pluginRoot();
  const skillPath = path.join(root, 'skills', 'agentbrain-bootstrap', 'SKILL.md');
  if (!fs.existsSync(skillPath)) {
    bootstrapCache = null;
    return null;
  }

  const content = stripFrontmatter(fs.readFileSync(skillPath, 'utf8')).trim();
  bootstrapCache = `<${MARKER}>
You have Agent Brain installed.

The activation skill below is already loaded. Follow it before answering, and do not load it again unless the runtime explicitly requires that.

${content}
</${MARKER}>`;
  return bootstrapCache;
};

export const AgentBrainPlugin = async () => ({
  config: async (config) => {
    const skillsDir = path.join(pluginRoot(), 'skills');
    config.skills = config.skills || {};
    config.skills.paths = config.skills.paths || [];
    if (!config.skills.paths.includes(skillsDir)) {
      config.skills.paths.push(skillsDir);
    }
  },

  'experimental.chat.messages.transform': async (_input, output) => {
    const bootstrap = bootstrapContent();
    if (!bootstrap || !output.messages?.length) return;

    const firstUser = output.messages.find((message) => message.info?.role === 'user');
    if (!firstUser?.parts?.length) return;
    if (firstUser.parts.some((part) => part.type === 'text' && part.text.includes(MARKER))) return;

    const ref = firstUser.parts[0];
    firstUser.parts.unshift({ ...ref, type: 'text', text: bootstrap });
  },
});

export default AgentBrainPlugin;
