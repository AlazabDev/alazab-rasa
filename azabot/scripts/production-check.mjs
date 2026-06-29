import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const distPath = path.resolve(__dirname, '../dist');

console.log('🚀 Starting Production Build Validation...');

if (!fs.existsSync(distPath)) {
  console.error('❌ Error: dist folder not found. Run build first.');
  process.exit(1);
}

const indexHtml = fs.readFileSync(path.join(distPath, 'index.html'), 'utf-8');

// Check for sensitive strings that shouldn't be in the build
const sensitivePatterns = [
  /VITE_SUPABASE_SERVICE_ROLE_KEY/i,
  /SECRET_KEY/i
];

sensitivePatterns.forEach(pattern => {
  if (pattern.test(indexHtml)) {
    console.error(`⚠️ Warning: Potential sensitive pattern found in build: ${pattern}`);
  }
});

// Check for bundle size
const assetsDir = path.join(distPath, 'assets');
if (fs.existsSync(assetsDir)) {
  const files = fs.readdirSync(assetsDir);
  const largeFiles = files.filter(f => fs.statSync(path.join(assetsDir, f)).size > 1024 * 1024);
  if (largeFiles.length > 0) {
    console.warn('⚠️ Warning: Large chunks detected (>1MB):', largeFiles);
  }
}

console.log('✅ Production check passed!');
