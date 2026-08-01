import { chromium } from 'playwright';

const urls = [
  'https://sanand0.github.io/tdsdata/js_table/?seed=24',
  'https://sanand0.github.io/tdsdata/js_table/?seed=25',
  'https://sanand0.github.io/tdsdata/js_table/?seed=26',
  'https://sanand0.github.io/tdsdata/js_table/?seed=27',
  'https://sanand0.github.io/tdsdata/js_table/?seed=28',
  'https://sanand0.github.io/tdsdata/js_table/?seed=29',
  'https://sanand0.github.io/tdsdata/js_table/?seed=30',
  'https://sanand0.github.io/tdsdata/js_table/?seed=31',
  'https://sanand0.github.io/tdsdata/js_table/?seed=32',
  'https://sanand0.github.io/tdsdata/js_table/?seed=33'
];

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  let grandTotal = 0;

  for (const url of urls) {
    await page.goto(url, { waitUntil: 'networkidle' });
    await page.waitForSelector('#table table td');

    const cellTexts = await page.$$eval('#table table td', tds => tds.map(td => td.textContent.strip ? td.textContent.strip() : td.textContent.trim()));
    const numbers = cellTexts.map(t => parseInt(t, 10)).filter(n => !isNaN(n));

    const pageSum = numbers.reduce((acc, curr) => acc + curr, 0);
    console.log(`Page ${url} sum: ${pageSum} (${numbers.length} numbers parsed)`);
    grandTotal += pageSum;
  }

  await browser.close();

  console.log(`\n========================================`);
  console.log(`TOTAL SUM: ${grandTotal}`);
  console.log(`========================================`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
