#!/usr/bin/env node
// Read-only guided browser QA. Only submits synthetic training records.
const fs=require('fs'),path=require('path');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'/home/aella/.dev/parserstudio-core/node_modules/playwright');
const root=path.join(__dirname,'..');
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 const ctx=await browser.newContext({viewport:{width:1440,height:900}});
 const page=await ctx.newPage();
 try{
  await page.goto(process.env.PARSER_STUDIO_URL||'https://app.parser.xdr.ooo/',{waitUntil:'networkidle',timeout:30000});
  const asset=await page.locator('script[src^="/assets/index-"]').first().getAttribute('src');
  await page.getByPlaceholder('e.g. Fortinet').fill('Training');
  await page.getByPlaceholder('e.g. FortiGate').fill('Relay KV demo');
  const source=fs.readFileSync(path.join(root,'practice/05-relay-forwarded.log'),'utf8').trim();
  await page.getByRole('textbox',{name:'Auto Parser raw logs'}).fill(source);
  const details=page.locator('details[aria-label="Review declared relay hosts"]');
  await details.locator('summary').click();
  await page.getByRole('textbox',{name:'Declared relay hostname list'}).fill('relay01');
  const preview=await page.locator('[aria-label="Relay source preview"]').innerText();
  if(!preview.includes('2 of 2 events recognized')||!preview.includes('0 unsafe')||!preview.includes('0 not matching')) throw Error('Relay preview mismatch: '+preview);
  await page.getByRole('button',{name:'Apply declared relay profile'}).click();
  await page.getByText(/Declared relays added to your local draft/).waitFor({timeout:20000});
  await page.getByRole('button',{name:'Analyze Logs'}).click();
  await page.getByText(/log events parsed completely/).first().waitFor({timeout:30000});
  const body=await page.locator('body').innerText();
  const m=body.match(/\d+ of \d+ log events parsed completely/g)||[];
  await page.screenshot({path:path.join(root,'images/current-12-relay-profile.png'),fullPage:true});
  console.log(JSON.stringify({asset,preview,counts:m,active:body.includes('Local profile: relay01'),reviewFieldsEnabled:await page.getByRole('button',{name:/Review Fields/}).last().isEnabled(),sampleBytes:Buffer.byteLength(source)},null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error('QA_FAIL',e.stack);process.exitCode=1});
