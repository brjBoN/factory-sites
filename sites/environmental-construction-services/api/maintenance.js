const PAGE = `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <title>Site Update in Progress | Environmental Construction Services</title>
  <meta name="description" content="Environmental Construction Services is updating its website. Call for drainage and site-work assistance in Moultrie and South Georgia.">
  <style>
    :root{color-scheme:light;--paper:#f1ecdf;--ink:#17191c;--muted:#5f625f;--red:#b82f26;--line:rgba(23,25,28,.18)}
    *{box-sizing:border-box}html,body{min-height:100%}
    body{margin:0;display:grid;place-items:center;padding:24px;font-family:Arial,Helvetica,sans-serif;color:var(--ink);background:linear-gradient(90deg,transparent 0 31px,rgba(184,47,38,.12) 31px 32px,transparent 32px),repeating-linear-gradient(0deg,rgba(23,25,28,.035) 0 1px,transparent 1px 34px),var(--paper)}
    main{position:relative;width:min(920px,100%);overflow:hidden;border:1px solid var(--line);border-top:8px solid var(--red);background:rgba(248,244,234,.95);box-shadow:0 28px 70px rgba(23,25,28,.14)}
    main:after{content:"";position:absolute;right:-115px;bottom:-145px;width:370px;height:370px;border:54px solid rgba(184,47,38,.08);border-radius:50%;box-shadow:inset 0 0 0 24px rgba(23,25,28,.04);pointer-events:none}
    .topbar{display:flex;justify-content:space-between;gap:24px;padding:22px 28px;border-bottom:1px solid var(--line);font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase}.topbar span:last-child{color:var(--red)}
    .content{position:relative;z-index:1;max-width:740px;padding:clamp(48px,8vw,92px) clamp(28px,7vw,72px) clamp(54px,8vw,86px)}
    .eyebrow{margin:0 0 20px;color:var(--red);font-size:13px;font-weight:800;letter-spacing:.18em;text-transform:uppercase}
    h1{max-width:690px;margin:0;font-family:"Arial Narrow",Impact,sans-serif;font-size:clamp(58px,10vw,112px);font-weight:900;letter-spacing:-.045em;line-height:.84;text-transform:uppercase}
    .intro{max-width:620px;margin:30px 0 0;color:var(--muted);font-size:clamp(17px,2.1vw,21px);line-height:1.55}
    .services{display:flex;flex-wrap:wrap;gap:8px;margin:26px 0 0;padding:0;list-style:none}.services li{padding:9px 11px;border:1px solid var(--line);background:rgba(255,255,255,.45);font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase}.services li:first-child{border-color:var(--red);color:var(--red)}
    .actions{display:flex;flex-wrap:wrap;gap:12px;margin-top:32px}.actions a{display:inline-flex;min-height:50px;align-items:center;justify-content:center;padding:14px 18px;border:2px solid var(--ink);color:var(--ink);font-size:14px;font-weight:800;letter-spacing:.08em;text-decoration:none;text-transform:uppercase}.actions a:first-child{border-color:var(--red);color:#fff;background:var(--red)}
    .details{margin:26px 0 0;color:var(--muted);font-size:13px;line-height:1.6}
    @media(max-width:600px){body{padding:12px}.topbar{display:block;padding:18px 20px}.topbar span{display:block}.topbar span:last-child{margin-top:8px}.content{padding-inline:20px}h1{font-size:clamp(52px,17vw,78px)}.actions a{width:100%}}
  </style>
</head>
<body>
  <main>
    <div class="topbar"><span>Environmental Construction Services</span><span>Site update in progress</span></div>
    <div class="content">
      <p class="eyebrow">Moultrie, Georgia &bull; Serving South Georgia</p>
      <h1>The site is paused.<br>The work isn't.</h1>
      <p class="intro">We are updating our website. Environmental Construction Services is still available for drainage and complete site work. Drainage is our primary service.</p>
      <ul class="services" aria-label="Services"><li>Drainage</li><li>Land clearing</li><li>Excavation</li><li>Culverts</li><li>Driveways</li><li>Hardscaping</li><li>Seawalls</li></ul>
      <div class="actions"><a href="tel:+12295160821">Call (229) 516-0821</a><a href="mailto:ecs.outdoorcustoms@gmail.com">Email ECS</a></div>
      <p class="details">33 Pine Cone Road, Moultrie, Georgia</p>
    </div>
  </main>
</body>
</html>`;

module.exports = function maintenance(_request, response) {
  response.statusCode = 503;
  response.setHeader("Content-Type", "text/html; charset=utf-8");
  response.setHeader("Cache-Control", "no-store, max-age=0");
  response.setHeader("Retry-After", "86400");
  response.setHeader("X-Robots-Tag", "noindex, nofollow");
  response.end(PAGE);
};
