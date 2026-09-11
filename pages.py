
# pages.py  -  OXNET v2.0.10
# شامل: LOGIN_HTML, DASHBOARD_HTML, get_public_page_html()

LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<script>(function(){try{var t=localStorage.getItem("oxnet-theme");if(t==="dark"||t==="light")document.documentElement.setAttribute("data-theme",t);}catch(e){}})();</script>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ورود · OXNET Edge</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --font:"Vazirmatn",system-ui,-apple-system,"Segoe UI",Tahoma,sans-serif;
  --bg:#F8FAFC; --bg2:#EEF2F7; --card:#FFFFFF;
  --ink:#111827; --muted:#6B7280; --line:#E5E7EB;
  --accent:#2563EB; --accent-hover:#1D4ED8; --accent-soft:rgba(37,99,235,.08);
  --ok:#16A34A; --err:#DC2626; --err-bg:rgba(220,38,38,.08);
  --r-sm:10px; --r-md:14px; --r-lg:18px;
  --shadow:0 8px 20px rgba(15,23,42,.05);
  --t:200ms ease;
}
@media (prefers-color-scheme: dark){
  :root{
    --bg:#0B1220; --bg2:#111827; --card:#111827;
    --ink:#F8FAFC; --muted:#CBD5E1; --line:#334155;
    --accent:#3B82F6; --accent-hover:#60A5FA; --accent-soft:rgba(59,130,246,.12);
    --ok:#22C55E; --err:#EF4444; --err-bg:rgba(239,68,68,.12);
    --shadow:0 8px 24px rgba(0,0,0,.35);
  }
}
html[data-theme="light"]{
  --bg:#F8FAFC; --bg2:#EEF2F7; --card:#FFFFFF;
  --ink:#111827; --muted:#6B7280; --line:#E5E7EB;
  --accent:#2563EB; --accent-hover:#1D4ED8; --accent-soft:rgba(37,99,235,.08);
  --ok:#16A34A; --err:#DC2626; --err-bg:rgba(220,38,38,.08);
  --shadow:0 8px 20px rgba(15,23,42,.05);
}
html[data-theme="dark"]{
  --bg:#0B1220; --bg2:#111827; --card:#111827;
  --ink:#F8FAFC; --muted:#CBD5E1; --line:#334155;
  --accent:#3B82F6; --accent-hover:#60A5FA; --accent-soft:rgba(59,130,246,.12);
  --ok:#22C55E; --err:#EF4444; --err-bg:rgba(239,68,68,.12);
  --shadow:0 8px 24px rgba(0,0,0,.35);
}
html,body{height:100%}
body{
  font-family:var(--font);color:var(--ink);background:linear-gradient(180deg,var(--bg),var(--bg2));
  min-height:100vh;display:flex;-webkit-font-smoothing:antialiased;line-height:1.6;font-weight:400;
}
.shell{display:grid;grid-template-columns:1.05fr .95fr;width:100%;min-height:100vh}
@media(max-width:860px){.shell{grid-template-columns:1fr}.brand-pane{display:none}}
.brand-pane{
  background:linear-gradient(165deg,#0F172A 0%,#1E3A8A 100%);
  color:#F8FAFC;padding:48px;display:flex;flex-direction:column;justify-content:space-between;
  position:relative;overflow:hidden;
}
.brand-pane::after{
  content:"";position:absolute;width:420px;height:420px;border-radius:50%;
  background:rgba(37,99,235,.18);top:-80px;left:-80px;pointer-events:none;
}
.brand-top{position:relative;z-index:1}
.logo-row{display:flex;align-items:center;gap:14px;margin-bottom:48px}
.logo-mark{
  width:48px;height:48px;border-radius:var(--r-md);background:#2563EB;color:#fff;
  display:flex;align-items:center;justify-content:center;font-size:22px;
  box-shadow:0 8px 20px rgba(37,99,235,.35);
}
.logo-name{font-size:22px;font-weight:700;letter-spacing:-.02em}
.logo-ver{font-size:12px;color:#94A3B8;font-weight:500;margin-top:2px}
.brand-title{font-size:32px;font-weight:700;letter-spacing:-.03em;line-height:1.3;margin-bottom:14px;max-width:380px}
.brand-desc{font-size:14.5px;color:#CBD5E1;line-height:1.8;max-width:360px;font-weight:400}
.brand-foot{position:relative;z-index:1;font-size:12px;color:#94A3B8}
.form-pane{display:flex;align-items:center;justify-content:center;padding:32px 24px}
.card{
  width:100%;max-width:400px;background:var(--card);border:1px solid var(--line);
  border-radius:var(--r-lg);padding:32px 28px;box-shadow:var(--shadow);
}
.card h1{font-size:22px;font-weight:700;letter-spacing:-.02em;margin-bottom:8px}
.sub{font-size:13.5px;color:var(--muted);margin-bottom:28px;line-height:1.7}
label{display:block;font-size:12.5px;font-weight:600;color:var(--muted);margin-bottom:8px}
.inp-wrap{position:relative}
.inp-wrap .ic{position:absolute;right:14px;top:50%;transform:translateY(-50%);color:var(--muted);font-size:16px;pointer-events:none}
input{
  width:100%;height:48px;border-radius:var(--r-md);border:1px solid var(--line);
  background:var(--card);padding:0 44px 0 16px;font-family:inherit;font-size:14px;color:var(--ink);
  outline:none;transition:border-color var(--t),box-shadow var(--t),background var(--t);
}
input:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
input::placeholder{color:var(--muted);opacity:.7}
.btn{
  width:100%;height:48px;margin-top:16px;border:none;border-radius:var(--r-md);
  background:var(--accent);color:#fff;font-family:inherit;font-size:14.5px;font-weight:600;
  cursor:pointer;display:inline-flex;align-items:center;justify-content:center;gap:8px;
  transition:background var(--t),transform var(--t),box-shadow var(--t);
  box-shadow:0 4px 14px rgba(37,99,235,.28);
}
.btn:hover{background:var(--accent-hover);transform:translateY(-1px)}
.btn:disabled{opacity:.6;cursor:not-allowed;transform:none}
.err{
  display:none;align-items:center;gap:8px;padding:10px 12px;border-radius:var(--r-sm);
  background:var(--err-bg);color:var(--err);font-size:13px;font-weight:500;margin-bottom:16px;
}
.err.show{display:flex}
.footer{margin-top:24px;text-align:center;font-size:12px;color:var(--muted);font-weight:500}

.brand-features{list-style:none;margin-top:28px;display:flex;flex-direction:column;gap:12px;position:relative;z-index:1}
.brand-features li{display:flex;align-items:center;gap:10px;font-size:13.5px;color:#CBD5E1;font-weight:500}
.brand-features i{color:#60A5FA;font-size:16px}
@keyframes spin{to{transform:rotate(360deg)}}
</style>
</head>
<body>
<div class="shell">
  <div class="brand-pane">
    <div class="brand-top">
      <div class="logo-row">
        <div class="logo-mark"><i class="ti ti-network"></i></div>
        <div>
          <div class="logo-name">OXNET</div>
          <div class="logo-ver">Stable · v2.0.11</div>
        </div>
      </div>
      <div class="brand-title">کنسول مدیریت لبه شبکه</div>
      <p class="brand-desc">مدیریت مسیرهای تحویل ترافیک، اشتراک‌ها و مانیتورینگ مصرف — مناسب سرویس‌های CDN و edge delivery.</p>
      <ul class="brand-features">
        <li><i class="ti ti-check"></i> چند مسیر انتقال استاندارد</li>
        <li><i class="ti ti-check"></i> اشتراک و دامنه‌های edge</li>
        <li><i class="ti ti-check"></i> مانیتورینگ نشست و پهنای باند</li>
      </ul>
    </div>
    <div class="brand-foot">OXNET Edge Console</div>
  </div>
  <div class="form-pane">
    <div class="card">
      <h1>ورود به پنل</h1>
      <p class="sub">رمز عبور مدیریت را وارد کنید تا وارد داشبورد شوید.</p>
      <div class="err" id="err"><i class="ti ti-alert-circle"></i><span id="err-text"></span></div>
      <form id="form">
        <div class="field">
          <label>رمز عبور</label>
          <div class="inp-wrap">
            <input type="password" id="pw" placeholder="رمز عبور را وارد کنید" autofocus required autocomplete="current-password">
            <i class="ti ti-lock ic"></i>
          </div>
        </div>
        <button class="btn" type="submit" id="btn"><i class="ti ti-login-2"></i> ورود به داشبورد</button>
      </form>
      <div class="footer">OXNET · 2.0.11</div>
    </div>
  </div>
</div>
<script>
document.getElementById('form').addEventListener('submit',async e=>{
  e.preventDefault();
  const btn=document.getElementById('btn'),err=document.getElementById('err'),et=document.getElementById('err-text');
  err.classList.remove('show');btn.disabled=true;
  btn.innerHTML='<i class="ti ti-loader-2" style="animation:spin 1s linear infinite"></i> در حال ورود...';
  try{
    const r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:document.getElementById('pw').value})});
    if(!r.ok){const d=await r.json().catch(()=>({}));throw new Error(d.detail||'خطا');}
    location.href=(window.OXNET_DASH||'/dashboard');
  }catch(e){
    et.textContent=e.message;err.classList.add('show');
    btn.disabled=false;btn.innerHTML='<i class="ti ti-login-2"></i> ورود به داشبورد';
  }
});
</script>
</body>
</html>
"""

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OXNET · oxnet</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --font:"Vazirmatn", system-ui, -apple-system, "Segoe UI", Tahoma, sans-serif;
  --bg:#F8FAFC;
  --bg2:#FFFFFF;
  --bg3:#E2E8F0;
  --card:#FFFFFF;
  --card-b:#E2E8F0;
  --card-bh:#CBD5E1;
  --accent:#2563EB;
  --accent2:#1D4ED8;
  --accent-d:rgba(37,99,235,0.08);
  --green:#16A34A;
  --green-bg:#DCFCE7;
  --green-t:#15803D;
  --red:#DC2626;
  --red-bg:#FEE2E2;
  --red-t:#B91C1C;
  --amber:#D97706;
  --amber-bg:#FEF3C7;
  --amber-t:#B45309;
  --purple:#7C3AED;
  --purple-bg:rgba(124,58,237,0.10);
  --purple-t:#6D28D9;
  --info:#0891B2;
  --info-bg:rgba(8,145,178,0.10);
  --t1:#0F172A;
  --t2:#64748B;
  --t3:#94A3B8;
  --sidebar-w:264px;
  --radius:14px;
  --r-sm:10px;
  --r-md:14px;
  --r-lg:18px;
  --shadow:0 1px 2px rgba(15,23,42,0.04);
  --shadow-md:0 8px 20px rgba(15,23,42,0.05);
  --shadow-lg:0 16px 40px rgba(15,23,42,0.06);
  --t:200ms ease;
  --space:8px;
}
[data-theme="dark"]{
  --bg:#0F172A;
  --bg2:#111827;
  --bg3:#334155;
  --card:#1E293B;
  --card-b:#334155;
  --card-bh:#475569;
  --accent:#3B82F6;
  --accent2:#60A5FA;
  --accent-d:rgba(59,130,246,0.14);
  --green:#22C55E;
  --green-bg:rgba(34,197,94,0.14);
  --green-t:#4ADE80;
  --red:#EF4444;
  --red-bg:rgba(239,68,68,0.14);
  --red-t:#F87171;
  --amber:#FBBF24;
  --amber-bg:rgba(251,191,36,0.14);
  --amber-t:#FCD34D;
  --purple:#A78BFA;
  --purple-bg:rgba(167,139,250,0.14);
  --purple-t:#C4B5FD;
  --info:#22D3EE;
  --info-bg:rgba(34,211,238,0.12);
  --t1:#F8FAFC;
  --t2:#CBD5E1;
  --t3:#64748B;
  --shadow:0 1px 2px rgba(0,0,0,0.2);
  --shadow-md:0 8px 20px rgba(0,0,0,0.28);
  --shadow-lg:0 16px 40px rgba(0,0,0,0.35);
}
html,body{height:100%}
body{font-family:var(--font,"Vazirmatn",system-ui,-apple-system,"Segoe UI",Tahoma,sans-serif);background:var(--bg);color:var(--t1);min-height:100vh;display:flex;font-size:14.5px;line-height:1.65;font-weight:400;letter-spacing:-.01em;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;text-rendering:optimizeLegibility;transition:background .3s,color .3s}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--bg3);border-radius:3px}
a{color:inherit;text-decoration:none}
.sidebar{width:var(--sidebar-w);min-height:100vh;background:var(--bg2);border-left:1px solid var(--card-b);display:flex;flex-direction:column;flex-shrink:0;position:fixed;right:0;top:0;bottom:0;z-index:200;transition:transform .25s cubic-bezier(.4,0,.2,1),background .3s,border-color .3s}
.logo{display:flex;align-items:center;gap:12px;padding:20px 16px 16px;border-bottom:1px solid var(--card-b)}
.logo-img{width:38px;height:38px;border-radius:10px;overflow:hidden;border:1px solid var(--card-b);box-shadow:0 0 14px var(--accent-d);flex-shrink:0}
.logo-img img{width:100%;height:100%;object-fit:cover}
.brand-mark{width:38px;height:38px;border-radius:10px;display:flex;align-items:center;justify-content:center;background:#0f172a;color:#fff;font-weight:800;letter-spacing:.04em;border:1px solid rgba(15,23,42,.12);box-shadow:0 8px 24px rgba(15,23,42,.12)}
.brand-mark.small{width:28px;height:28px;border-radius:8px;font-size:10px;flex-shrink:0}
.logo-name{font-size:13.5px;font-weight:700;color:var(--t1)}
.logo-sub{font-size:10px;color:var(--t3);margin-top:1px}
.sb-close{display:none;position:absolute;left:12px;top:20px;background:var(--accent-d);border:1px solid var(--card-b);color:var(--t2);width:30px;height:30px;border-radius:8px;font-size:16px;align-items:center;justify-content:center;cursor:pointer}
.nav-wrap{flex:1;overflow-y:auto;padding:6px 0 8px}
.nav-sec{padding:14px 14px 4px;font-size:9px;letter-spacing:.14em;text-transform:uppercase;color:var(--t3);font-weight:700}
.nav-it{display:flex;align-items:center;gap:9px;padding:9px 14px;color:var(--t3);font-size:12.5px;cursor:pointer;border-right:2px solid transparent;transition:all .15s;margin:1px 6px}
.nav-it i{font-size:16px;width:18px;text-align:center;flex-shrink:0}
.nav-it:hover{background:var(--accent-d);color:var(--t2)}
.nav-it.on{background:var(--accent-d);color:var(--t1);border-right-color:var(--accent);font-weight:600}
.nav-badge{margin-right:auto;background:rgba(37,99,235,0.15);color:var(--accent2);font-size:9px;padding:1px 6px;border-radius:20px;font-weight:700}
.sb-foot{padding:12px 14px;border-top:1px solid var(--card-b)}
.tg-btn{display:flex;align-items:center;justify-content:center;gap:8px;background:linear-gradient(135deg,#0098e6,#0077bb);color:#fff;border-radius:9px;padding:10px;font-size:12.5px;font-weight:600;font-family:inherit;border:none;cursor:pointer;width:100%;transition:.15s}
.tg-btn:hover{filter:brightness(1.1)}
.theme-btn{display:flex;align-items:center;justify-content:center;gap:7px;background:var(--accent-d);color:var(--t2);border-radius:9px;padding:8px;font-size:12px;font-weight:500;font-family:inherit;border:1px solid var(--card-b);cursor:pointer;width:100%;transition:.15s;margin-bottom:7px}
.theme-btn:hover{background:var(--card-b);color:var(--t1)}
.logout-btn{display:flex;align-items:center;justify-content:center;gap:7px;background:var(--red-bg);color:var(--red-t);border-radius:9px;padding:8px;font-size:12px;font-weight:500;font-family:inherit;border:1px solid rgba(239,68,68,0.2);cursor:pointer;width:100%;transition:.15s;margin-top:6px}
.logout-btn:hover{background:rgba(239,68,68,0.2)}
.mob-top{display:none;position:fixed;top:0;right:0;left:0;height:52px;background:var(--bg2);border-bottom:1px solid var(--card-b);z-index:150;align-items:center;justify-content:space-between;padding:0 14px;transition:background .3s}
.mob-top .ml{display:flex;align-items:center;gap:9px}
.mob-logo{width:28px;height:28px;border-radius:7px;overflow:hidden}
.mob-logo img{width:100%;height:100%;object-fit:cover}
.mob-title{color:var(--t1);font-size:13px;font-weight:700}
.mob-right{display:flex;gap:6px}
.menu-btn,.theme-mob{background:var(--accent-d);border:1px solid var(--card-b);color:var(--t2);width:34px;height:34px;border-radius:8px;font-size:17px;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:.15s}
.overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:190;backdrop-filter:blur(3px)}
.overlay.show{display:block}
.main{margin-right:var(--sidebar-w);flex:1;padding:28px 28px 60px;min-width:0;transition:margin .25s}
.pg{display:none}
.pg.on{display:block;animation:none!important;opacity:1!important;transform:none!important}
@keyframes fi{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.topbar{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:22px;flex-wrap:wrap;gap:12px}
.tb-title{font-size:18px;font-weight:700;color:var(--t1);display:flex;align-items:center;gap:8px;letter-spacing:-.02em}
.tb-title i{color:var(--accent);font-size:20px}
.tb-sub{font-size:11px;color:var(--t3);margin-top:4px}
.tb-right{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.badge{font-size:10px;padding:3px 10px;border-radius:20px;font-weight:700;display:inline-flex;align-items:center;gap:5px;white-space:nowrap}
.bg-green{background:var(--green-bg);color:var(--green-t)}
.bg-blue{background:var(--accent-d);color:var(--accent2)}
.bg-amber{background:var(--amber-bg);color:var(--amber-t)}
.bg-red{background:var(--red-bg);color:var(--red-t)}
.bg-purple{background:var(--purple-bg);color:var(--purple-t)}
.dot{width:6px;height:6px;border-radius:50%;flex-shrink:0;display:inline-block}
.dg{background:var(--green)}.dr{background:var(--red)}.da{background:var(--amber)}.db{background:var(--accent)}
.pulse{animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
.metrics{display:grid;grid-template-columns:repeat(6,1fr);gap:13px;margin-bottom:18px}
.metric{background:var(--card);border:1px solid var(--card-b);border-radius:var(--radius);padding:17px 17px 14px;transition:all .2s;position:relative;overflow:hidden;cursor:default}
.metric::after{content:'';position:absolute;top:0;right:0;width:3px;height:100%;background:var(--accent);opacity:0;transition:.2s}
.metric:hover{border-color:var(--card-bh);transform:translateY(-2px);box-shadow:var(--shadow)}
.metric:hover::after{opacity:1}
.metric.suc::after{background:var(--green)}
.metric.dan::after{background:var(--red)}
/* ══════ صفحه ترافیک - ریدیزاین ══════ */
.traf-hero{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:13px;margin-bottom:18px}
.traf-main-stat{background:linear-gradient(155deg,var(--bg3) 0%,var(--card) 60%);border:1px solid var(--card-b);border-radius:20px;padding:22px 24px;position:relative;overflow:hidden}
.traf-main-stat::before{content:'';position:absolute;top:-50px;left:-50px;width:200px;height:200px;background:radial-gradient(circle,var(--accent-d),transparent 70%);pointer-events:none}
.traf-main-label{font-size:10.5px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.08em;display:flex;align-items:center;gap:6px;margin-bottom:10px;position:relative;z-index:1}
.traf-main-val{font-size:34px;font-weight:800;color:var(--t1);line-height:1;letter-spacing:-.02em;display:flex;align-items:baseline;gap:6px;position:relative;z-index:1}
.traf-main-val span{font-size:14px;font-weight:500;color:var(--t3)}
.traf-trend{display:inline-flex;align-items:center;gap:4px;font-size:11px;font-weight:700;padding:4px 10px;border-radius:20px;margin-top:12px;position:relative;z-index:1}
.traf-trend.up{background:var(--green-bg);color:var(--green-t)}
.traf-trend.down{background:var(--red-bg);color:var(--red-t)}
.traf-mini{background:var(--card);border:1px solid var(--card-b);border-radius:20px;padding:18px 19px;display:flex;flex-direction:column;justify-content:space-between;transition:.2s}
.traf-mini:hover{border-color:var(--card-bh);transform:translateY(-2px)}
.traf-mini-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px}
.traf-mini-icon{width:32px;height:32px;border-radius:9px;background:var(--accent-d);color:var(--accent);display:flex;align-items:center;justify-content:center;font-size:15px}
.traf-mini-icon.pk{background:var(--amber-bg);color:var(--amber)}
.traf-mini-icon.lo{background:var(--purple-bg);color:var(--purple)}
.traf-mini-label{font-size:9.5px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.06em}
.traf-mini-val{font-size:21px;font-weight:800;color:var(--t1);letter-spacing:-.01em}
.traf-mini-sub{font-size:9.5px;color:var(--t3);margin-top:3px}

.traf-chart-card{background:var(--card);border:1px solid var(--card-b);border-radius:22px;padding:22px 24px 18px;box-shadow:var(--shadow);margin-bottom:16px}
.traf-chart-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;flex-wrap:wrap;gap:10px}
.traf-chart-title{font-size:14px;font-weight:800;color:var(--t1);display:flex;align-items:center;gap:8px}
.traf-chart-title i{color:var(--accent);font-size:18px}
.traf-chart-sub{font-size:10.5px;color:var(--t3);margin-top:3px}
.traf-legend{display:flex;gap:14px;align-items:center}
.traf-legend-item{display:flex;align-items:center;gap:6px;font-size:10.5px;color:var(--t2);font-weight:600}
.traf-legend-dot{width:8px;height:8px;border-radius:3px}
.traf-range-tabs{display:flex;gap:4px;background:var(--accent-d);padding:3px;border-radius:10px;border:1px solid var(--card-b)}
.traf-range-tab{padding:6px 13px;border-radius:8px;font-size:10.5px;font-weight:700;color:var(--t3);cursor:pointer;transition:.15s;border:none;background:transparent;font-family:inherit}
.traf-range-tab.on{background:var(--accent);color:#fff;box-shadow:0 2px 8px rgba(37,99,235,.2)}
.traf-chart-body{height:320px;margin-top:14px;position:relative}

@media(max-width:900px){.traf-hero{grid-template-columns:1fr 1fr}}
@media(max-width:520px){.traf-hero{grid-template-columns:1fr}.traf-chart-body{height:260px}}
.m-icon{width:34px;height:34px;border-radius:8px;background:var(--accent-d);display:flex;align-items:center;justify-content:center;margin-bottom:11px;color:var(--accent);font-size:17px}
.m-icon.suc{background:var(--green-bg);color:var(--green)}
.m-icon.dan{background:var(--red-bg);color:var(--red)}
.m-icon.pur{background:var(--purple-bg);color:var(--purple)}
.m-label{font-size:10px;color:var(--t3);margin-bottom:4px;font-weight:600;text-transform:uppercase;letter-spacing:.05em}
.m-val{font-size:25px;font-weight:700;color:var(--t1);line-height:1;letter-spacing:-.02em}
.m-unit{font-size:12px;font-weight:400;color:var(--t3)}
.m-sub{font-size:10px;color:var(--t3);margin-top:6px;display:flex;align-items:center;gap:3px}
.vless-box{background:linear-gradient(135deg,var(--bg3) 0%,var(--bg2) 100%);border:1px solid var(--card-b);border-radius:18px;padding:20px 22px;margin-bottom:18px;box-shadow:var(--shadow);position:relative;overflow:hidden;transition:background .3s}
.vless-box::before{content:'';position:absolute;top:-50px;left:-50px;width:180px;height:180px;background:radial-gradient(circle,var(--accent-d),transparent 70%);pointer-events:none}
.vl-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:13px;flex-wrap:wrap;gap:8px}
.vl-title{color:var(--t2);font-size:11px;display:flex;align-items:center;gap:6px;font-weight:700;text-transform:uppercase;letter-spacing:.06em}
.vl-title i{color:var(--accent);font-size:15px}
.vl-code{background:var(--bg);border:1px solid var(--card-b);border-radius:10px;padding:13px 15px;font-size:11px;font-family:ui-monospace,monospace;color:var(--t1);word-break:break-all;line-height:1.8;letter-spacing:.01em}
[data-theme="dark"] .vl-code{background:var(--bg2)!important;color:var(--t1)!important}
.vl-actions{display:flex;gap:8px;margin-top:13px;flex-wrap:wrap}
.btn{font-family:inherit;font-size:12px;font-weight:500;border-radius:9px;padding:8px 14px;cursor:pointer;display:inline-flex;align-items:center;gap:5px;border:none;transition:all .15s;white-space:nowrap}
.btn i{font-size:13px}
.btn:disabled{opacity:.4;cursor:not-allowed}
.btn-p{background:var(--accent);color:#fff;box-shadow:0 4px 14px rgba(37,99,235,.28)}
.btn-p:hover{background:var(--accent2);box-shadow:0 6px 18px rgba(37,99,235,.35)}
.btn-o{background:transparent;border:1px solid var(--card-b);color:var(--t2)}
.btn-o:hover{background:var(--accent-d);border-color:rgba(37,99,235,.18)}
.btn-g{background:var(--accent-d);color:var(--accent2);border:1px solid rgba(37,99,235,.12)}
.btn-g:hover{background:rgba(37,99,235,.16)}
.btn-d{background:var(--red-bg);color:var(--red-t);border:1px solid rgba(220,38,38,.15)}
.btn-d:hover{background:rgba(220,38,38,.15)}
.btn-pur{background:var(--purple-bg);color:var(--purple-t);border:1px solid rgba(99,102,241,.15)}
.btn-pur:hover{background:rgba(99,102,241,.18)}
.btn-amber{background:var(--amber-bg);color:var(--amber-t);border:1px solid rgba(217,119,6,.15)}
.btn-amber:hover{background:rgba(217,119,6,.18)}
.btn-sm{padding:5px 9px;font-size:10.5px;border-radius:7px}
.btn-icon{width:30px;height:30px;padding:0;justify-content:center;border-radius:5px}
.card{background:var(--card);border:1px solid var(--card-b);border-radius:var(--radius);padding:18px 20px;transition:border-color .2s,background .3s}
.card:hover{border-color:var(--card-bh)}
.card-title{font-size:12.5px;font-weight:700;color:var(--t1);margin-bottom:15px;display:flex;align-items:center;gap:7px}
.card-title i{font-size:16px;color:var(--accent)}
.ml-auto{margin-right:auto}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-bottom:16px}
.g3{display:grid;grid-template-columns:2fr 1fr;gap:13px;margin-bottom:16px}
.mb16{margin-bottom:16px}
.sr{display:flex;align-items:center;justify-content:space-between;padding:9px 0;border-bottom:1px solid rgba(37,99,235,0.06);font-size:12px}
.sr:last-child{border-bottom:none}
.sr-k{color:var(--t2);display:flex;align-items:center;gap:6px}
.sr-k i{font-size:13px;color:var(--t3)}
.sr-v{color:var(--t1);font-weight:600;font-size:11.5px}
.ch{position:relative;height:230px}
.ch-lg{position:relative;height:330px}
.ch-sm{position:relative;height:185px}
.exp-chip{font-size:9px;padding:3px 8px;border-radius:6px;font-weight:700;display:inline-flex;align-items:center;gap:3px}
.ec-ok{background:var(--green-bg);color:var(--green-t)}
.ec-warn{background:var(--amber-bg);color:var(--amber-t)}
.ec-exp{background:var(--red-bg);color:var(--red-t)}
.ec-inf{background:var(--accent-d);color:var(--accent2)}
.tog{width:19px;height:34px;border-radius:19px;background:rgba(100,116,139,0.25);position:relative;cursor:pointer;transition:.2s;flex-shrink:0;border:none}
.tog::after{content:'';position:absolute;width:13px;height:13px;border-radius:50%;background:#fff;left:3px;bottom:3px;transition:.2s;box-shadow:0 1px 3px rgba(0,0,0,.3)}
.tog.on{background:var(--green)}
.tog.on::after{bottom:18px}
.form-row{display:flex;gap:9px;flex-wrap:wrap;align-items:flex-end}
.fg{display:flex;flex-direction:column;gap:5px}
.fg label{font-size:10px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.06em}
.fi,.fs{padding:9px 12px;border-radius:9px;border:1px solid var(--card-b);background:rgba(0,0,0,.18);color:var(--t1);font-family:inherit;font-size:12px;outline:none;transition:.15s;min-width:100px}
[data-theme="dark"] .fi,[data-theme="dark"] .fs{background:var(--bg2)!important;color:var(--t1)!important}
.fi::placeholder{color:var(--t3)}
.fi:focus,.fs:focus{border-color:rgba(37,99,235,.45);background:rgba(0,0,0,.25);box-shadow:0 0 0 3px rgba(37,99,235,.08)}
.fs option{background:var(--bg2)}
[data-theme="dark"] .fs option{background:var(--bg2)!important;color:var(--t1)!important}
.cl{background:var(--accent-d);border:1px solid rgba(37,99,235,.12);border-radius:10px;padding:11px 13px;font-size:11px;color:var(--t2);display:flex;gap:9px;align-items:flex-start;line-height:1.8;margin-top:12px}
.cl i{font-size:15px;color:var(--accent);margin-top:1px;flex-shrink:0}
.cl.amber{background:var(--amber-bg);border-color:rgba(217,119,6,.15);color:var(--amber-t)}
/* ══════ پنل ساخت کانفیگ - طراحی جدید ══════ */
.create-panel{background:linear-gradient(155deg,var(--bg3) 0%,var(--card) 55%);border:1px solid var(--card-b);border-radius:22px;padding:0;overflow:hidden;box-shadow:var(--shadow);margin-bottom:16px;position:relative}
.create-panel::before{content:'';position:absolute;top:-60px;left:-60px;width:220px;height:220px;background:radial-gradient(circle,var(--accent-d),transparent 70%);pointer-events:none}
.cp-head{display:flex;align-items:center;gap:13px;padding:22px 24px 18px;position:relative;z-index:1}
.cp-head-icon{width:44px;height:44px;border-radius:13px;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;color:#fff;font-size:20px;flex-shrink:0;box-shadow:0 6px 18px rgba(37,99,235,.2)}
.cp-head-text{flex:1;min-width:0}
.cp-head-title{font-size:15px;font-weight:800;color:var(--t1);letter-spacing:-.01em}
.cp-head-sub{font-size:11px;color:var(--t3);margin-top:2px}
.cp-body{padding:2px 24px 22px;position:relative;z-index:1}
.cp-row{display:grid;grid-template-columns:1.3fr 1fr;gap:14px;margin-bottom:16px}
.cp-block{background:var(--bg);border:1px solid var(--card-b);border-radius:14px;padding:14px 16px}
[data-theme="dark"] .cp-block{background:var(--bg2)!important;color:var(--t1)!important}
.cp-block-label{font-size:10px;font-weight:800;color:var(--t2);text-transform:uppercase;letter-spacing:.08em;display:flex;align-items:center;gap:6px;margin-bottom:11px}
.cp-block-label i{color:var(--accent);font-size:14px}
.cp-input-full{width:100%;padding:10px 13px;border-radius:10px;border:1px solid var(--card-b);background:rgba(0,0,0,.18);color:var(--t1);font-family:inherit;font-size:12.5px;outline:none;transition:.15s}
[data-theme="dark"] .cp-input-full{background:var(--bg2)!important;color:var(--t1)!important}
.cp-input-full:focus{border-color:rgba(37,99,235,.5);box-shadow:0 0 0 3px rgba(37,99,235,.1)}
.cp-input-full::placeholder{color:var(--t3)}
.cp-mini-row{display:flex;gap:8px;margin-top:9px}
.cp-quota-inputs{display:flex;gap:8px}
.cp-quota-inputs .cp-input-full{flex:1}
.cp-quota-inputs select.cp-input-full{flex:0 0 76px}
.chip-row{display:flex;gap:6px;flex-wrap:wrap;margin-top:9px}
.chip{font-size:10.5px;font-weight:700;padding:5px 12px;border-radius:8px;background:var(--accent-d);color:var(--t2);border:1px solid var(--card-b);cursor:pointer;transition:.15s;white-space:nowrap}
.chip:hover{background:rgba(37,99,235,.18);color:var(--accent2)}
.chip.active{background:var(--accent);color:#fff;border-color:var(--accent);box-shadow:0 3px 10px rgba(37,99,235,.2)}
.proto-tabs{display:flex;gap:8px;flex-wrap:wrap}
.proto-step-label{font-size:10px;font-weight:800;color:var(--t2);text-transform:uppercase;letter-spacing:.06em;display:flex;align-items:center;gap:6px;margin-bottom:9px}
.proto-step-label i{color:var(--accent);font-size:14px}

.proto-base-cards{display:grid;grid-template-columns:1fr 1fr;gap:9px}
.proto-base-card{border:1.5px solid var(--card-b);border-radius:13px;padding:14px 12px;cursor:pointer;transition:.18s;text-align:center;position:relative;background:rgba(0,0,0,.1)}
[data-theme="dark"] .proto-base-card{background:var(--bg2)!important;color:var(--t1)!important}
.proto-base-card:hover{border-color:var(--card-bh);transform:translateY(-1px)}
.proto-base-card.active{border-color:var(--accent);background:var(--accent-d);box-shadow:0 0 0 3px rgba(37,99,235,.1)}
.proto-base-icon{width:34px;height:34px;border-radius:9px;background:var(--accent-d);color:var(--accent);display:flex;align-items:center;justify-content:center;font-size:17px;margin:0 auto 8px}
.proto-base-card.active .proto-base-icon{background:var(--accent);color:#fff}
.proto-base-title{font-size:12px;font-weight:800;color:var(--t1)}
.proto-base-desc{font-size:9.5px;color:var(--t3);margin-top:3px}

.proto-transport-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}
.proto-t-card{border:1.5px solid var(--card-b);border-radius:13px;padding:13px 10px;cursor:pointer;transition:.18s;text-align:center;position:relative;background:rgba(0,0,0,.1)}
[data-theme="dark"] .proto-t-card{background:var(--bg2)!important;color:var(--t1)!important}
.proto-t-card:hover{border-color:var(--card-bh);transform:translateY(-1px)}
.proto-t-card.active{border-color:var(--accent);background:var(--accent-d);box-shadow:0 0 0 3px rgba(37,99,235,.1)}
.proto-t-icon{width:30px;height:30px;border-radius:9px;background:var(--accent-d);color:var(--accent);display:flex;align-items:center;justify-content:center;font-size:15px;margin:0 auto 7px}
.proto-t-card.active .proto-t-icon{background:var(--accent);color:#fff}
.proto-t-title{font-size:10.5px;font-weight:800;color:var(--t1)}
.proto-t-desc{font-size:9px;color:var(--t3);margin-top:3px;line-height:1.4}

@media(max-width:760px){
  .proto-transport-cards{grid-template-columns:1fr}
}
.proto-tab{flex:1;min-width:120px;display:flex;align-items:center;justify-content:center;gap:7px;
  padding:11px 10px;border-radius:12px;border:1.5px solid var(--card-b);background:rgba(0,0,0,.1);
  color:var(--t2);font-family:inherit;font-size:11.5px;font-weight:700;cursor:pointer;transition:.15s}
.proto-tab.active{border-color:var(--accent);background:var(--accent-d);color:var(--accent2);
  box-shadow:0 0 0 3px rgba(37,99,235,.1)}
.proto-submodes{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}
.proto-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}
.proto-card{border:1.5px solid var(--card-b);border-radius:13px;padding:13px 12px;cursor:pointer;transition:.18s;text-align:center;position:relative;background:rgba(0,0,0,.1)}
[data-theme="dark"] .proto-card{background:var(--bg2)!important;color:var(--t1)!important}
.proto-card:hover{border-color:var(--card-bh);transform:translateY(-1px)}
.proto-card.active{border-color:var(--accent);background:var(--accent-d);box-shadow:0 0 0 3px rgba(37,99,235,.1)}
.proto-card.active .proto-card-check{opacity:1;transform:scale(1)}
.proto-card-check{position:absolute;top:7px;left:7px;width:16px;height:16px;border-radius:50%;background:var(--accent);color:#fff;font-size:10px;display:flex;align-items:center;justify-content:center;opacity:0;transform:scale(.5);transition:.18s}
.proto-card-icon{width:32px;height:32px;border-radius:9px;background:var(--accent-d);color:var(--accent);display:flex;align-items:center;justify-content:center;font-size:16px;margin:0 auto 8px}
.proto-card.active .proto-card-icon{background:var(--accent);color:#fff}
.proto-card-title{font-size:11px;font-weight:800;color:var(--t1)}
.proto-card-desc{font-size:9px;color:var(--t3);margin-top:3px;line-height:1.5}
.cp-footer{display:flex;align-items:center;justify-content:space-between;gap:12px;padding-top:16px;border-top:1px solid var(--card-b);flex-wrap:wrap}
.cp-footer-note{display:flex;align-items:center;gap:8px;font-size:10.5px;color:var(--t3);line-height:1.7;flex:1;min-width:220px}
.cp-footer-note i{color:var(--accent);font-size:15px;flex-shrink:0}
.cp-submit-btn{background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;border:none;border-radius:13px;padding:13px 26px;font-family:inherit;font-size:13px;font-weight:800;cursor:pointer;display:flex;align-items:center;gap:8px;box-shadow:0 6px 20px rgba(37,99,235,.2);transition:.18s;white-space:nowrap}
.cp-submit-btn:hover{transform:translateY(-2px);box-shadow:0 10px 26px rgba(37,99,235,.45)}
.cp-submit-btn:active{transform:translateY(0) scale(.98)}
@media(max-width:760px){
  .cp-row{grid-template-columns:1fr}
  .proto-cards{grid-template-columns:1fr}
  .cp-footer{flex-direction:column;align-items:stretch}
  .cp-submit-btn{justify-content:center}
}
/* ══════ پنل اطلاعات سرور ══════ */
.srv-panel{background:linear-gradient(155deg,var(--bg3) 0%,var(--card) 60%);border:1px solid var(--card-b);border-radius:22px;overflow:hidden;box-shadow:var(--shadow);position:relative}
.srv-panel::before{content:'';position:absolute;top:-60px;left:-60px;width:200px;height:200px;background:radial-gradient(circle,var(--accent-d),transparent 70%);pointer-events:none}
.srv-hero{display:flex;align-items:center;gap:14px;padding:22px 24px;position:relative;z-index:1;border-bottom:1px solid var(--card-b)}
.srv-hero-icon{width:50px;height:50px;border-radius:14px;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;color:#fff;font-size:22px;flex-shrink:0;box-shadow:0 6px 18px rgba(37,99,235,.2)}
.srv-hero-text{flex:1;min-width:0}
.srv-hero-domain{font-size:15px;font-weight:800;color:var(--t1);word-break:break-all}
.srv-hero-sub{font-size:10.5px;color:var(--t3);margin-top:4px;display:flex;align-items:center;gap:6px}
.srv-tiles{display:grid;grid-template-columns:1fr 1fr;gap:11px;padding:20px 22px 22px;position:relative;z-index:1}
.srv-tile{display:flex;align-items:center;gap:11px;background:var(--bg);border:1px solid var(--card-b);border-radius:13px;padding:12px 14px;transition:.18s}
[data-theme="dark"] .srv-tile{background:var(--bg2)!important;color:var(--t1)!important}
.srv-tile:hover{border-color:var(--card-bh);transform:translateY(-1px)}
.srv-tile-icon{width:34px;height:34px;border-radius:10px;background:var(--accent-d);color:var(--accent);display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0}
.srv-tile-text{min-width:0}
.srv-tile-label{font-size:9.5px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.05em;margin-bottom:3px}
.srv-tile-val{font-size:12px;font-weight:700;color:var(--t1);word-break:break-word}

/* ══════ پنل تغییر رمز ══════ */
.pw-panel{background:linear-gradient(155deg,var(--bg3) 0%,var(--card) 60%);border:1px solid var(--card-b);border-radius:22px;overflow:hidden;box-shadow:var(--shadow);position:relative}
.pw-panel::before{content:'';position:absolute;top:-60px;right:-60px;width:200px;height:200px;background:radial-gradient(circle,var(--purple-bg),transparent 70%);pointer-events:none}
.pw-hero{display:flex;align-items:center;gap:14px;padding:22px 24px 18px;position:relative;z-index:1}
.pw-hero-icon{width:50px;height:50px;border-radius:14px;background:linear-gradient(135deg,var(--purple),var(--purple));display:flex;align-items:center;justify-content:center;color:#fff;font-size:22px;flex-shrink:0;box-shadow:0 6px 18px rgba(99,102,241,.2)}
.pw-hero-text{flex:1;min-width:0}
.pw-hero-title{font-size:15px;font-weight:800;color:var(--t1)}
.pw-hero-sub{font-size:10.5px;color:var(--t3);margin-top:3px}
.pw-body{padding:2px 24px 22px;position:relative;z-index:1}
.pw-field{position:relative;margin-bottom:13px}
.pw-field label{display:block;font-size:10px;font-weight:700;color:var(--t2);text-transform:uppercase;letter-spacing:.06em;margin-bottom:7px}
.pw-input{width:100%;padding:11px 42px 11px 14px;border-radius:11px;border:1px solid var(--card-b);background:rgba(0,0,0,.18);color:var(--t1);font-family:inherit;font-size:12.5px;outline:none;transition:.15s}
[data-theme="dark"] .pw-input{background:var(--bg2)!important;color:var(--t1)!important}
.pw-input:focus{border-color:rgba(99,102,241,.5);box-shadow:0 0 0 3px rgba(99,102,241,.1)}
.pw-eye{position:absolute;left:12px;top:34px;background:none;border:none;color:var(--t3);cursor:pointer;font-size:16px;padding:4px;display:flex}
.pw-eye:hover{color:var(--purple)}
.pw-strength{height:4px;border-radius:3px;background:var(--accent-d);margin-top:8px;overflow:hidden;display:flex;gap:3px}
.pw-strength-seg{flex:1;height:100%;border-radius:3px;background:rgba(100,116,139,.2);transition:.25s}
.pw-strength-label{font-size:9.5px;color:var(--t3);margin-top:5px;display:flex;align-items:center;gap:5px}
.pw-reqs{display:flex;flex-wrap:wrap;gap:6px;margin-top:11px;margin-bottom:16px}
.pw-req{font-size:9.5px;padding:4px 10px;border-radius:7px;background:var(--accent-d);color:var(--t3);font-weight:600;display:flex;align-items:center;gap:4px;transition:.18s}
.pw-req.met{background:var(--green-bg);color:var(--green-t)}
.pw-submit{width:100%;justify-content:center;background:linear-gradient(135deg,var(--purple),var(--purple));color:#fff;border:none;border-radius:12px;padding:12px;font-family:inherit;font-size:13px;font-weight:800;cursor:pointer;display:flex;align-items:center;gap:8px;box-shadow:0 6px 18px rgba(99,102,241,.32);transition:.18s}
.pw-submit:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(99,102,241,.42)}
.pw-submit:active{transform:translateY(0) scale(.98)}

/* ══════ اتصالات فعال - نسخه پیشرفته ══════ */
.conn-hero{display:grid;grid-template-columns:repeat(6,1fr);gap:12px;margin-bottom:18px}
.conn-hero-tile{background:var(--card);border:1px solid var(--card-b);border-radius:16px;padding:16px 18px;position:relative;overflow:hidden;transition:.2s}
.conn-hero-tile:hover{border-color:var(--card-bh);transform:translateY(-2px);box-shadow:var(--shadow)}
.conn-hero-tile::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--green),transparent)}
.conn-hero-icon{width:32px;height:32px;border-radius:9px;background:var(--green-bg);color:var(--green-t);display:flex;align-items:center;justify-content:center;font-size:15px;margin-bottom:10px}
.conn-hero-tile:nth-child(2) .conn-hero-icon{background:var(--accent-d);color:var(--accent)}
.conn-hero-tile:nth-child(3) .conn-hero-icon{background:var(--purple-bg);color:var(--purple)}
.conn-hero-tile:nth-child(4) .conn-hero-icon{background:var(--amber-bg);color:var(--amber)}
.conn-hero-label{font-size:9.5px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px}
.conn-hero-val{font-size:21px;font-weight:800;color:var(--t1);line-height:1;letter-spacing:-.02em}
.conn-hero-unit{font-size:11px;color:var(--t3);font-weight:500}

.conn-toolbar{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:14px;flex-wrap:wrap}
.conn-toolbar-title{font-size:12px;font-weight:800;color:var(--t2);display:flex;align-items:center;gap:7px;text-transform:uppercase;letter-spacing:.06em}
.conn-toolbar-title i{color:var(--green);font-size:15px}
.conn-live-badge{display:flex;align-items:center;gap:6px;font-size:10.5px;font-weight:700;color:var(--green-t);background:var(--green-bg);padding:5px 12px;border-radius:20px;border:1px solid rgba(16,185,129,.2)}
.conn-live-dot{width:6px;height:6px;border-radius:50%;background:var(--green);animation:pulse 1.6s infinite}

.conn-grid-v2{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.conn-card-v2{background:var(--card);border:1px solid var(--card-b);border-radius:18px;padding:0;overflow:hidden;transition:all .22s cubic-bezier(.4,0,.2,1);position:relative}
.conn-card-v2:hover{border-color:var(--card-bh);transform:translateY(-3px);box-shadow:0 14px 32px rgba(0,0,0,.22)}
.conn-card-v2-glow{position:absolute;top:-40px;left:-40px;width:140px;height:140px;background:radial-gradient(circle,rgba(16,185,129,.1),transparent 70%);pointer-events:none}
.conn-card-v2-top{display:flex;align-items:center;gap:12px;padding:16px 17px 13px;position:relative;z-index:1}
.conn-avatar{width:42px;height:42px;border-radius:13px;background:linear-gradient(135deg,var(--green),#0D9668);display:flex;align-items:center;justify-content:center;color:#fff;font-size:18px;flex-shrink:0;position:relative;box-shadow:0 4px 14px rgba(16,185,129,.3)}
.conn-avatar::after{content:'';position:absolute;inset:-4px;border-radius:16px;border:1.5px solid var(--green);opacity:.4;animation:breathe2 2.4s ease-in-out infinite}
@keyframes breathe2{0%,100%{transform:scale(1);opacity:.4}50%{transform:scale(1.12);opacity:0}}
.conn-card-v2-id{flex:1;min-width:0}
.conn-ip-v2{font-family:ui-monospace,monospace;font-size:14px;font-weight:800;color:var(--t1);display:flex;align-items:center;gap:6px}
.conn-ip-copy{background:none;border:none;color:var(--t3);cursor:pointer;font-size:12px;padding:2px;display:flex;transition:.15s}
.conn-ip-copy:hover{color:var(--accent)}
.conn-label-v2{font-size:10.5px;color:var(--t3);margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.conn-status-pill{font-size:9px;font-weight:800;padding:4px 9px;border-radius:20px;background:var(--green-bg);color:var(--green-t);display:flex;align-items:center;gap:4px;white-space:nowrap;flex-shrink:0}
.conn-card-v2-divider{height:1px;background:linear-gradient(90deg,transparent,var(--card-b) 15%,var(--card-b) 85%,transparent);margin:0 17px}
.conn-card-v2-body{padding:14px 17px 16px}
.conn-proto-row{margin-bottom:12px}
.conn-stat-row{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px}
.conn-stat-box{display:flex;align-items:center;gap:8px}
.conn-stat-icon{width:26px;height:26px;border-radius:8px;background:var(--accent-d);color:var(--accent);display:flex;align-items:center;justify-content:center;font-size:12px;flex-shrink:0}
.conn-stat-icon.time{background:var(--purple-bg);color:var(--purple)}
.conn-stat-text-label{font-size:8.5px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.04em}
.conn-stat-text-val{font-size:11.5px;font-weight:700;color:var(--t1);margin-top:1px}
.conn-duration-track{height:5px;border-radius:4px;background:var(--accent-d);overflow:hidden;position:relative}
.conn-duration-fill{height:100%;border-radius:4px;background:linear-gradient(90deg,var(--green),#3FD79C);position:relative;overflow:hidden}
.conn-duration-fill::after{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(255,255,255,.35),transparent);width:40%;animation:shimmer 1.8s linear infinite}
@keyframes shimmer{0%{transform:translateX(-120%)}100%{transform:translateX(280%)}}

.conn-empty-v2{text-align:center;padding:70px 20px;background:var(--card);border:1px dashed var(--card-b);border-radius:20px}
.conn-empty-v2-icon{width:64px;height:64px;border-radius:18px;background:var(--accent-d);display:flex;align-items:center;justify-content:center;font-size:28px;color:var(--t3);margin:0 auto 16px}
.conn-empty-v2-title{font-size:13.5px;font-weight:700;color:var(--t2);margin-bottom:5px}
.conn-empty-v2-sub{font-size:11px;color:var(--t3)}

@media(max-width:760px){.conn-hero{grid-template-columns:1fr 1fr}}
@media(max-width:500px){.conn-grid-v2{grid-template-columns:1fr}}

@media(max-width:560px){.srv-tiles{grid-template-columns:1fr}}
.cl.amber i{color:var(--amber)}
.sub-box{background:rgba(99,102,241,.07);border:1px solid rgba(99,102,241,.15);border-radius:10px;padding:14px 16px;display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-top:11px}
.sub-url{font-family:ui-monospace,monospace;font-size:10.5px;color:var(--purple-t);word-break:break-all;flex:1}
.spbar{height:4px;border-radius:3px;background:var(--accent-d);margin-top:5px;overflow:hidden}
.spfill{height:100%;border-radius:3px;background:linear-gradient(90deg,var(--accent),var(--accent2));transition:width 1s}
.empty{text-align:center;padding:50px 20px;color:var(--t3)}
.empty i{font-size:40px;opacity:.3;margin-bottom:12px;display:block}
.empty p{font-size:12.5px;margin-top:4px}
/* ══════ گروه‌های ساب - ریدیزاین کامل ══════ */
.subs-toolbar{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:16px;flex-wrap:wrap}
.subs-search{flex:1;min-width:200px;position:relative}
.subs-search input{width:100%;padding:11px 40px 11px 15px;border-radius:12px;border:1px solid var(--card-b);background:var(--card);color:var(--t1);font-family:inherit;font-size:12.5px;outline:none;transition:.15s}
.subs-search input:focus{border-color:rgba(99,102,241,.5);box-shadow:0 0 0 3px rgba(99,102,241,.1)}
.subs-search i{position:absolute;left:14px;top:50%;transform:translateY(-50%);color:var(--t3);font-size:15px}

.sub-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:16px;margin-bottom:18px}
.sub-card{background:var(--card);border:1px solid var(--card-b);border-radius:20px;padding:0;overflow:hidden;transition:all .25s cubic-bezier(.4,0,.2,1);position:relative}
.sub-card:hover{border-color:var(--card-bh);transform:translateY(-4px);box-shadow:0 16px 36px rgba(0,0,0,.24)}
.sub-card-top{background:linear-gradient(155deg,var(--purple-bg) 0%,transparent 65%);padding:20px 20px 16px;position:relative}
.sub-card-top::before{content:'';position:absolute;top:-30px;left:-30px;width:130px;height:130px;background:radial-gradient(circle,rgba(99,102,241,.14),transparent 70%);pointer-events:none}
.sub-card-head-v2{display:flex;align-items:flex-start;gap:13px;position:relative;z-index:1}
.sub-card-icon{width:46px;height:46px;border-radius:14px;background:linear-gradient(135deg,var(--purple),var(--purple));display:flex;align-items:center;justify-content:center;color:#fff;font-size:20px;flex-shrink:0;box-shadow:0 6px 16px rgba(99,102,241,.2)}
.sub-card-titles{flex:1;min-width:0}
.sub-card-name-v2{font-size:15.5px;font-weight:800;color:var(--t1);letter-spacing:-.01em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sub-card-desc-v2{font-size:11px;color:var(--t3);margin-top:3px;line-height:1.6;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.sub-card-lock-badge{flex-shrink:0;width:26px;height:26px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:12px}
.sub-card-lock-badge.locked{background:var(--amber-bg);color:var(--amber-t)}
.sub-card-lock-badge.open{background:var(--green-bg);color:var(--green-t)}

.sub-card-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:0;position:relative;z-index:1;margin-top:16px;background:var(--bg);border:1px solid var(--card-b);border-radius:13px;overflow:hidden}
[data-theme="dark"] .sub-card-stats{background:rgba(99,102,241,.06)}
.sub-card-stat{padding:11px 8px;text-align:center;border-left:1px solid var(--card-b)}
.sub-card-stat:last-child{border-left:none}
.sub-card-stat-val{font-size:15px;font-weight:800;color:var(--t1);line-height:1.2}
.sub-card-stat-label{font-size:8.5px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.05em;margin-top:4px}

.sub-card-url-row{margin:14px 20px 0;background:rgba(99,102,241,.08);border:1px dashed rgba(99,102,241,.25);border-radius:11px;padding:9px 12px;display:flex;align-items:center;gap:8px}
.sub-card-url-text{font-family:ui-monospace,monospace;font-size:9.5px;color:var(--purple-t);flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sub-card-url-copy{background:none;border:none;color:var(--purple);cursor:pointer;font-size:13px;padding:3px;display:flex;flex-shrink:0;transition:.15s}
.sub-card-url-copy:hover{color:var(--purple-t);transform:scale(1.1)}

.sub-card-bottom{padding:14px 20px 18px;display:flex;gap:7px;flex-wrap:wrap}
.sub-card-bottom .btn{flex:1;justify-content:center;min-width:fit-content}

.subs-empty-v2{text-align:center;padding:70px 20px;background:var(--card);border:1px dashed var(--card-b);border-radius:20px;grid-column:1/-1}
.subs-empty-v2-icon{width:64px;height:64px;border-radius:18px;background:var(--purple-bg);display:flex;align-items:center;justify-content:center;font-size:28px;color:var(--purple);margin:0 auto 16px}
.subs-empty-v2-title{font-size:13.5px;font-weight:700;color:var(--t2);margin-bottom:5px}
.subs-empty-v2-sub{font-size:11px;color:var(--t3)}

/* ══════ مودال ساخت گروه - نسخه فشرده ══════ */
.modal-v2{background:var(--card);border:1px solid var(--card-b);border-radius:22px;padding:0;max-width:430px;width:calc(100% - 32px);max-height:92vh;overflow-y:auto;position:relative;animation:fi .2s ease;box-shadow:0 24px 70px rgba(0,0,0,.5)}
.modal-v2-head{background:linear-gradient(155deg,rgba(99,102,241,.14) 0%,transparent 65%);padding:18px 22px 14px;position:relative;overflow:hidden}
.modal-v2-head::before{content:'';position:absolute;top:-50px;left:-50px;width:160px;height:160px;background:radial-gradient(circle,rgba(99,102,241,.15),transparent 70%);pointer-events:none}
.modal-v2-close{position:absolute;top:14px;left:14px;background:var(--accent-d);border:1px solid var(--card-b);color:var(--t2);width:30px;height:30px;border-radius:9px;font-size:15px;display:flex;align-items:center;justify-content:center;cursor:pointer;z-index:2;transition:.15s}
.modal-v2-close:hover{background:var(--red-bg);color:var(--red-t);border-color:rgba(239,68,68,.25)}
.modal-v2-icon{width:42px;height:42px;border-radius:13px;background:linear-gradient(135deg,var(--purple),var(--purple));display:flex;align-items:center;justify-content:center;color:#fff;font-size:19px;margin-bottom:10px;position:relative;z-index:1;box-shadow:0 8px 18px rgba(99,102,241,.4)}
.modal-v2-title{font-size:15.5px;font-weight:800;color:var(--t1);position:relative;z-index:1;letter-spacing:-.01em}
.modal-v2-sub{font-size:10.5px;color:var(--t3);margin-top:3px;position:relative;z-index:1;line-height:1.6}
.modal-v2-body{padding:16px 22px 20px;border-top:1px solid var(--card-b)}
.modal-v2-field{margin-bottom:11px}
.modal-v2-field label{display:flex;align-items:center;gap:5px;font-size:9.5px;font-weight:800;color:var(--t2);text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px}
.modal-v2-field label i{color:var(--purple);font-size:13px}
.modal-v2-input-wrap{position:relative}
.modal-v2-input-wrap>i{position:absolute;right:13px;top:50%;transform:translateY(-50%);color:var(--t3);font-size:14px;pointer-events:none;transition:.15s;z-index:1}
.modal-v2-input{width:100%;padding:9px 38px 9px 13px;border-radius:11px;border:1px solid var(--card-b);background:rgba(0,0,0,.2);color:var(--t1);font-family:inherit;font-size:12.5px;outline:none;transition:.18s}
[data-theme="dark"] .modal-v2-input{background:var(--bg2)!important;color:var(--t1)!important}
.modal-v2-input::placeholder{color:var(--t3)}
.modal-v2-input:focus{border-color:rgba(99,102,241,.55);box-shadow:0 0 0 3px rgba(99,102,241,.12);background:rgba(0,0,0,.28)}
[data-theme="dark"] .modal-v2-input:focus{background:var(--bg2)!important;color:var(--t1)!important}
.modal-v2-input:focus~i{color:var(--purple)}
.modal-v2-hint{background:rgba(37,99,235,.08);border:1px solid rgba(37,99,235,.18);border-radius:11px;padding:9px 12px;font-size:10px;color:var(--t2);display:flex;gap:7px;align-items:flex-start;line-height:1.6;margin-top:2px}
.modal-v2-hint i{font-size:14px;color:var(--accent);margin-top:1px;flex-shrink:0}
.modal-v2-footer{display:flex;gap:8px;margin-top:15px}
.modal-v2-btn-cancel{flex:.75;justify-content:center;padding:10px;border-radius:11px;background:transparent;border:1px solid var(--card-b);color:var(--t2);font-family:inherit;font-size:12px;font-weight:700;cursor:pointer;transition:.15s;display:flex;align-items:center}
.modal-v2-btn-cancel:hover{background:var(--accent-d);color:var(--t1)}
.modal-v2-btn-submit{flex:1;justify-content:center;padding:10px;border-radius:11px;background:linear-gradient(135deg,var(--purple),var(--purple));color:#fff;border:none;font-family:inherit;font-size:12px;font-weight:800;cursor:pointer;display:flex;align-items:center;gap:6px;box-shadow:0 6px 18px rgba(99,102,241,.4);transition:.18s}
.modal-v2-btn-submit:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(99,102,241,.5)}
.modal-v2-btn-submit:active{transform:translateY(0) scale(.98)}

/* ══════ مودال انتخاب کانفیگ - نسخه پیشرفته ══════ */
.lmodal-head{background:linear-gradient(155deg,var(--accent-d) 0%,transparent 70%);padding:22px 24px 18px;position:relative;border-bottom:1px solid var(--card-b)}
.lmodal-icon-row{display:flex;align-items:center;gap:12px;position:relative;z-index:1}
.lmodal-icon{width:44px;height:44px;border-radius:13px;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;color:#fff;font-size:19px;flex-shrink:0;box-shadow:0 6px 16px rgba(37,99,235,.2)}
.lmodal-title-v2{font-size:14.5px;font-weight:800;color:var(--t1)}
.lmodal-sub-v2{font-size:10.5px;color:var(--t3);margin-top:2px}
.lmodal-search{margin-top:14px;position:relative}
.lmodal-search input{width:100%;padding:10px 38px 10px 13px;border-radius:11px;border:1px solid var(--card-b);background:rgba(0,0,0,.2);color:var(--t1);font-family:inherit;font-size:12px;outline:none}
[data-theme="dark"] .lmodal-search input{background:var(--bg2)!important;color:var(--t1)!important}
.lmodal-search input:focus{border-color:rgba(37,99,235,.5);box-shadow:0 0 0 3px rgba(37,99,235,.1)}
.lmodal-search i{position:absolute;left:12px;top:50%;transform:translateY(-50%);color:var(--t3);font-size:14px}
.lmodal-quickbar{display:flex;gap:8px;margin-top:11px;position:relative;z-index:1}
.lmodal-qbtn{font-size:10px;font-weight:700;padding:5px 11px;border-radius:8px;background:var(--accent-d);color:var(--accent2);border:1px solid var(--card-b);cursor:pointer;transition:.15s;font-family:inherit}
.lmodal-qbtn:hover{background:rgba(37,99,235,.2)}
.lmodal-count{margin-right:auto;font-size:10.5px;color:var(--t3);display:flex;align-items:center}

.lmodal-list{padding:10px 14px;max-height:360px;overflow-y:auto}
.lrow-v2{display:flex;align-items:center;gap:11px;padding:11px 12px;border-radius:13px;cursor:pointer;transition:.15s;margin-bottom:4px;border:1px solid transparent}
.lrow-v2:hover{background:var(--accent-d)}
.lrow-v2.checked{background:rgba(37,99,235,.1);border-color:rgba(37,99,235,.25)}
.lrow-v2-check{width:20px;height:20px;border-radius:7px;border:2px solid var(--card-b);flex-shrink:0;display:flex;align-items:center;justify-content:center;transition:.15s;background:var(--bg)}
.lrow-v2.checked .lrow-v2-check{background:var(--accent);border-color:var(--accent)}
.lrow-v2-check i{font-size:12px;color:#fff;opacity:0;transform:scale(.5);transition:.15s}
.lrow-v2.checked .lrow-v2-check i{opacity:1;transform:scale(1)}
.lrow-v2-avatar{width:34px;height:34px;border-radius:10px;background:var(--accent-d);color:var(--accent);display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0}
.lrow-v2.checked .lrow-v2-avatar{background:var(--accent);color:#fff}
.lrow-v2-info{flex:1;min-width:0}
.lrow-v2-name{font-size:12.5px;font-weight:700;color:var(--t1);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lrow-v2-meta{font-size:9.5px;color:var(--t3);margin-top:2px;display:flex;align-items:center;gap:6px}
.lrow-v2-status{font-size:9px;font-weight:800;padding:3px 9px;border-radius:20px;flex-shrink:0;white-space:nowrap}
.lrow-v2-status.on{background:var(--green-bg);color:var(--green-t)}
.lrow-v2-status.off{background:var(--red-bg);color:var(--red-t)}

.lmodal-footer{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:16px 24px;border-top:1px solid var(--card-b)}
.lmodal-footer-info{font-size:10.5px;color:var(--t3);display:flex;align-items:center;gap:6px}
.lmodal-footer-info i{color:var(--accent)}
.lmodal-footer-btns{display:flex;gap:8px}

@media(max-width:500px){.sub-grid{grid-template-columns:1fr}.sub-card-stats{grid-template-columns:repeat(3,1fr)}}

.modal-bg{display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:500;align-items:center;justify-content:center;backdrop-filter:blur(4px)}
.modal-bg.open{display:flex}
.modal{background:var(--card);border:1px solid var(--card-b);border-radius:20px;padding:28px 26px;max-width:520px;width:calc(100% - 32px);max-height:90vh;overflow-y:auto;position:relative;animation:fi .2s ease}
.modal-close{position:absolute;top:14px;left:14px;background:var(--accent-d);border:1px solid var(--card-b);color:var(--t2);width:30px;height:30px;border-radius:8px;font-size:16px;display:flex;align-items:center;justify-content:center;cursor:pointer;border:none}
.modal-title{font-size:16px;font-weight:700;color:var(--t1);margin-bottom:18px;display:flex;align-items:center;gap:8px}
.modal-title i{color:var(--accent)}
.lrow{display:flex;align-items:center;gap:8px;padding:7px 0;border-bottom:1px solid rgba(37,99,235,.05)}
.lrow:last-child{border-bottom:none}
.lrow-check{width:16px;height:16px;border-radius:4px;cursor:pointer;accent-color:var(--accent)}
.lrow-label{flex:1;font-size:12px;color:var(--t1)}
.lrow-badge{font-size:9px;padding:2px 7px;border-radius:5px;background:var(--green-bg);color:var(--green-t);font-weight:700}
.toast{position:fixed;bottom:22px;left:50%;transform:translateX(-50%) translateY(40px);background:var(--card);border:1px solid var(--card-b);color:var(--t1);border-radius:10px;padding:10px 18px;font-size:12.5px;opacity:0;transition:all .25s;z-index:999;pointer-events:none;display:flex;align-items:center;gap:8px;box-shadow:var(--shadow);white-space:nowrap}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.toast.ok{border-color:rgba(16,185,129,.3);background:var(--green-bg);color:var(--green-t)}
.toast.err{border-color:rgba(239,68,68,.3);background:var(--red-bg);color:var(--red-t)}
/* ══════ نوار اعلان‌های همگانی ══════ */
.ann-banner-wrap{display:flex;flex-direction:column;gap:10px;margin-bottom:18px}
.ann-card{position:relative;display:flex;gap:13px;background:var(--card);border:1px solid var(--card-b);border-radius:16px;padding:15px 44px 15px 17px;box-shadow:var(--shadow);animation:fi .25s ease;overflow:hidden}
.ann-card::before{content:'';position:absolute;top:0;right:0;width:4px;height:100%}
.ann-card.news::before{background:var(--accent)}
.ann-card.ad::before{background:var(--purple)}
.ann-card.warning::before{background:var(--amber)}
.ann-card.urgent::before{background:var(--red)}
.ann-icon{width:38px;height:38px;border-radius:11px;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0}
.ann-card.news .ann-icon{background:var(--accent-d);color:var(--accent2)}
.ann-card.ad .ann-icon{background:var(--purple-bg);color:var(--purple)}
.ann-card.warning .ann-icon{background:var(--amber-bg);color:var(--amber-t)}
.ann-card.urgent .ann-icon{background:var(--red-bg);color:var(--red-t)}
.ann-body{flex:1;min-width:0}
.ann-title{font-size:13px;font-weight:700;color:var(--t1);margin-bottom:4px}
.ann-text{font-size:12px;color:var(--t2);line-height:1.8}
.ann-img{max-width:100%;border-radius:10px;margin-top:10px;border:1px solid var(--card-b);display:block}
.ann-close{position:absolute;top:10px;left:10px;width:24px;height:24px;border-radius:7px;background:var(--accent-d);border:none;color:var(--t3);font-size:13px;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:.15s}
.ann-close:hover{background:var(--red-bg);color:var(--red-t)}
.dash-footer{border-top:1px solid var(--card-b);margin-top:14px;padding-top:14px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px}
.df-text{font-size:10px;color:var(--t3)}
.df-link{font-size:11.5px;color:var(--accent2);display:flex;align-items:center;gap:5px;font-weight:600}

.info-strip{display:flex;align-items:center;background:var(--card);border:1px solid var(--card-b);border-radius:16px;padding:16px 22px;margin-bottom:16px;gap:0;flex-wrap:wrap;box-shadow:var(--shadow)}
.info-item{display:flex;flex-direction:column;gap:6px;flex:1;min-width:130px;padding:0 18px;position:relative}
.info-item:not(:first-child)::before{content:'';position:absolute;right:0;top:2px;bottom:2px;width:1px;background:var(--card-b)}
.info-item-label{font-size:10.5px;color:var(--t3);font-weight:700}
.info-item-val{display:flex;align-items:center;gap:7px;font-size:15px;font-weight:800;color:var(--t1);letter-spacing:-.01em}
.info-item-val i{color:var(--accent);font-size:16px}
.info-item-val .info-badge{font-size:11px;font-weight:800;background:var(--green-bg);color:var(--green-t);padding:2px 9px;border-radius:20px}
@media(max-width:760px){.info-strip{gap:14px}.info-item{min-width:45%;padding:0 0 10px}.info-item:not(:first-child)::before{display:none}}

/* ══════ کانفیگ‌ها - طراحی ردیفی حرفه‌ای ══════ */
.cfg-grid{display:flex;flex-direction:column;gap:10px}
.cfg-card{background:var(--card);border:1px solid var(--card-b);border-radius:14px;padding:0;transition:all .2s cubic-bezier(.4,0,.2,1);position:relative;overflow:hidden}
.cfg-card:hover{border-color:var(--card-bh);box-shadow:0 6px 24px rgba(0,0,0,.18)}
.cfg-card.is-off{opacity:.6}
.cfg-card.is-exp{opacity:.78}
.cfg-row{display:flex;align-items:center;gap:16px;padding:14px 18px}
.cfg-status-dot{width:9px;height:9px;border-radius:50%;background:var(--green);flex-shrink:0;box-shadow:0 0 0 3px var(--green-bg)}
.cfg-card.is-off .cfg-status-dot{background:var(--red);box-shadow:0 0 0 3px var(--red-bg)}
.cfg-card.is-exp .cfg-status-dot{background:var(--amber);box-shadow:0 0 0 3px var(--amber-bg)}
.cfg-identity{display:flex;flex-direction:column;gap:3px;min-width:150px;flex-shrink:0}
.cfg-label{font-size:13.5px;font-weight:700;color:var(--t1);display:flex;align-items:center;gap:7px}
.cfg-sub-meta{display:flex;align-items:center;gap:8px;font-size:10px;color:var(--t3)}
.cfg-uuid-mini{font-family:ui-monospace,monospace;font-size:9.5px;color:var(--accent2);background:var(--accent-d);padding:2px 7px;border-radius:5px;cursor:pointer;transition:.15s}
.cfg-uuid-mini:hover{background:rgba(37,99,235,.2)}
.cfg-divider-v{width:1px;align-self:stretch;background:var(--card-b);flex-shrink:0}
.cfg-usage-col{flex:1;min-width:160px;display:flex;flex-direction:column;gap:5px}
.ubar{height:5px;border-radius:4px;background:rgba(37,99,235,0.1);overflow:hidden}
.ubar-f{height:100%;border-radius:4px;transition:width .4s ease}
.utxt{font-size:10px;color:var(--t3);display:flex;justify-content:space-between}
.cfg-exp-col{flex-shrink:0;min-width:110px}
.cfg-badges-col{display:flex;flex-direction:column;gap:5px;flex-shrink:0;align-items:flex-end}
.cfg-actions{display:flex;gap:5px;flex-shrink:0}
.proto-chip{font-size:9px;padding:3px 8px;border-radius:6px;font-weight:700;white-space:nowrap}
.pc-ws{background:var(--accent-d);color:var(--accent2)}
.pc-xhttp{background:var(--purple-bg);color:var(--purple-t)}
.pc-ultra{background:var(--green-bg);color:var(--green-t)}
.cfg-sub-tag{font-size:9.5px;color:var(--t3);display:flex;align-items:center;gap:4px;white-space:nowrap}
.cfg-sub-tag i{color:var(--purple);font-size:11px}
.tog{width:19px;height:30px;border-radius:19px;background:rgba(100,116,139,0.25);position:relative;cursor:pointer;transition:.2s;flex-shrink:0;border:none}
.tog::after{content:'';position:absolute;width:13px;height:13px;border-radius:50%;background:#fff;left:3px;top:3px;transition:.2s;box-shadow:0 1px 3px rgba(0,0,0,.3)}
.tog.on::after{top:14px}
.tog.on{background:var(--green)}

@media(max-width:880px){
  .cfg-row{flex-wrap:wrap}
  .cfg-divider-v{display:none}
  .cfg-usage-col{min-width:100%;order:5}
}

/* ── زیر ۷۶۸px: تبدیل کامل به کارت موبایل ── */
@media(max-width:768px){
  .cfg-grid{display:grid;grid-template-columns:1fr;gap:13px}
  .cfg-card{border-radius:16px}
  .cfg-row{flex-direction:column;align-items:stretch;gap:12px;padding:16px}
  .cfg-row-top{display:flex;align-items:center;justify-content:space-between;gap:10px}
  .cfg-identity{min-width:0;flex:1}
  .cfg-usage-col{min-width:0}
  .cfg-exp-col{min-width:0}
  .cfg-badges-col{flex-direction:row;align-items:center;flex-wrap:wrap}
  .cfg-actions{flex-wrap:wrap;border-top:1px solid var(--card-b);padding-top:10px;margin-top:2px;width:100%}
}

/* ══════ اتصالات فعال با IP ══════ */
.conn-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}
.conn-card{background:var(--card);border:1px solid var(--card-b);border-radius:16px;padding:15px 17px;transition:.2s;position:relative;overflow:hidden}
.conn-card:hover{border-color:var(--card-bh);transform:translateY(-1px)}
.conn-card::before{content:'';position:absolute;top:0;right:0;width:3px;height:100%;background:var(--green)}
.conn-ip-row{display:flex;align-items:center;gap:8px;margin-bottom:10px}
.conn-ip-icon{width:32px;height:32px;border-radius:9px;background:var(--green-bg);color:var(--green-t);display:flex;align-items:center;justify-content:center;font-size:15px;flex-shrink:0}
.conn-ip{font-family:ui-monospace,monospace;font-size:13px;font-weight:700;color:var(--t1)}
.conn-label{font-size:10.5px;color:var(--t3);margin-top:1px}
.conn-meta{display:flex;justify-content:space-between;align-items:center;font-size:10px;color:var(--t3);padding-top:10px;border-top:1px solid var(--card-b)}

/* ══════ لاگ فعالیت‌ها ══════ */
.log-timeline{display:flex;flex-direction:column}
.log-item{display:flex;gap:12px;padding:11px 0;border-bottom:1px solid rgba(37,99,235,.05);position:relative}
.log-item:last-child{border-bottom:none}
.log-ic{width:30px;height:30px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0}
.log-ic.ok{background:var(--green-bg);color:var(--green-t)}
.log-ic.err{background:var(--red-bg);color:var(--red-t)}
.log-ic.warn{background:var(--amber-bg);color:var(--amber-t)}
.log-ic.info{background:var(--accent-d);color:var(--accent2)}
.log-body{flex:1;min-width:0}
.log-msg{font-size:12.5px;color:var(--t1);line-height:1.6}
.log-time{font-size:9.5px;color:var(--t3);margin-top:2px;display:flex;align-items:center;gap:5px}
.log-kind{font-size:8.5px;padding:1px 7px;border-radius:10px;background:var(--accent-d);color:var(--accent2);font-weight:700;text-transform:uppercase;letter-spacing:.04em}
.erow{padding:9px 0;border-bottom:1px solid rgba(37,99,235,.05)}
.erow:last-child{border-bottom:none}
.etime{color:var(--t3);font-size:9.5px;margin-bottom:3px;display:flex;align-items:center;gap:4px}
.emsg{color:var(--red-t);font-family:ui-monospace,monospace;background:var(--red-bg);padding:6px 9px;border-radius:6px;word-break:break-all;font-size:10.5px}

@media(max-width:1050px){
  .sidebar{transform:translateX(100%)}
  .sidebar.open{transform:translateX(0);box-shadow:-10px 0 40px rgba(0,0,0,.4)}
  .sb-close{display:flex}
  .main{margin-right:0;padding-top:70px}
  .mob-top{display:flex}
  .metrics{grid-template-columns:1fr 1fr}
  .g2,.g3{grid-template-columns:1fr}
}
@media(max-width:500px){
  .metrics{grid-template-columns:1fr}
  .main{padding:62px 12px 50px}
  .sub-grid,.cfg-grid,.conn-grid{grid-template-columns:1fr}
}
/* ══════ نسخه و بروزرسانی — دیزاین جدید ══════ */
.upd-hero{background:linear-gradient(150deg,var(--bg3) 0%,var(--card) 65%);border:1px solid var(--card-b);border-radius:24px;padding:26px 26px 22px;position:relative;overflow:hidden;box-shadow:var(--shadow);margin-bottom:16px}
.upd-hero-glow{position:absolute;top:-70px;left:-70px;width:260px;height:260px;background:radial-gradient(circle,rgba(37,99,235,.1),transparent 70%);pointer-events:none}
.upd-hero-top{display:flex;align-items:flex-start;justify-content:space-between;gap:14px;position:relative;z-index:1;flex-wrap:wrap;margin-bottom:14px}
.upd-hero-cur{display:flex;align-items:center;gap:14px}
.upd-hero-icon{width:52px;height:52px;border-radius:16px;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;color:#fff;font-size:24px;flex-shrink:0;box-shadow:0 8px 22px rgba(37,99,235,.2)}
.upd-hero-label{font-size:10.5px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px}
.upd-hero-ver{font-size:26px;font-weight:800;color:var(--t1);letter-spacing:-.02em}
.upd-hero-desc{font-size:12.5px;color:var(--t2);line-height:1.8;position:relative;z-index:1;margin-bottom:14px;background:var(--bg);border:1px solid var(--card-b);border-radius:12px;padding:12px 14px}
[data-theme="dark"] .upd-hero-desc{background:var(--bg2)!important;color:var(--t1)!important}
.upd-hero-meta{display:flex;gap:8px;flex-wrap:wrap;position:relative;z-index:1}
.upd-meta-chip{display:flex;align-items:center;gap:6px;font-size:10.5px;font-weight:700;color:var(--t2);background:var(--accent-d);border:1px solid var(--card-b);padding:6px 12px;border-radius:20px}
.upd-meta-chip i{color:var(--accent);font-size:13px}
.upd-pill{display:inline-flex;align-items:center;gap:6px;font-size:11px;font-weight:800;padding:6px 14px;border-radius:20px}
.upd-pill-blue{background:var(--accent-d);color:var(--accent2)}
.upd-pill-green{background:var(--green-bg);color:var(--green-t)}
.upd-pill-amber{background:var(--amber-bg);color:var(--amber-t)}
.upd-dot{width:6px;height:6px;border-radius:50%;background:currentColor;animation:pulse 1.6s infinite}

.upd-latest-card{background:linear-gradient(120deg,var(--amber) 0%,#D97706 100%);border-radius:22px;padding:20px 24px;display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:16px;box-shadow:0 12px 32px rgba(245,158,11,.28);position:relative;overflow:hidden}
.upd-latest-card::before{content:'';position:absolute;top:-40px;left:-40px;width:180px;height:180px;background:radial-gradient(circle,rgba(255,255,255,.18),transparent 70%);pointer-events:none}
.upd-latest-left{display:flex;align-items:center;gap:14px;position:relative;z-index:1;min-width:220px}
.upd-latest-icon{width:48px;height:48px;border-radius:14px;background:rgba(255,255,255,.22);display:flex;align-items:center;justify-content:center;color:#fff;font-size:22px;flex-shrink:0}
.upd-latest-title{font-size:13px;font-weight:800;color:#fff;opacity:.92}
.upd-latest-ver{font-size:18px;font-weight:800;color:#fff;margin-top:2px}
.upd-latest-desc{font-size:11.5px;color:rgba(255,255,255,.88);margin-top:4px;line-height:1.7;max-width:440px}
.upd-install-btn{background:#fff;color:#B45309;border:none;border-radius:14px;padding:13px 24px;font-family:inherit;font-size:13.5px;font-weight:800;cursor:pointer;display:flex;align-items:center;gap:8px;box-shadow:0 6px 18px rgba(0,0,0,.18);transition:.18s;position:relative;z-index:1;white-space:nowrap}
.upd-install-btn:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(0,0,0,.24)}
.upd-install-btn:active{transform:translateY(0) scale(.98)}
.upd-install-btn:disabled{opacity:.6;cursor:not-allowed;transform:none}

.upd-progress-card{background:var(--card);border:1px solid var(--card-b);border-radius:18px;padding:18px 20px;margin-bottom:16px;box-shadow:var(--shadow)}
.upd-progress-head{display:flex;align-items:center;gap:12px;margin-bottom:12px}
.upd-progress-icon{width:38px;height:38px;border-radius:11px;background:var(--accent-d);color:var(--accent);display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0}
.upd-progress-title{font-size:13px;font-weight:800;color:var(--t1)}
.upd-progress-txt{font-size:10.5px;color:var(--t3);margin-top:2px}
.upd-progress-pct{font-size:16px;font-weight:800;color:var(--accent2);flex-shrink:0}
.upd-progress-track{height:8px;border-radius:6px;background:var(--accent-d);overflow:hidden}
.upd-progress-fill{height:100%;border-radius:6px;background:linear-gradient(90deg,var(--accent),var(--accent2));transition:width .4s ease;position:relative;overflow:hidden}
.upd-progress-fill::after{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(255,255,255,.4),transparent);width:40%;animation:shimmer 1.6s linear infinite}

.upd-log-card{background:var(--card);border:1px solid var(--card-b);border-radius:18px;padding:18px 20px;margin-bottom:20px;box-shadow:var(--shadow)}
.upd-log-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px}
.upd-log-title{font-size:12.5px;font-weight:800;color:var(--t1);display:flex;align-items:center;gap:7px}
.upd-log-title i{color:var(--accent);font-size:16px}
.upd-log-box{background:rgba(0,0,0,.3);border:1px solid var(--card-b);border-radius:12px;padding:14px 16px;max-height:240px;overflow-y:auto;font-family:ui-monospace,monospace;font-size:10.5px;line-height:2}
[data-theme="dark"] .upd-log-box{background:var(--bg)}
.upd-log-empty{color:var(--t3)}
.upd-log-line{color:var(--t2);white-space:pre-wrap;word-break:break-all}
.upd-log-line.err{color:var(--red-t)}
.upd-log-line.ok{color:var(--green-t)}

.upd-history-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px}
.upd-history-title{font-size:13px;font-weight:800;color:var(--t1);display:flex;align-items:center;gap:7px}
.upd-history-title i{color:var(--accent);font-size:17px}

.upd-timeline{position:relative;display:flex;flex-direction:column;gap:0}
.upd-timeline::before{content:'';position:absolute;top:8px;bottom:8px;right:19px;width:2px;background:linear-gradient(180deg,var(--card-b),transparent)}
.upd-item{display:flex;gap:16px;padding:0 0 20px;position:relative}
.upd-item:last-child{padding-bottom:0}
.upd-item-dot-wrap{position:relative;z-index:1;flex-shrink:0}
.upd-item-dot{width:40px;height:40px;border-radius:13px;background:var(--card);border:2px solid var(--green);display:flex;align-items:center;justify-content:center;color:var(--green-t);font-size:17px;box-shadow:var(--shadow)}
.upd-item.err .upd-item-dot{border-color:var(--red);color:var(--red-t)}
.upd-item-card{flex:1;background:var(--card);border:1px solid var(--card-b);border-radius:16px;padding:14px 17px;transition:.18s;min-width:0}
.upd-item-card:hover{border-color:var(--card-bh);transform:translateY(-1px)}
.upd-item-head{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-bottom:6px}
.upd-item-versions{font-size:13.5px;font-weight:800;color:var(--t1);display:flex;align-items:center;gap:8px}
.upd-item-versions .arrow{color:var(--t3);font-size:14px}
.upd-item-versions .to{color:var(--accent2)}
.upd-item-time{font-size:10px;color:var(--t3);display:flex;align-items:center;gap:5px;white-space:nowrap}
.upd-item-desc{font-size:11.5px;color:var(--t2);line-height:1.8;margin-top:6px}
.upd-item-badge{font-size:9px;font-weight:800;padding:3px 9px;border-radius:20px;flex-shrink:0}
.upd-item-badge.ok{background:var(--green-bg);color:var(--green-t)}
.upd-item-badge.err{background:var(--red-bg);color:var(--red-t)}
.upd-item-err-box{margin-top:8px;background:var(--red-bg);border:1px solid rgba(220,38,38,.15);border-radius:9px;padding:8px 11px;font-size:10.5px;color:var(--red-t);font-family:ui-monospace,monospace;word-break:break-all}
.upd-history-empty{text-align:center;padding:50px 20px;color:var(--t3);background:var(--card);border:1px dashed var(--card-b);border-radius:18px}
.upd-history-empty i{font-size:36px;opacity:.35;margin-bottom:10px;display:block}

/* ══════ بخش حذف‌شده ══════ */
.sup-wrap{max-width:1450px;background:var(--card);border:1px solid var(--card-b);border-radius:24px;overflow:hidden;box-shadow:var(--shadow);position:relative}
.sup-wrap::before{content:'';position:absolute;top:-60px;left:-60px;width:200px;height:200px;background:radial-gradient(circle,var(--accent-d),transparent 70%);pointer-events:none;z-index:0}
.sup-head{display:flex;align-items:center;gap:13px;padding:18px 22px;border-bottom:1px solid var(--card-b);background:linear-gradient(155deg,var(--accent-d) 0%,transparent 75%);position:relative;z-index:1}
.sup-head-icon{width:42px;height:42px;border-radius:13px;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;color:#fff;font-size:19px;flex-shrink:0;box-shadow:0 6px 16px rgba(37,99,235,.2);position:relative}
.sup-head-icon::after{content:'';position:absolute;inset:-5px;border-radius:16px;border:1.5px solid var(--accent);opacity:.4;animation:supBreathe 2.4s ease-in-out infinite}
@keyframes supBreathe{0%,100%{transform:scale(1);opacity:.4}50%{transform:scale(1.1);opacity:0}}
.sup-head-text{flex:1;min-width:0}
.sup-head-title{font-size:14.5px;font-weight:800;color:var(--t1);letter-spacing:-.01em}
.sup-head-sub{font-size:10.5px;color:var(--t3);margin-top:3px;display:flex;align-items:center;gap:6px}
.sup-head-sub .sdot{width:6px;height:6px;border-radius:50%;background:var(--green);animation:pulse 1.6s infinite;flex-shrink:0}
.sup-close-btn{background:var(--red-bg);color:var(--red-t);border:1px solid rgba(220,38,38,.15);border-radius:10px;padding:8px 14px;font-family:inherit;font-size:11px;font-weight:700;cursor:pointer;display:flex;align-items:center;gap:6px;transition:.15s}
.sup-close-btn:hover{background:rgba(220,38,38,.15);transform:translateY(-1px)}
.sup-blocked-banner{background:var(--red-bg);color:var(--red-t);font-size:11.5px;font-weight:700;padding:11px 22px;display:flex;align-items:center;gap:8px;border-bottom:1px solid var(--card-b);position:relative;z-index:1}
 
#support-msgs{height:370px;overflow-y:auto;display:flex;flex-direction:column;gap:2px;padding:20px;background:var(--bg2);position:relative;z-index:1;scroll-behavior:smooth}
#support-msgs::-webkit-scrollbar{width:5px}
#support-msgs::-webkit-scrollbar-thumb{background:var(--card-b);border-radius:3px}
 
.sup-date-sep{text-align:center;font-size:9.5px;color:var(--t3);font-weight:700;margin:14px 0 10px;position:relative}
.sup-date-sep span{background:var(--bg2);padding:0 12px;position:relative;z-index:1}
.sup-date-sep::before{content:'';position:absolute;top:50%;right:0;left:0;height:1px;background:var(--card-b);z-index:0}
 
.sup-msg-row{display:flex;align-items:flex-end;gap:8px;margin-bottom:10px;max-width:100%}
.sup-msg-row.client{margin-right:0;margin-left:auto;flex-direction:row-reverse}
.sup-msg-row.admin{margin-left:0; display: flex; justify-content: left}
.sup-avatar{width:26px;height:26px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:12px;flex-shrink:0;margin-bottom:2px}
.sup-avatar.admin{background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff}
.sup-avatar.client{background:var(--purple-bg);color:var(--purple)}
.sup-msg{padding:10px 15px;border-radius:16px;font-size:12.8px;line-height:1.75;word-break:break-word;position:relative;box-shadow:0 1px 2px rgba(0,0,0,.06)}
.sup-msg.client{background:var(--accent);color:#fff;border-bottom-right-radius:5px}
.sup-msg.admin{background:var(--card);color:var(--t1);border:1px solid var(--card-b);border-bottom-left-radius:5px}
.sup-msg .sup-time{display:flex;align-items:center;gap:4px;font-size:9px;opacity:.68;margin-top:5px;justify-content:flex-end}
.sup-msg .sup-time i{font-size:12px}
.sup-msg.client .sup-time i.seen{color:#fff}
 
.sup-empty{color:var(--t3);font-size:12px;text-align:center;padding:60px 20px;display:flex;flex-direction:column;align-items:center;gap:12px}
.sup-empty i{font-size:38px;opacity:.35}
.sup-empty b{color:var(--t2);font-size:13px;font-weight:700}
 
.sup-input-row{display:flex;gap:10px;padding:16px 18px;background:var(--card);border-top:1px solid var(--card-b);position:relative;z-index:1}
.sup-input-row input{margin-bottom:0;border-radius:13px;padding:12px 16px}
.sup-input-row button{border-radius:13px;padding:0 18px;display:flex;align-items:center;justify-content:center}
.sup-input-row.disabled{opacity:.55;pointer-events:none}
 
.sup-new-badge{display:inline-flex;align-items:center;gap:4px;background:var(--red);color:#fff;font-size:9px;font-weight:800;padding:2px 8px;border-radius:20px;margin-right:6px;animation:pulse 1.6s infinite}

/* ══════ مودال ساخت کانفیگ - نسخه حرفه‌ای ══════ */
.cm-modal{max-width:620px;width:calc(100% - 32px);padding:0;border-radius:24px;overflow:hidden;
  max-height:92vh;display:flex;flex-direction:column}
.cm-head{background:linear-gradient(155deg,rgba(37,99,235,.1) 0%,transparent 70%);
  padding:26px 28px 20px;position:relative;border-bottom:1px solid var(--card-b);flex-shrink:0}
.cm-head::before{content:'';position:absolute;top:-60px;left:-60px;width:200px;height:200px;
  background:radial-gradient(circle,rgba(37,99,235,.18),transparent 70%);pointer-events:none}
.cm-head-row{display:flex;align-items:center;gap:14px;position:relative;z-index:1}
.cm-head-icon{width:46px;height:46px;border-radius:14px;background:linear-gradient(135deg,var(--accent),var(--accent2));
  display:flex;align-items:center;justify-content:center;color:#fff;font-size:21px;flex-shrink:0;
  box-shadow:0 8px 20px rgba(37,99,235,.2)}
.cm-head-title{font-size:16.5px;font-weight:800;color:var(--t1);letter-spacing:-.01em}
.cm-head-sub{font-size:11px;color:var(--t3);margin-top:3px}
.cm-close{position:absolute;top:18px;left:18px;background:rgba(0,0,0,.18);border:1px solid var(--card-b);
  color:var(--t2);width:32px;height:32px;border-radius:10px;font-size:15px;display:flex;align-items:center;
  justify-content:center;cursor:pointer;z-index:2;transition:.15s}
.cm-close:hover{background:var(--red-bg);color:var(--red-t);border-color:rgba(239,68,68,.25)}

.cm-body{padding:22px 28px 8px;overflow-y:auto;overflow-x:hidden;flex:1;max-height:min(68vh,720px);scrollbar-width:thin}
.cm-section{margin-bottom:20px}
.cm-section-label{font-size:10.5px;font-weight:800;color:var(--t3);text-transform:uppercase;
  letter-spacing:.08em;display:flex;align-items:center;gap:6px;margin-bottom:10px}
.cm-section-label i{color:var(--accent);font-size:14px}

.cm-field{margin-bottom:14px}
.cm-field label{display:block;font-size:11px;font-weight:700;color:var(--t2);margin-bottom:7px}
.cm-input{width:100%;padding:11px 14px;border-radius:11px;border:1px solid var(--card-b);
  background:rgba(0,0,0,.18);color:var(--t1);font-family:inherit;font-size:12.8px;outline:none;transition:.15s}
[data-theme="dark"] .cm-input{background:var(--bg2)!important;color:var(--t1)!important}
.cm-input:focus{border-color:rgba(37,99,235,.5);box-shadow:0 0 0 3px rgba(37,99,235,.1)}
.cm-input::placeholder{color:var(--t3)}
.cm-row2{display:grid;grid-template-columns:1fr 1fr;gap:12px}

/* ── آکاردئون کشویی انتخاب پروتکل / ترابرد ── */
.cm-dd{border:1px solid var(--card-b);border-radius:14px;overflow:hidden;background:rgba(0,0,0,.1);transition:.18s}
[data-theme="dark"] .cm-dd{background:var(--bg2)!important;color:var(--t1)!important}
.cm-dd.open{border-color:var(--card-bh);box-shadow:0 0 0 3px rgba(37,99,235,.08)}
.cm-dd-trigger{display:flex;align-items:center;gap:12px;padding:13px 15px;cursor:pointer;user-select:none}
.cm-dd-icon{width:38px;height:38px;border-radius:11px;background:var(--accent-d);color:var(--accent);
  display:flex;align-items:center;justify-content:center;font-size:17px;flex-shrink:0;transition:.18s}
.cm-dd-text{flex:1;min-width:0}
.cm-dd-title{font-size:13px;font-weight:800;color:var(--t1)}
.cm-dd-desc{font-size:10px;color:var(--t3);margin-top:2px}
.cm-dd-chev{color:var(--t3);font-size:16px;transition:transform .2s;flex-shrink:0}
.cm-dd.open .cm-dd-chev{transform:rotate(180deg);color:var(--accent)}

.cm-dd-panel{display:grid;grid-template-rows:0fr;transition:grid-template-rows .22s ease}
.cm-dd.open .cm-dd-panel{grid-template-rows:1fr}
.cm-dd-panel-inner{overflow:hidden}
.cm-dd-list{border-top:1px solid var(--card-b);padding:6px}
.cm-opt{display:flex;align-items:flex-start;gap:12px;padding:14px 16px;border-radius:14px;cursor:pointer;transition:background 200ms ease,border-color 200ms ease,transform 200ms ease,box-shadow 200ms ease;margin-bottom:12px;border:1px solid #DBEAFE;background:#EFF6FF}
.cm-opt:hover{border-color:#93C5FD;transform:translateY(-2px);box-shadow:0 8px 20px rgba(37,99,235,.08)}
.cm-opt.sel{background:#DBEAFE;border-color:#2563EB;box-shadow:0 0 0 1px #2563EB}
[data-theme="dark"] .cm-opt{background:rgba(248,250,252,.06);border-color:rgba(248,250,252,.12)}
[data-theme="dark"] .cm-opt:hover{background:rgba(248,250,252,.09);border-color:rgba(248,250,252,.18);box-shadow:0 8px 20px rgba(0,0,0,.2)}
[data-theme="dark"] .cm-opt.sel{background:rgba(248,250,252,.12);border-color:#93C5FD;box-shadow:0 0 0 1px rgba(147,197,253,.35)}
.cm-opt-radio{width:18px;height:18px;border-radius:50%;border:2px solid #93C5FD;flex-shrink:0;display:flex;align-items:center;justify-content:center;transition:border-color 200ms ease;margin-top:2px;background:transparent}
.cm-opt.sel .cm-opt-radio{border-color:#2563EB}
[data-theme="dark"] .cm-opt-radio{border-color:rgba(248,250,252,.35)}
[data-theme="dark"] .cm-opt.sel .cm-opt-radio{border-color:#93C5FD}
.cm-opt-radio::after{content:'';width:8px;height:8px;border-radius:50%;background:#2563EB;transform:scale(0);transition:transform 200ms ease}
.cm-opt.sel .cm-opt-radio::after{transform:scale(1)}
[data-theme="dark"] .cm-opt-radio::after{background:#93C5FD}
.cm-opt-icon{display:none !important}
.cm-opt-text{flex:1;min-width:0}
.cm-opt-title{font-size:15px;font-weight:600;color:var(--t1);letter-spacing:-.01em}
.cm-opt-desc{font-size:11.5px;color:var(--t2);margin-top:4px;line-height:1.7;font-weight:400}
.cm-opt-tag{font-size:10.5px;font-weight:600;padding:3px 8px;border-radius:999px;background:rgba(37,99,235,.1);color:#1D4ED8;flex-shrink:0}
[data-theme="dark"] .cm-opt-tag{background:rgba(248,250,252,.1);color:#E2E8F0}
.cm-opt-tag.rec,.cm-opt.sel .cm-opt-tag{background:#2563EB;color:#fff}
[data-theme="dark"] .cm-opt-tag.rec,[data-theme="dark"] .cm-opt.sel .cm-opt-tag{background:#93C5FD;color:#0F172A}

.cm-pills{display:flex;gap:6px;flex-wrap:wrap;margin-top:9px}
.cm-pill{padding:6px 13px;border-radius:20px;font-size:10.5px;font-weight:700;color:var(--t2);
  background:transparent;border:1px solid var(--card-b);cursor:pointer;transition:.15s;font-family:inherit}
.cm-pill:hover{background:var(--accent-d)}
.cm-pill.active{background:var(--accent);color:#fff;border-color:var(--accent);box-shadow:0 3px 10px rgba(37,99,235,.18)}

.cm-note{font-size:10.5px;color:var(--t3);display:flex;align-items:flex-start;gap:7px;
  background:var(--accent-d);border-radius:10px;padding:10px 13px;line-height:1.7;margin-top:4px}
.cm-note i{color:var(--accent);font-size:14px;flex-shrink:0;margin-top:1px}

.cm-footer{display:flex;gap:10px;padding:16px 28px;border-top:1px solid var(--card-b);flex-shrink:0;
  background:var(--card)}
.cm-btn-cancel{flex:.55;justify-content:center;padding:12px;border-radius:12px;background:transparent;
  border:1px solid var(--card-b);color:var(--t2);font-family:inherit;font-size:12.5px;font-weight:700;
  cursor:pointer;transition:.15s;display:flex;align-items:center}
.cm-btn-cancel:hover{background:var(--accent-d);color:var(--t1)}
.cm-btn-submit{flex:1;justify-content:center;padding:12px;border-radius:12px;
  background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;border:none;
  font-family:inherit;font-size:13px;font-weight:800;cursor:pointer;display:flex;align-items:center;
  gap:7px;box-shadow:0 6px 18px rgba(37,99,235,.22);transition:.18s}
.cm-btn-submit:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(37,99,235,.5)}
.cm-btn-submit:active{transform:translateY(0) scale(.98)}

/* دسکتاپ بزرگ‌تر */
@media(min-width:900px){
  .cm-modal{max-width:680px}
  .cm-body{padding:24px 34px 8px}
  .cm-head{padding:28px 34px 22px}
  .cm-footer{padding:18px 34px}
}

/* موبایل = باتم‌شیت */
@media(max-width:640px){
  #modal-create-link.modal-bg{align-items:flex-end}
  .cm-modal{max-width:100%;width:100%;border-radius:22px 22px 0 0;max-height:90vh;
    animation:cmSlideUp .28s cubic-bezier(.32,.72,0,1)}
  .cm-row2{grid-template-columns:1fr}
  .cm-head{padding:20px 18px 16px}
  .cm-body{padding:18px 18px 6px}
  .cm-footer{padding:14px 18px 18px}
}
@keyframes cmSlideUp{from{transform:translateY(100%)}to{transform:translateY(0)}}

</style>

<style id="oxnet-dashboard-redesign">
/* OXNET professional blue theme overrides */
body, button, input, select, textarea { font-family: var(--font, "Vazirmatn", system-ui, sans-serif) !important; }
body{
  background: var(--bg) !important;
  letter-spacing:-.01em;
}
.sidebar{
  background: var(--bg2) !important;
  backdrop-filter: blur(12px);
  border-left: 1px solid var(--card-b) !important;
  box-shadow: -6px 0 24px rgba(15,23,42,.04);
}
[data-theme="dark"] .sidebar{ background: var(--bg2) !important; }
.brand-mark,.logo .brand-mark{
  background: var(--accent) !important;
  color: #fff !important;
  border: none !important;
  box-shadow: 0 8px 20px rgba(37,99,235,.28) !important;
}
.nav-it{
  margin:2px 10px !important;
  border-radius:12px !important;
  border-right:none !important;
  padding:10px 12px !important;
  color:var(--t2) !important;
  font-weight:500 !important;
}
.nav-it:hover{ background:var(--accent-d) !important; color:var(--t1) !important; }
.nav-it.on{
  background:var(--accent) !important;
  color:#fff !important;
  font-weight:600 !important;
  box-shadow:0 6px 16px rgba(37,99,235,.28);
}
.nav-it.on i{ color:#fff !important; }
.nav-badge{
  background:rgba(15,23,42,.06) !important;
  color:var(--t2) !important;
  border-radius:999px !important;
}
.nav-it.on .nav-badge{ background:rgba(255,255,255,.2) !important; color:#fff !important; }
.main{ background:transparent !important; }
.topbar{ background:transparent !important; border-bottom:none !important; }
.tb-title{ font-weight:800 !important; color:var(--t1) !important; }
.tb-sub{ color:var(--t2) !important; }
.card,.stat-card,.srv-panel,.pw-panel,.cfg-card,.row-item,.sub-info,.copy-all-bar{
  background:var(--card) !important;
  border:1px solid var(--card-b) !important;
  box-shadow:var(--shadow) !important;
}
.btn-p,.btn.btn-p{
  background:var(--accent) !important;
  color:#fff !important;
  box-shadow:0 4px 14px rgba(37,99,235,.3) !important;
}
.btn-p:hover{ background:var(--accent2) !important; transform:translateY(-1px); }
.btn-g,.btn-o{
  background:var(--accent-d) !important;
  color:var(--accent) !important;
  border:1px solid transparent !important;
}
.btn-g:hover,.btn-o:hover{ background:rgba(37,99,235,.16) !important; color:var(--accent2) !important; }
.btn-d{ background:var(--red-bg) !important; color:var(--red-t) !important; }
.btn-pur{ background:var(--purple-bg) !important; color:var(--purple-t) !important; }
.btn-amber{ background:var(--amber-bg) !important; color:var(--amber-t) !important; }
.fi,.pw-input,.cm-input,.modal-v2-input{
  background:var(--card) !important;
  border:1px solid var(--card-b) !important;
  color:var(--t1) !important;
}
.fi:focus,.pw-input:focus,.cm-input:focus,.modal-v2-input:focus{
  border-color:var(--accent) !important;
  box-shadow:0 0 0 3px var(--accent-d) !important;
}
.vl-code{
  background:var(--bg) !important;
  border:1px solid var(--card-b) !important;
  color:var(--t1) !important;
}

/* ===== Dashboard visual layout (was missing) ===== */
.dash-hero{
  display:grid;
  grid-template-columns:1.6fr 1fr;
  gap:16px;
  margin-bottom:18px;
}
@media(max-width:980px){.dash-hero{grid-template-columns:1fr}}
.dash-main-card{
  background:var(--card);
  border:1px solid var(--card-b);
  border-radius:20px;
  padding:28px 28px 24px;
  box-shadow:var(--shadow);
  position:relative;
  overflow:hidden;
}
.dash-main-card::before{
  content:"";
  position:absolute;inset:0 auto 0 0;width:4px;
  background:linear-gradient(180deg,var(--accent),var(--info));
  border-radius:20px 0 0 20px;
}
.dash-eyebrow{
  font-size:11px;font-weight:700;color:var(--accent);
  letter-spacing:.06em;text-transform:uppercase;margin-bottom:8px;
}
.dash-title{
  font-size:24px;font-weight:800;color:var(--t1);
  letter-spacing:-.03em;line-height:1.35;margin-bottom:10px;
}
.dash-title span{color:var(--accent)}
.dash-desc{
  font-size:13.5px;color:var(--t2);line-height:1.8;max-width:520px;margin-bottom:18px;
}
.dash-actions{display:flex;flex-wrap:wrap;gap:10px}
.dash-side{
  display:grid;grid-template-columns:1fr 1fr;gap:12px;
}
.dash-kpi{
  background:var(--card);
  border:1px solid var(--card-b);
  border-radius:16px;
  padding:16px 14px;
  box-shadow:var(--shadow);
  transition:transform .15s, border-color .15s, box-shadow .15s;
}
.dash-kpi:hover{
  transform:translateY(-2px);
  border-color:var(--card-bh);
  box-shadow:0 12px 28px rgba(15,23,42,.08);
}
.dash-kpi-icon{
  width:36px;height:36px;border-radius:10px;
  background:var(--accent-d);color:var(--accent);
  display:flex;align-items:center;justify-content:center;
  font-size:17px;margin-bottom:10px;
}
.dash-kpi-label{font-size:11px;font-weight:600;color:var(--t3);margin-bottom:4px}
.dash-kpi-val{font-size:22px;font-weight:800;color:var(--t1);letter-spacing:-.02em;line-height:1.2}
.dash-kpi-sub{font-size:10.5px;color:var(--t2);margin-top:2px;font-weight:500}
.dash-protocols{
  display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:18px;
}
@media(max-width:900px){.dash-protocols{grid-template-columns:1fr 1fr}}
@media(max-width:520px){.dash-protocols{grid-template-columns:1fr}}
.dash-protocol{
  background:var(--card);
  border:1px solid var(--card-b);
  border-radius:14px;
  padding:14px 16px;
  display:flex;align-items:center;gap:12px;
  box-shadow:var(--shadow);
  transition:border-color .15s, transform .15s;
}
.dash-protocol:hover{border-color:var(--accent);transform:translateY(-1px)}
.dash-protocol i{
  width:40px;height:40px;border-radius:12px;
  background:var(--accent-d);color:var(--accent);
  display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;
}
.dash-protocol b{display:block;font-size:13px;font-weight:700;color:var(--t1)}
.dash-protocol span{display:block;font-size:11px;color:var(--t3);margin-top:2px}



.fallback-bars{display:flex;align-items:flex-end;gap:6px;height:200px;padding:8px 4px}
.fallback-bars span{flex:1;background:rgba(37,99,235,.35);border-radius:6px 6px 2px 2px;min-height:4px;transition:height 200ms ease}
.fallback-protos{display:flex;flex-direction:column;gap:10px;padding:8px 0}
.fallback-protos .fp-row{display:flex;align-items:center;gap:10px;font-size:12px;color:var(--t2)}
.fallback-protos .fp-bar{flex:1;height:8px;background:var(--bg3);border-radius:999px;overflow:hidden}
.fallback-protos .fp-bar i{display:block;height:100%;background:var(--accent);border-radius:999px}
/* ===== Dashboard charts + section cards (were missing layout CSS) ===== */
.dash-chart-grid{
  display:grid;
  grid-template-columns:1.6fr 1fr;
  gap:16px;
  margin:16px 0 16px;
}
@media(max-width:960px){.dash-chart-grid{grid-template-columns:1fr}}
.dash-chart-card{
  background:var(--card);
  border:1px solid var(--card-b);
  border-radius:14px;
  padding:16px 16px 12px;
  box-shadow:0 8px 20px rgba(15,23,42,.05);
  min-height:0;
}
.dash-card-head{
  display:flex;
  align-items:flex-start;
  justify-content:space-between;
  gap:12px;
  margin-bottom:12px;
}
.dash-card-title{
  font-size:14px;
  font-weight:700;
  color:var(--t1);
  display:flex;
  align-items:center;
  gap:8px;
  letter-spacing:-.02em;
}
.dash-card-title i{color:var(--accent);font-size:16px}
.dash-card-sub{
  font-size:12px;
  color:var(--t3);
  margin-top:4px;
  font-weight:400;
}
.dash-chart-card .ch{
  position:relative;
  height:240px;
  width:100%;
}
.dash-chart-card .ch-sm{
  position:relative;
  height:220px;
  width:100%;
  max-width:280px;
  margin:0 auto;
}
.dash-chart-card canvas{
  width:100% !important;
  height:100% !important;
}
/* health / summary cards polish */
#pg-overview .g2{gap:16px;margin-bottom:8px}
#pg-overview .card{
  background:var(--card);
  border:1px solid var(--card-b);
  border-radius:14px;
  padding:16px 18px;
  box-shadow:0 8px 20px rgba(15,23,42,.05);
}
#pg-overview .card-title{
  font-size:14px;font-weight:700;color:var(--t1);
  margin-bottom:12px;display:flex;align-items:center;gap:8px;
}
#pg-overview .card-title i{color:var(--accent)}
#pg-overview .sr{
  display:flex;align-items:center;justify-content:space-between;
  padding:10px 0;border-bottom:1px solid var(--card-b);font-size:13px;
}
#pg-overview .sr:last-child{border-bottom:none}
#pg-overview .sr-k{color:var(--t2);display:flex;align-items:center;gap:8px;font-weight:500}
#pg-overview .sr-k i{color:var(--t3);font-size:15px}
#pg-overview .sr-v{color:var(--t1);font-weight:600;font-size:12.5px}
.spbar{
  height:6px;border-radius:999px;background:var(--bg3);
  overflow:hidden;margin-top:6px;
}
.spfill{
  height:100%;border-radius:999px;background:var(--accent);
  transition:width 200ms ease;
}
#lsummary .row-item,
#lsummary .ls-row{
  display:flex;align-items:center;justify-content:space-between;gap:10px;
  padding:10px 0;border-bottom:1px solid var(--card-b);font-size:13px;
}
#lsummary .ls-row:last-child{border-bottom:none}
/* vless box polish */
.vless-box{
  background:var(--card);
  border:1px solid var(--card-b);
  border-radius:14px;
  padding:16px 18px;
  margin:16px 0;
  box-shadow:0 8px 20px rgba(15,23,42,.05);
}
.vl-header{
  display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:12px;flex-wrap:wrap;
}
.vl-title{
  font-size:14px;font-weight:700;color:var(--t1);display:flex;align-items:center;gap:8px;
}
.vl-title i{color:var(--accent)}
/* ===== Multi-protocol group cards (was missing CSS) ===== */
.links-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px}
.multi-group-card{
  background:var(--card);
  border:1px solid var(--card-b);
  border-radius:14px;
  padding:0;
  overflow:hidden;
  box-shadow:0 8px 20px rgba(15,23,42,.05);
  transition:border-color 200ms ease, box-shadow 200ms ease, transform 200ms ease;
}
.multi-group-card:hover{
  border-color:var(--card-bh);
  box-shadow:0 10px 24px rgba(15,23,42,.07);
  transform:translateY(-2px);
}
.multi-group-head{
  display:flex;align-items:flex-start;justify-content:space-between;gap:12px;
  padding:16px 16px 12px;flex-wrap:wrap;
}
.multi-group-title{
  font-size:15px;font-weight:700;color:var(--t1);display:flex;align-items:center;gap:8px;letter-spacing:-.02em;
}
.multi-group-title i{color:var(--accent);font-size:18px}
.multi-protos{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.multi-protos span{
  font-size:11px;font-weight:500;color:var(--t2);
  background:var(--bg);border:1px solid var(--card-b);
  border-radius:10px;padding:4px 8px;
}
.multi-group-card .utxt{
  display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;
  padding:12px 16px 16px;border-top:1px solid var(--card-b);
  font-size:11.5px;color:var(--t3);font-weight:500;
}
.multi-group-card .utxt span:last-child{
  font-family:ui-monospace,monospace;color:var(--accent);word-break:break-all;font-size:11px;
}
.badge.bg-blue{background:var(--accent-d);color:var(--accent)}

/* ===== Design system refinements ===== */
:root{
  --r-sm:10px; --r-md:14px; --r-lg:18px;
  --shadow:0 8px 20px rgba(15,23,42,.05) !important;
  --t:200ms ease;
}
body{
  background:linear-gradient(180deg,#F8FAFC,#EEF2F7) !important;
  transition:background var(--t),color var(--t);
}
[data-theme="dark"] body{
  background:linear-gradient(180deg,#0B1220,#111827) !important;
}
.card,.stat-card,.cfg-card,.sub-card,.srv-panel,.pw-panel,.row-item,.dash-main-card,.dash-kpi,.dash-protocol,.multi-group-card{
  border-radius:var(--r-md) !important;
  box-shadow:0 8px 20px rgba(15,23,42,.05) !important;
}
.btn,.btn-p,.btn-g,.btn-o,.btn-d,.btn-sm{
  border-radius:12px !important;
  transition:background var(--t),color var(--t),border-color var(--t),transform var(--t),box-shadow var(--t),opacity var(--t) !important;
  font-weight:600 !important;
}
.btn-p{background:var(--accent) !important;color:#fff !important;box-shadow:0 4px 12px rgba(37,99,235,.25) !important}
.btn-p:hover{background:var(--accent2) !important}
.btn-g,.btn-o{background:transparent !important;border:1px solid var(--card-b) !important;color:var(--t2) !important}
.btn-g:hover,.btn-o:hover{background:var(--accent-d) !important;color:var(--accent) !important;border-color:transparent !important}
.nav-it{
  transition:background var(--t),color var(--t),border-color var(--t) !important;
  border-right:3px solid transparent !important;
}
.nav-it.on{
  background:#EFF6FF !important;
  color:var(--accent) !important;
  border-right:3px solid var(--accent) !important;
  box-shadow:none !important;
}
.nav-it.on i{color:var(--accent) !important}
[data-theme="dark"] .nav-it.on{
  background:#172554 !important;
  color:#93C5FD !important;
  border-right-color:#3B82F6 !important;
}
[data-theme="dark"] .nav-it.on i{color:#93C5FD !important}
.nav-it.on .nav-badge{background:rgba(37,99,235,.12) !important;color:var(--accent) !important}
/* icon boxes only on dashboard KPIs */
.dash-kpi-icon,.dash-protocol i{background:var(--accent-d) !important;color:var(--accent) !important}
.card-title i,.tb-title i{background:transparent !important;color:var(--accent) !important}
.sub-card-top{background:var(--card) !important}
.sub-card-top::before{display:none !important}
.sub-card-icon{
  background:var(--accent-d) !important;color:var(--accent) !important;
  box-shadow:none !important;
}
.sub-card-icon i{color:var(--accent) !important}
.sub-card-url-row{
  background:var(--bg) !important;
  border:1px solid var(--card-b) !important;
  border-radius:var(--r-sm) !important;
}
.sub-card-url-text{color:var(--t2) !important}
.dash-main-card::before{background:var(--accent) !important}


/* ===== Protocol picker (create modal) — muted tags, soft selection ===== */
.cm-opt-tag{
  background:#F1F5F9 !important;
  color:#475569 !important;
  border:none !important;
  font-size:10.5px !important;
  font-weight:600 !important;
  padding:3px 8px !important;
  border-radius:999px !important;
  letter-spacing:0 !important;
}
[data-theme="dark"] .cm-opt-tag{
  background:#1E293B !important;
  color:#CBD5E1 !important;
}
.cm-opt-tag.rec,
.cm-opt-tag.recommended,
.cm-opt-tag.is-rec{
  background:#DBEAFE !important;
  color:#1D4ED8 !important;
}
[data-theme="dark"] .cm-opt-tag.rec,
[data-theme="dark"] .cm-opt-tag.recommended,
[data-theme="dark"] .cm-opt-tag.is-rec{
  background:rgba(37,99,235,.18) !important;
  color:#93C5FD !important;
}
/* kill green tags on protocol options */
.cm-opt .badge.bg-green,
.cm-opt-tag.bg-green,
.cm-opt .cm-opt-tag[style*="green"]{
  background:#F1F5F9 !important;
  color:#475569 !important;
}
.cm-opt{
  display:flex;align-items:flex-start;gap:12px;
  padding:14px 14px !important;
  margin-bottom:12px !important;
  border:1px solid var(--card-b) !important;
  border-radius:14px !important;
  background:var(--card) !important;
  transition:background 200ms ease,border-color 200ms ease,box-shadow 200ms ease,transform 200ms ease !important;
  cursor:pointer;
}
.cm-opt:hover{
  border-color:var(--card-bh) !important;
  transform:translateY(-2px);
  box-shadow:0 8px 20px rgba(15,23,42,.05);
}
.cm-opt.on,
.cm-opt.selected,
.cm-opt.active,
.cm-opt[aria-selected="true"]{
  border-color:#2563EB !important;
  background:#DBEAFE !important;
  box-shadow:0 0 0 1px #2563EB !important;
}
[data-theme="dark"] .cm-opt.on,
[data-theme="dark"] .cm-opt.selected,
[data-theme="dark"] .cm-opt.active{
  border-color:#93C5FD !important;
  background:rgba(248,250,252,.12) !important;
  box-shadow:0 0 0 1px rgba(147,197,253,.35) !important;
}
[data-theme="dark"] .cm-opt{
  background:rgba(248,250,252,.06) !important;
  border-color:rgba(248,250,252,.12) !important;
}
.cm-opt-icon,
.cm-opt .ico,
.cm-opt > i,
.proto-card-icon,
.cm-opt-dot{
  width:18px !important;height:18px !important;min-width:18px !important;
  border-radius:50% !important;
  background:#E2E8F0 !important;
  color:transparent !important;
  border:2px solid #CBD5E1 !important;
  box-shadow:none !important;
  display:inline-flex !important;
  align-items:center;justify-content:center;
  font-size:0 !important;
  margin-top:3px;
}
.cm-opt.on .cm-opt-icon,
.cm-opt.selected .cm-opt-icon,
.cm-opt.on > i,
.cm-opt.selected > i,
.cm-opt.on .ico,
.cm-opt.selected .ico{
  background:#2563EB !important;
  border-color:#2563EB !important;
}
[data-theme="dark"] .cm-opt-icon,
[data-theme="dark"] .cm-opt > i{
  background:#334155 !important;
  border-color:#475569 !important;
}
[data-theme="dark"] .cm-opt.on .cm-opt-icon,
[data-theme="dark"] .cm-opt.selected .cm-opt-icon,
[data-theme="dark"] .cm-opt.on > i{
  background:#3B82F6 !important;
  border-color:#3B82F6 !important;
}
.cm-opt-title,
.cm-opt-name{
  font-size:15px !important;
  font-weight:600 !important;
  color:var(--t1) !important;
  letter-spacing:-.01em;
}
.cm-opt-desc,
.cm-opt-sub{
  font-size:11.5px !important;
  line-height:1.7 !important;
  color:var(--t2) !important;
  margin-top:4px !important;
  font-weight:400 !important;
}
.cm-opt-rec-line{
  display:block;
  font-size:11px !important;
  font-weight:600 !important;
  color:#1D4ED8 !important;
  margin-top:4px !important;
}
[data-theme="dark"] .cm-opt-rec-line{color:#93C5FD !important}

/* Sidebar version footer */
.sb-foot .sb-version,
.sidebar-version{
  font-size:11px;color:var(--t3);padding:8px 12px 4px;text-align:center;font-weight:500;
}


.stat-v2-foot{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-top:10px}
.stat-v2-foot .spark{width:120px;height:28px;flex-shrink:0;opacity:.9}
.dash-chart-card .ch{height:280px !important}
.dash-chart-card .ch-sm{height:240px !important;position:relative}
.donut-center{
  position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
  pointer-events:none;text-align:center;padding-bottom:28px;
}
.donut-center .dc-num{font-size:22px;font-weight:700;color:var(--t1);letter-spacing:-.03em;line-height:1.1}
.donut-center .dc-sub{font-size:11px;color:var(--t3);font-weight:500;margin-top:4px}
/* ===== OXNET Modern Enterprise SaaS system ===== */
html{font-size:15px}
body{
  background:var(--bg) !important;
  color:var(--t1);
  font-weight:400;
  line-height:1.7;
  letter-spacing:-.011em;
}
.main{
  padding:24px 28px 48px !important;
  max-width:1280px;
}
@media(max-width:900px){.main{padding:16px 14px 40px !important}}
.sidebar{
  background:var(--bg2) !important;
  border-left:1px solid var(--card-b) !important;
  box-shadow:none !important;
}
.logo{padding:20px 16px !important;border-bottom:1px solid var(--card-b)}
.logo-text,.brand-name{font-weight:700 !important;font-size:17px !important;letter-spacing:-.02em}
.nav-sec{
  font-size:11px !important;font-weight:600 !important;letter-spacing:.06em !important;
  text-transform:uppercase;color:var(--t3) !important;margin:16px 14px 6px !important;
}
.nav-it{
  margin:2px 10px !important;border-radius:var(--r-sm) !important;
  padding:10px 12px !important;color:var(--t2) !important;font-weight:500 !important;
  border-right:3px solid transparent !important;transition:background var(--t),color var(--t),border-color var(--t) !important;
}
.nav-it:hover{background:#F3F4F6 !important;color:var(--t1) !important}
[data-theme="dark"] .nav-it:hover{background:#1E293B !important}
.nav-it.on{
  background:#EFF6FF !important;color:var(--accent) !important;
  border-right:3px solid var(--accent) !important;box-shadow:none !important;font-weight:600 !important;
}
.nav-it.on i{color:var(--accent) !important}
[data-theme="dark"] .nav-it.on{background:#1E3A8A33 !important;color:#93C5FD !important;border-right-color:#3B82F6 !important}
[data-theme="dark"] .nav-it.on i{color:#93C5FD !important}
.nav-it.on .nav-badge{background:rgba(37,99,235,.12) !important;color:var(--accent) !important}

.btn,.btn-p,.btn-g,.btn-o,.btn-d,.btn-sm,.btn-pur,.btn-amber{
  border-radius:12px !important;font-weight:600 !important;font-size:14px !important;
  transition:background var(--t),color var(--t),border-color var(--t),transform var(--t),box-shadow var(--t),opacity var(--t) !important;
}
.btn-p{background:var(--accent) !important;color:#fff !important;box-shadow:0 1px 2px rgba(37,99,235,.2) !important}
.btn-p:hover{background:var(--accent2) !important}
.btn-g,.btn-o{background:transparent !important;border:1px solid var(--card-b) !important;color:var(--t2) !important;box-shadow:none !important}
.btn-g:hover,.btn-o:hover{background:var(--accent-d) !important;color:var(--accent) !important;border-color:transparent !important}
.btn-d{background:var(--red-bg) !important;color:var(--red-t) !important;border:none !important}
.btn-sm{padding:7px 12px !important;font-size:13px !important;border-radius:10px !important}

.card,.cfg-card,.sub-card,.dash-chart-card,.vless-box,.stat-card-v2,.multi-group-card{
  background:var(--card) !important;
  border:1px solid var(--card-b) !important;
  border-radius:var(--r-md) !important;
  box-shadow:var(--shadow-md) !important;
}
.badge{border-radius:999px !important;font-weight:600 !important;font-size:11px !important;padding:3px 10px !important}
.badge.bg-blue{background:var(--accent-d) !important;color:var(--accent) !important}
.badge.bg-green{background:var(--green-bg) !important;color:var(--green-t) !important}
.badge.bg-red{background:var(--red-bg) !important;color:var(--red-t) !important}
.badge.bg-amber{background:var(--amber-bg) !important;color:var(--amber-t) !important}

.fi,.pw-input,.cm-input,.modal-v2-input,input[type="text"],input[type="password"],select,textarea{
  height:46px;border-radius:12px !important;border:1px solid var(--card-b) !important;
  background:var(--card) !important;color:var(--t1) !important;transition:border-color var(--t),box-shadow var(--t) !important;
}
.fi:focus,.pw-input:focus,.cm-input:focus,.modal-v2-input:focus,input:focus,select:focus,textarea:focus{
  border-color:var(--accent) !important;box-shadow:0 0 0 3px var(--accent-d) !important;outline:none;
}
::placeholder{color:#94A3B8 !important}

/* Overview layout */
.ov-topbar{display:flex;align-items:flex-start;justify-content:space-between;gap:16px;margin-bottom:20px;flex-wrap:wrap}
.ov-greeting{font-size:24px;font-weight:700;color:var(--t1);letter-spacing:-.03em;line-height:1.3}
.ov-sub{font-size:14px;color:var(--t2);margin-top:4px;font-weight:400}
.ov-top-actions{display:flex;gap:8px;flex-wrap:wrap}

.qa-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-bottom:20px}
@media(max-width:1000px){.qa-grid{grid-template-columns:repeat(3,1fr)}}
@media(max-width:560px){.qa-grid{grid-template-columns:repeat(2,1fr)}}
.qa-item{
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;
  padding:16px 10px;background:var(--card);border:1px solid var(--card-b);border-radius:var(--r-md);
  box-shadow:var(--shadow);cursor:pointer;font-family:inherit;color:var(--t1);
  transition:background var(--t),border-color var(--t),transform var(--t),box-shadow var(--t);
}
.qa-item i{font-size:20px;color:var(--accent)}
.qa-item span{font-size:12.5px;font-weight:600;color:var(--t2)}
.qa-item:hover{border-color:var(--accent);transform:translateY(-1px);box-shadow:var(--shadow-md)}
.qa-item:hover span{color:var(--t1)}

.stat-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:16px}
@media(max-width:900px){.stat-grid{grid-template-columns:1fr 1fr}}
@media(max-width:480px){.stat-grid{grid-template-columns:1fr}}
.stat-card-v2{padding:16px 18px;transition:border-color var(--t),box-shadow var(--t)}
.stat-card-v2:hover{border-color:var(--card-bh);box-shadow:var(--shadow-md)}
.stat-v2-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px}
.stat-v2-label{font-size:12.5px;font-weight:500;color:var(--t2)}
.stat-v2-ic{font-size:18px;color:var(--t3);opacity:.7}
.stat-v2-num{font-size:28px;font-weight:700;color:var(--t1);letter-spacing:-.03em;line-height:1.15}
.stat-v2-foot{margin-top:8px}
.stat-v2-hint{font-size:12px;color:var(--t3);font-weight:400}

.proto-strip{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px}
.proto-chip-v2{
  display:inline-flex;align-items:center;gap:6px;padding:7px 12px;
  background:var(--card);border:1px solid var(--card-b);border-radius:999px;
  font-size:12.5px;font-weight:600;color:var(--t2);
}
.proto-chip-v2 i{color:var(--accent);font-size:14px}

.ov-bottom{margin-top:4px;margin-bottom:8px}
.empty{text-align:center;padding:32px 16px;color:var(--t3)}
.empty i{font-size:32px;display:block;margin-bottom:10px;opacity:.5}
.empty p{font-size:14px;font-weight:500;color:var(--t2)}

/* modal backdrop */
.modal-bg,.modal-overlay,.lmodal-bg{backdrop-filter:blur(8px);background:rgba(15,23,42,.4) !important}

::-webkit-scrollbar{width:8px;height:8px}
::-webkit-scrollbar-thumb{background:var(--bg3);border-radius:999px}
::-webkit-scrollbar-track{background:transparent}

.tb-title{font-size:20px !important;font-weight:700 !important;letter-spacing:-.02em}
.tb-sub{font-size:13px !important;color:var(--t2) !important}

/* ===== Protocol Selection Tiles (iOS / Linear style) ===== */
.cm-opt-grid{display:flex;flex-direction:column;gap:8px;width:100%}
.cm-dd-list .cm-opt-grid{padding:4px 0}
.cm-opt{
  display:flex !important;
  align-items:center !important;
  gap:12px !important;
  padding:10px 12px !important;
  margin:0 !important;
  margin-bottom:0 !important;
  border-radius:12px !important;
  border:1px solid var(--card-b) !important;
  background:var(--card) !important;
  box-shadow:none !important;
  transform:none !important;
  cursor:pointer;
  min-height:0 !important;
  transition:background 180ms ease, border-color 180ms ease !important;
}
.cm-opt:hover{
  background:#F8FAFC !important;
  border-color:#CBD5E1 !important;
  transform:none !important;
  box-shadow:none !important;
}
.cm-opt.sel,
.cm-opt.on,
.cm-opt.selected,
.cm-opt.active{
  background:#EFF6FF !important;
  border-color:#2563EB !important;
  box-shadow:none !important;
}
[data-theme="dark"] .cm-opt{
  background:#1E293B !important;
  border-color:#334155 !important;
}
[data-theme="dark"] .cm-opt:hover{
  background:#243044 !important;
  border-color:#475569 !important;
}
[data-theme="dark"] .cm-opt.sel,
[data-theme="dark"] .cm-opt.on,
[data-theme="dark"] .cm-opt.selected{
  background:rgba(37,99,235,.12) !important;
  border-color:#3B82F6 !important;
}
.cm-opt-radio{
  width:16px !important;height:16px !important;min-width:16px !important;
  border-radius:50% !important;
  border:2px solid #CBD5E1 !important;
  background:transparent !important;
  flex-shrink:0 !important;
  display:flex !important;align-items:center;justify-content:center;
  margin:0 !important;
  transition:border-color 180ms ease !important;
}
.cm-opt.sel .cm-opt-radio{border-color:#2563EB !important}
[data-theme="dark"] .cm-opt-radio{border-color:#64748B !important}
[data-theme="dark"] .cm-opt.sel .cm-opt-radio{border-color:#60A5FA !important}
.cm-opt-radio::after{
  content:'' !important;
  width:8px !important;height:8px !important;
  border-radius:50% !important;
  background:#2563EB !important;
  transform:scale(0) !important;
  transition:transform 180ms ease !important;
  display:block !important;
}
.cm-opt.sel .cm-opt-radio::after{transform:scale(1) !important}
[data-theme="dark"] .cm-opt-radio::after{background:#60A5FA !important}
.cm-opt-icon{display:none !important}
.cm-opt-body,.cm-opt-text{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}
.cm-opt-row{display:flex;align-items:center;justify-content:space-between;gap:8px}
.cm-opt-title{
  font-size:13.5px !important;
  font-weight:600 !important;
  color:var(--t1) !important;
  letter-spacing:-.01em !important;
  line-height:1.3 !important;
}
.cm-opt-desc{
  font-size:11.5px !important;
  color:var(--t2) !important;
  line-height:1.45 !important;
  margin:0 !important;
  font-weight:400 !important;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
}
.cm-opt-tag{
  font-size:10px !important;
  font-weight:600 !important;
  padding:2px 7px !important;
  border-radius:999px !important;
  background:#EFF6FF !important;
  color:#2563EB !important;
  flex-shrink:0 !important;
  letter-spacing:0 !important;
  line-height:1.4 !important;
}
[data-theme="dark"] .cm-opt-tag{
  background:rgba(37,99,235,.15) !important;
  color:#93C5FD !important;
}
.cm-opt-tag.rec{
  background:#EFF6FF !important;
  color:#2563EB !important;
}
[data-theme="dark"] .cm-opt-tag.rec{
  background:rgba(37,99,235,.15) !important;
  color:#93C5FD !important;
}
</style>
</head>
<body>
<div class="toast" id="toast"></div>

<div class="modal-bg" id="modal-create-link">
  <div class="modal-v2 cm-modal">
    <button class="cm-close" onclick="closeModal('modal-create-link')"><i class="ti ti-x"></i></button>
    <div class="cm-head">
      <div class="cm-head-row">
        <div class="cm-head-icon" id="cm-head-icon"><i class="ti ti-plus"></i></div>
        <div>
          <div class="cm-head-title" id="cm-head-title">ساخت کانفیگ جدید</div>
          <div class="cm-head-sub" id="cm-head-sub">تنظیمات کامل پروتکل، ترابرد و محدودیت‌ها در یک صفحه</div>
        </div>
      </div>
    </div>

    <div class="cm-body">

      <!-- اطلاعات پایه -->
      <div class="cm-section">
        <div class="cm-section-label"><i class="ti ti-id-badge-2"></i> اطلاعات پایه</div>
        <div class="cm-field"><label>نام کانفیگ</label>
          <input class="cm-input" id="nl-label" placeholder="مثلاً: PlanAsli">
        </div>
        <div class="cm-field"><label>Path اختصاصی</label>
          <input class="cm-input" id="nl-path" dir="ltr" placeholder="PlanAsli">
          <div class="cm-note" style="margin-top:8px"><i class="ti ti-info-circle"></i> اگر بنویسید PlanAsli، مسیر WebSocket به شکل /ws/PlanAsli ساخته می‌شود.</div>
        </div>
        <div class="cm-row2">
          <div class="cm-field"><label>گروه ساب</label>
            <select class="cm-input" id="nl-sub"><option value="">— بدون گروه —</option></select>
          </div>
          <div class="cm-field"><label>یادداشت (اختیاری)</label>
            <input class="cm-input" id="nl-note" placeholder="توضیح کوتاه">
          </div>
        </div>
      </div>

      <!-- پروتکل و ترابرد: کشویی -->
      <div class="cm-section">
        <div class="cm-section-label"><i class="ti ti-plug-connected"></i> پروتکل و ترابرد</div>

        <div class="cm-dd open" id="dd-base">
          <div class="cm-dd-trigger" onclick="cmToggleDD('dd-base')">
            <div class="cm-dd-icon" id="dd-base-icon"><i class="ti ti-bolt"></i></div>
            <div class="cm-dd-text">
              <div class="cm-dd-title">پروتکل پایه — <span id="dd-base-current">VLESS</span></div>
              <div class="cm-dd-desc" id="dd-base-current-desc">سبک، سریع و پرکاربردترین گزینه</div>
            </div>
            <i class="ti ti-chevron-down cm-dd-chev"></i>
          </div>
          <div class="cm-dd-panel"><div class="cm-dd-panel-inner"><div class="cm-dd-list">
            <div class="cm-opt-grid">
            <div class="cm-opt sel" data-base="vless" onclick="cmSelectBase('vless',this)">
              <div class="cm-opt-radio"></div>
              <div class="cm-opt-body">
                <div class="cm-opt-row"><span class="cm-opt-title">VLESS</span><span class="cm-opt-tag rec">Recommended</span></div>
                <div class="cm-opt-desc">سبک، سریع و مناسب اکثر کاربران</div>
              </div>
            </div>
            <div class="cm-opt" data-base="trojan" onclick="cmSelectBase('trojan',this)">
              <div class="cm-opt-radio"></div>
              <div class="cm-opt-body">
                <div class="cm-opt-row"><span class="cm-opt-title">Trojan</span></div>
                <div class="cm-opt-desc">شبیه‌سازی ترافیک HTTPS</div>
              </div>
            </div>
            <div class="cm-opt" data-base="multi" onclick="cmSelectBase('multi',this)">
              <div class="cm-opt-radio"></div>
              <div class="cm-opt-body">
                <div class="cm-opt-row"><span class="cm-opt-title">Multi Protocol</span><span class="cm-opt-tag">All-in-one</span></div>
                <div class="cm-opt-desc">همه پروتکل‌ها در یک ساب</div>
              </div>
            </div>
            <div class="cm-opt" data-base="shadowsocks" onclick="cmSelectBase('shadowsocks',this)">
              <div class="cm-opt-radio"></div>
              <div class="cm-opt-body">
                <div class="cm-opt-row"><span class="cm-opt-title">Shadowsocks</span><span class="cm-opt-tag">TLS</span></div>
                <div class="cm-opt-desc">روی TLS / WebSocket</div>
              </div>
            </div>
            <div class="cm-opt" data-base="telproxy" onclick="cmSelectBase('telproxy',this)">
              <div class="cm-opt-radio"></div>
              <div class="cm-opt-body">
                <div class="cm-opt-row"><span class="cm-opt-title">Telegram Proxy</span><span class="cm-opt-tag">MTProto</span></div>
                <div class="cm-opt-desc">پروکسی تلگرام روی پورت داخلی</div>
              </div>
            </div>
            <div class="cm-opt" data-base="vless-tcp" onclick="cmSelectBase('vless-tcp',this)">
              <div class="cm-opt-radio"></div>
              <div class="cm-opt-body">
                <div class="cm-opt-row"><span class="cm-opt-title">VLESS TCP Proxy</span><span class="cm-opt-tag">Railway</span></div>
                <div class="cm-opt-desc">دامنه و پورت TCP Proxy ریلوی · بدون TLS</div>
              </div>
            </div>
            <div class="cm-opt" data-base="vless-reality" onclick="cmSelectBase('vless-reality',this)">
              <div class="cm-opt-radio"></div>
              <div class="cm-opt-body">
                <div class="cm-opt-row"><span class="cm-opt-title">VLESS Reality</span><span class="cm-opt-tag">TCP</span></div>
                <div class="cm-opt-desc">Reality با pbk / sid / sni</div>
              </div>
            </div>
            </div></div></div>
          </div>
        </div>

        <div class="cm-dd" id="transport-section">
          <div class="cm-dd-trigger" onclick="cmToggleDD('transport-section')">
            <div class="cm-dd-icon" id="dd-transport-icon"><i class="ti ti-link"></i></div>
            <div class="cm-dd-text">
              <div class="cm-dd-title">ترابرد — <span id="dd-transport-current">WebSocket</span></div>
              <div class="cm-dd-desc" id="dd-transport-current-desc">پایدار و سازگار با همه شرایط شبکه</div>
            </div>
            <i class="ti ti-chevron-down cm-dd-chev"></i>
          </div>
          <div class="cm-dd-panel" id="dd-transport"><div class="cm-dd-panel-inner"><div class="cm-dd-list">
            <div class="cm-opt sel" onclick="cmSelectTransport('ws',this)">
              <div class="cm-opt-radio"></div>
              <div class="cm-opt-body">
                <div class="cm-opt-row"><span class="cm-opt-title">WebSocket</span></div>
                <div class="cm-opt-desc">پایدارترین حالت عمومی</div>
              </div>
            </div>
            <div class="cm-opt" onclick="cmSelectTransport('xhttp-packet-up',this)">
              <div class="cm-opt-radio"></div>
              <div class="cm-opt-body">
                <div class="cm-opt-row"><span class="cm-opt-title">XHTTP packet-up</span></div>
                <div class="cm-opt-desc">سازگار با CDN و پروکسی</div>
              </div>
            </div>
            <div class="cm-opt" onclick="cmSelectTransport('xhttp-stream-up',this)">
              <div class="cm-opt-radio"></div>
              <div class="cm-opt-body">
                <div class="cm-opt-row"><span class="cm-opt-title">XHTTP stream-up</span></div>
                <div class="cm-opt-desc">تاخیر کمتر برای شبکه پایدار</div>
              </div>
            </div>
          </div></div></div>
        </div>

        <input type="hidden" id="nl-proto" value="vless-ws">

        <div class="cm-note" style="margin-top:12px" id="transport-note"><i class="ti ti-info-circle"></i> پروتکل و ترابرد پس از ساخت کانفیگ قابل تغییر نیستند.</div>
        <div class="cm-note" style="margin-top:12px;display:none" id="mtproto-note"><i class="ti ti-brand-telegram"></i> Telegram Proxy روی پورت داخلی پنل ساخته می‌شود. ابزار پروکسی Railway از این نسخه حذف شده است.</div>
        <div class="cm-note" style="margin-top:12px;display:none" id="tcp-note"><i class="ti ti-route"></i> از دامنه و پورت TCP Proxy ریلوی استفاده می‌شود. مقادیر پیش‌فرض از <b>تنظیمات</b> خوانده می‌شوند؛ اینجا می‌توانی برای همین کانفیگ override بگذاری.</div>
        <div class="cm-note" style="margin-top:12px;display:none" id="reality-note"><i class="ti ti-shield-lock"></i> لینک Reality با پارامترهای pbk/sid/sni ساخته می‌شود. مقادیر پیش‌فرض از <b>تنظیمات</b>؛ اینجا override اختیاری است.</div>

        <div class="cm-section" id="mtproto-port-field" style="display:none;margin-bottom:0">
          <div class="cm-row2">
            <div class="cm-field">
              <label><i class="ti ti-route" style="color:var(--accent);margin-left:4px"></i>پورت TCP</label>
              <input class="cm-input" id="nl-mtproto-port" type="number" min="1" max="65535" placeholder="خالی = خودکار">
            </div>
            <div class="cm-field">
              <label><i class="ti ti-server-2" style="color:var(--accent);margin-left:4px"></i>Fake TLS SNI</label>
              <input class="cm-input" id="nl-mtproto-domain" type="text" placeholder="www.cloudflare.com" oninput="cmClearSniPills()">
            </div>
          </div>
          <div class="cm-pills" style="margin-top:-4px;margin-bottom:10px">
            <span class="cm-pill active" onclick="cmSetSni('www.cloudflare.com',this)"><i class="ti ti-brand-cloudflare" style="margin-left:3px"></i>www.cloudflare.com</span>
            <span class="cm-pill" onclick="cmSetSni('www.google.com',this)">www.google.com</span>
            <span class="cm-pill" onclick="cmSetSni('www.microsoft.com',this)">www.microsoft.com</span>
            <span class="cm-pill" onclick="cmSetSni('www.amazon.com',this)">www.amazon.com</span>
          </div>
          <div class="cm-note" style="margin-top:0">
            <i class="ti ti-info-circle"></i>
            پورت خالی = یک پورت آزاد از بازه‌ی ۸۵۰۰–۸۶۰۰ خودکار انتخاب می‌شود. Fake SNI دامنه‌ای است که ترافیک پروکسی پشت آن پنهان می‌شود؛ می‌تونی خودت هر دامنه‌ای بذاری، پیش‌فرض پیشنهادی <b>www.cloudflare.com</b> است.
          </div>
        </div>

        <div class="cm-section" id="tcp-proxy-field" style="display:none;margin-bottom:0">
          <div class="cm-row2">
            <div class="cm-field">
              <label>دامنه TCP Proxy</label>
              <input class="cm-input" id="nl-tcp-domain" dir="ltr" placeholder="yamabiko.proxy.rlwy.net">
            </div>
            <div class="cm-field">
              <label>پورت TCP</label>
              <input class="cm-input" id="nl-tcp-port" type="number" min="1" max="65535" placeholder="49391">
            </div>
          </div>
          <div class="cm-field">
            <label>حالت Path</label>
            <select class="cm-input" id="nl-tcp-path-mode">
              <option value="root" selected>ساده — / (پیشنهادی)</option>
              <option value="panel">پنل — /ws/{path}</option>
            </select>
          </div>
        </div>

        <div class="cm-section" id="reality-field" style="display:none;margin-bottom:0">
          <div class="cm-row2">
            <div class="cm-field">
              <label>Host / IP</label>
              <input class="cm-input" id="nl-reality-host" dir="ltr" placeholder="66.33.22.241">
            </div>
            <div class="cm-field">
              <label>پورت</label>
              <input class="cm-input" id="nl-reality-port" type="number" min="1" max="65535" placeholder="443">
            </div>
          </div>
          <div class="cm-field">
            <label>Public Key (pbk)</label>
            <input class="cm-input" id="nl-reality-pbk" dir="ltr" placeholder="eXooS5Ko...">
          </div>
          <div class="cm-row2">
            <div class="cm-field">
              <label>Short ID (sid)</label>
              <input class="cm-input" id="nl-reality-sid" dir="ltr" placeholder="51ea838b11">
            </div>
            <div class="cm-field">
              <label>SNI</label>
              <input class="cm-input" id="nl-reality-sni" dir="ltr" placeholder="eventapi.semiconductor.samsung.com">
            </div>
          </div>
          <div class="cm-row2">
            <div class="cm-field">
              <label>Fingerprint (fp)</label>
              <input class="cm-input" id="nl-reality-fp" dir="ltr" placeholder="chrome" value="chrome">
            </div>
            <div class="cm-field">
              <label>SpiderX (spx)</label>
              <input class="cm-input" id="nl-reality-spx" dir="ltr" placeholder="/" value="/">
            </div>
          </div>
        </div>

      </div>

      <!-- محدودیت‌ها -->
      <div class="cm-section">
        <div class="cm-section-label"><i class="ti ti-adjustments"></i> محدودیت‌ها</div>
        <div class="cm-field">
          <label>سهمیه ترافیک</label>
          <div class="cm-row2">
            <input class="cm-input" id="nl-val" type="number" min="0" step="0.1" placeholder="0 = نامحدود">
            <select class="cm-input" id="nl-unit"><option value="GB">GB</option><option value="MB" selected>MB</option></select>
          </div>
          <div class="cm-pills">
            <span class="cm-pill" onclick="cmQuota(0,'GB',this)">نامحدود</span>
            <span class="cm-pill" onclick="cmQuota(500,'MB',this)">۵۰۰MB</span>
            <span class="cm-pill active" onclick="cmQuota(1,'GB',this)">۱GB</span>
            <span class="cm-pill" onclick="cmQuota(5,'GB',this)">۵GB</span>
            <span class="cm-pill" onclick="cmQuota(10,'GB',this)">۱۰GB</span>
            <span class="cm-pill" onclick="cmQuota(50,'GB',this)">۵۰GB</span>
          </div>
        </div>
        <div class="cm-field" style="margin-bottom:4px">
          <label>انقضا</label>
          <input class="cm-input" id="nl-exp" type="number" min="0" step="1" placeholder="روز · 0 = نامحدود">
          <div class="cm-pills">
            <span class="cm-pill" onclick="cmExpiry(0,this)">نامحدود</span>
            <span class="cm-pill" onclick="cmExpiry(7,this)">۷ روز</span>
            <span class="cm-pill active" onclick="cmExpiry(30,this)">۳۰ روز</span>
            <span class="cm-pill" onclick="cmExpiry(90,this)">۹۰ روز</span>
          </div>
        </div>
      </div>

    </div>

    <div class="cm-footer">
      <button class="cm-btn-cancel" onclick="closeModal('modal-create-link')">انصراف</button>
      <button class="cm-btn-submit" id="cm-submit-btn" onclick="createLink()"><i class="ti ti-link-plus" id="cm-submit-icon"></i> <span id="cm-submit-text">ساخت کانفیگ</span></button>    </div>
  </div>
</div>



<div class="modal-bg" id="modal-update" style="z-index:9999">
  <div class="modal-v2" style="max-width:460px">
    <div class="modal-v2-head" style="background:linear-gradient(155deg,rgba(37,99,235,.16) 0%,transparent 65%)">
      <button class="modal-v2-close" onclick="closeModal('modal-update')"><i class="ti ti-x"></i></button>
      <div class="modal-v2-icon" style="background:linear-gradient(135deg,var(--accent),var(--accent2))"><i class="ti ti-cloud-download"></i></div>
      <div class="modal-v2-title">بروزرسانی جدید موجود است</div>
      <div class="modal-v2-sub">نسخه‌ی جدید <span id="update-modal-version">—</span> آماده نصب است</div>
    </div>
    <div class="modal-v2-body">
      <div class="cl" style="margin-top:0">
        <i class="ti ti-info-circle"></i>
        <span id="update-modal-desc">توضیحات بروزرسانی...</span>
      </div>
      <div class="modal-v2-footer">
        <button class="btn btn-o" onclick="dismissUpdate()" style="flex:.6">انصراف</button>
        <button class="btn btn-p" onclick="startUpdateFromModal()" style="flex:1;justify-content:center"><i class="ti ti-download"></i> نصب بروزرسانی</button>
      </div>
    </div>
  </div>
</div>


<!-- OXNET v2.0.10 repaired action modals -->
<div class="modal-bg" id="modal-edit-link">
  <div class="modal-v2" style="max-width:520px">
    <button class="modal-v2-close" onclick="closeModal('modal-edit-link')"><i class="ti ti-x"></i></button>
    <div class="modal-v2-head"><div class="modal-v2-icon"><i class="ti ti-edit"></i></div><div class="modal-v2-title">ویرایش کانفیگ</div><div class="modal-v2-sub">نام، یادداشت، سهمیه و انقضا را تغییر بده.</div></div>
    <div class="modal-v2-body">
      <input type="hidden" id="el-uuid">
      <div class="modal-v2-field"><label><i class="ti ti-id"></i> نام</label><input class="modal-v2-input" id="el-label" placeholder="نام کانفیگ"></div>
      <div class="modal-v2-field"><label><i class="ti ti-note"></i> یادداشت</label><input class="modal-v2-input" id="el-note" placeholder="یادداشت"></div>
      <div class="form-row"><input class="fi" id="el-val" type="number" min="0" placeholder="سهمیه"><select class="fs" id="el-unit"><option value="GB">GB</option><option value="MB">MB</option></select><input class="fi" id="el-exp" type="number" min="0" placeholder="انقضا / روز"></div>
      <div class="modal-v2-footer"><button class="modal-v2-btn-cancel" onclick="closeModal('modal-edit-link')">انصراف</button><button class="modal-v2-btn-submit" onclick="saveEditLink()"><i class="ti ti-check"></i> ذخیره</button></div>
    </div>
  </div>
</div>

<div class="modal-bg" id="modal-create-sub">
  <div class="modal-v2" style="max-width:520px">
    <button class="modal-v2-close" onclick="closeModal('modal-create-sub')"><i class="ti ti-x"></i></button>
    <div class="modal-v2-head"><div class="modal-v2-icon"><i class="ti ti-folder-plus"></i></div><div class="modal-v2-title">گروه جدید</div><div class="modal-v2-sub">برای دسته‌بندی کانفیگ‌ها و ساخت صفحه عمومی.</div></div>
    <div class="modal-v2-body">
      <div class="modal-v2-field"><label><i class="ti ti-folder"></i> نام گروه</label><input class="modal-v2-input" id="ns-name" placeholder="مثلاً مشتری‌های ویژه"></div>
      <div class="modal-v2-field"><label><i class="ti ti-notes"></i> توضیح</label><input class="modal-v2-input" id="ns-desc" placeholder="توضیح اختیاری"></div>
      <div class="modal-v2-field"><label><i class="ti ti-lock"></i> رمز صفحه عمومی</label><input class="modal-v2-input" id="ns-pw" type="password" placeholder="خالی = بدون رمز"></div>
      <div class="modal-v2-footer"><button class="modal-v2-btn-cancel" onclick="closeModal('modal-create-sub')">انصراف</button><button class="modal-v2-btn-submit" onclick="createSub()"><i class="ti ti-folder-plus"></i> ساخت گروه</button></div>
    </div>
  </div>
</div>

<div class="modal-bg" id="modal-links">
  <div class="modal-v2" style="max-width:720px">
    <button class="modal-v2-close" onclick="closeModal('modal-links')"><i class="ti ti-x"></i></button>
    <div class="lmodal-head">
      <div class="lmodal-icon-row"><div class="lmodal-icon"><i class="ti ti-link-plus"></i></div><div><div class="lmodal-title-v2">کانفیگ‌های گروه: <span id="modal-sub-name">—</span></div><div class="lmodal-sub-v2">کانفیگ‌هایی که باید داخل این گروه باشند را انتخاب کن.</div></div></div>
      <div class="lmodal-search"><input id="lmodal-search-inp" placeholder="جستجو..." oninput="filterLmodal(this.value)"><i class="ti ti-search"></i></div>
      <div class="lmodal-quickbar"><button class="lmodal-qbtn" onclick="lmodalSelectAll(true)">انتخاب همه</button><button class="lmodal-qbtn" onclick="lmodalSelectAll(false)">حذف انتخاب</button><span class="lmodal-count" id="lmodal-count">۰ انتخاب شده</span></div>
    </div>
    <div class="lmodal-list" id="modal-links-body"></div>
    <div class="lmodal-footer"><div class="lmodal-footer-info"><i class="ti ti-info-circle"></i> تغییرات بعد از ذخیره اعمال می‌شود.</div><div class="lmodal-footer-btns"><button class="btn btn-o" onclick="closeModal('modal-links')">انصراف</button><button class="btn btn-p" onclick="saveSubLinks()"><i class="ti ti-device-floppy"></i> ذخیره</button></div></div>
  </div>
</div>

<div class="modal-bg" id="modal-ad-tag">
  <div class="modal-v2" style="max-width:520px">
    <button class="modal-v2-close" onclick="closeModal('modal-ad-tag')"><i class="ti ti-x"></i></button>
    <div class="modal-v2-head"><div class="modal-v2-icon"><i class="ti ti-speakerphone"></i></div><div class="modal-v2-title">تبلیغ کانال</div><div class="modal-v2-sub" id="at-cfg-name">—</div></div>
    <div class="modal-v2-body"><div class="modal-v2-field"><label>ad_tag</label><input class="modal-v2-input" id="at-tag" dir="ltr" placeholder="ad tag"></div><div class="modal-v2-footer"><button class="modal-v2-btn-cancel" onclick="closeModal('modal-ad-tag')">انصراف</button><button class="modal-v2-btn-submit" id="at-submit-btn" onclick="submitAdTag()"><i class="ti ti-check"></i> ذخیره و اعمال</button></div></div>
  </div>
</div>

<div class="modal-bg" id="modal-mt-info">
  <div class="modal-v2" style="max-width:620px">
    <button class="modal-v2-close" onclick="closeModal('modal-mt-info')"><i class="ti ti-x"></i></button>
    <div class="modal-v2-head"><div class="modal-v2-icon"><i class="ti ti-brand-telegram"></i></div><div class="modal-v2-title">اطلاعات پروکسی</div><div class="modal-v2-sub" id="mti-cfg-name">—</div></div>
    <div class="modal-v2-body">
      <div class="cl amber" id="mti-warn"><i class="ti ti-alert-triangle"></i><span>دامنه عمومی هنوز آماده نشده است.</span></div>
      <div class="modal-v2-field"><label>Secret</label><div class="vl-code" id="mti-secret">—</div><button class="btn btn-g btn-sm" onclick="cpMtiField('mti-secret','سکرت کپی شد')"><i class="ti ti-copy"></i> کپی</button></div>
      <div class="modal-v2-field"><label>Link</label><div class="vl-code" id="mti-link">—</div><button class="btn btn-p btn-sm" onclick="cpMtiField('mti-link','لینک کپی شد')"><i class="ti ti-copy"></i> کپی لینک</button></div>
    </div>
  </div>
</div>



<div class="mob-top">
  <div class="ml">
    <div class="brand-mark small"><i class="ti ti-network"></i></div>
    <span class="mob-title">OXNET</span>
  </div>
  <div class="mob-right">
    <button class="theme-mob" id="theme-mob-btn" onclick="toggleTheme()"><i class="ti ti-sun" id="theme-mob-icon"></i></button>
    <button class="menu-btn" id="open-sb"><i class="ti ti-menu-2"></i></button>
  </div>
</div>
<div class="overlay" id="overlay"></div>
<aside class="sidebar" id="sb">
  <button class="sb-close" id="close-sb"><i class="ti ti-x"></i></button>
  <div class="logo">
    <div class="brand-mark small"><i class="ti ti-network"></i></div>
    <div><div class="logo-name">OXNET</div><div class="logo-sub">OXNET Stable · v2.0.10</div></div>
  </div>
  <div class="nav-wrap">
    <div class="nav-sec">پنل</div>
    <div class="nav-it on" data-pg="overview"><i class="ti ti-layout-dashboard"></i> داشبورد</div>
    <div class="nav-it" data-pg="links"><i class="ti ti-link-plus"></i> کانفیگ‌ها <span class="nav-badge" id="links-nb">0</span></div>
    <div class="nav-it" data-pg="subgroups"><i class="ti ti-folders"></i> گروه‌های ساب <span class="nav-badge" id="subs-nb">0</span></div>
    <div class="nav-it" data-pg="subscriptions"><i class="ti ti-rss"></i> سابسکریپشن</div>
    <div class="nav-it" data-pg="traffic"><i class="ti ti-chart-area"></i> ترافیک</div>
    <div class="nav-it" data-pg="connections"><i class="ti ti-plug-connected"></i> اتصالات <span class="nav-badge" id="conns-nb">0</span></div>
    <div class="nav-it" data-pg="customers"><i class="ti ti-users"></i> کاربران</div>
    <div class="nav-it" data-pg="cloudflare"><i class="ti ti-cloud"></i> کلادفلیر</div>
    <div class="nav-sec">سیستم</div>
    <div class="nav-it" data-pg="security"><i class="ti ti-shield-lock"></i> امنیت</div>
    <div class="nav-it" data-pg="logs"><i class="ti ti-history"></i> لاگ فعالیت‌ها</div>
    <div class="nav-it" data-pg="errors"><i class="ti ti-alert-triangle"></i> خطاها</div>
    <div class="nav-it" data-pg="settings"><i class="ti ti-settings"></i> تنظیمات</div>
  </div>
  <div class="sb-foot">
    <button class="theme-btn" onclick="toggleTheme()"><i class="ti ti-moon" id="theme-icon"></i> <span id="theme-label">تم روشن</span></button>
    <button class="logout-btn" id="logout-btn"><i class="ti ti-logout"></i> خروج</button>
  </div>
</aside>
<main class="main">
<div class="ann-banner-wrap" id="ann-banner-wrap"></div>
<section class="pg on" id="pg-overview">
  <div class="ov-topbar">
    <div>
      <div class="ov-greeting" id="ov-greeting">سلام، خوش آمدید</div>
      <div class="ov-sub">نمای کلی لبه شبکه، پهنای باند و مسیرهای فعال</div>
    </div>
    <div class="ov-top-actions">
      <button class="btn btn-o btn-sm" onclick="dashRefresh()"><i class="ti ti-refresh"></i> بروزرسانی</button>
      <button class="btn btn-p btn-sm" onclick="dashCreateConfig()"><i class="ti ti-plus"></i> کانفیگ جدید</button>
    </div>
  </div>

  <div class="qa-grid">
    <button type="button" class="qa-item" onclick="dashCreateConfig()"><i class="ti ti-plus"></i><span>ساخت کانفیگ</span></button>
    <button type="button" class="qa-item" onclick="navTo('subs')"><i class="ti ti-folders"></i><span>گروه ساب</span></button>
    <button type="button" class="qa-item" onclick="navTo('traffic')"><i class="ti ti-chart-area"></i><span>ترافیک</span></button>
    <button type="button" class="qa-item" onclick="navTo('connections')"><i class="ti ti-plug-connected"></i><span>اتصالات</span></button>
    <button type="button" class="qa-item" onclick="navTo('cloudflare')"><i class="ti ti-cloud"></i><span>کلادفلیر</span></button>
    <button type="button" class="qa-item" onclick="navTo('settings')"><i class="ti ti-settings"></i><span>تنظیمات</span></button>
  </div>

  <div class="stat-grid">
    <div class="stat-card-v2">
      <div class="stat-v2-top"><span class="stat-v2-label">اتصالات زنده</span><i class="ti ti-plug-connected stat-v2-ic"></i></div>
      <div class="stat-v2-num" id="m-conns">—</div>
      <div class="stat-v2-foot"><span class="stat-v2-hint">نشست‌های فعال</span><canvas class="spark" id="spark-conns" width="120" height="28"></canvas></div>
    </div>
    <div class="stat-card-v2">
      <div class="stat-v2-top"><span class="stat-v2-label">ترافیک کل</span><i class="ti ti-transfer stat-v2-ic"></i></div>
      <div class="stat-v2-num" id="m-traffic">—</div>
      <div class="stat-v2-foot"><span class="stat-v2-hint">از شروع سرویس</span><canvas class="spark" id="spark-traffic" width="120" height="28"></canvas></div>
    </div>
    <div class="stat-card-v2">
      <div class="stat-v2-top"><span class="stat-v2-label">کانفیگ فعال</span><i class="ti ti-link stat-v2-ic"></i></div>
      <div class="stat-v2-num" id="m-alinks">—</div>
      <div class="stat-v2-foot"><span class="stat-v2-hint" id="m-lsub">کل لینک‌ها</span><canvas class="spark" id="spark-links" width="120" height="28"></canvas></div>
    </div>
    <div class="stat-card-v2">
      <div class="stat-v2-top"><span class="stat-v2-label">گروه ساب</span><i class="ti ti-folders stat-v2-ic"></i></div>
      <div class="stat-v2-num" id="m-subs">—</div>
      <div class="stat-v2-foot"><span class="stat-v2-hint">صفحات عمومی</span><canvas class="spark" id="spark-subs" width="120" height="28"></canvas></div>
    </div>
  </div>

  <div class="proto-strip">
    <div class="proto-chip-v2"><i class="ti ti-bolt"></i> VLESS WS</div>
    <div class="proto-chip-v2"><i class="ti ti-route"></i> TCP Proxy</div>
    <div class="proto-chip-v2"><i class="ti ti-shield-lock"></i> Reality</div>
    <div class="proto-chip-v2"><i class="ti ti-shield-lock"></i> Trojan WS</div>
    <div class="proto-chip-v2"><i class="ti ti-lock"></i> Shadowsocks TLS</div>
    <div class="proto-chip-v2"><i class="ti ti-package"></i> XHTTP</div>
  </div>

  <div class="vless-box">
    <div class="vl-header">
      <div class="vl-title"><i class="ti ti-link"></i> لینک فعال پیشنهادی</div>
      <span class="badge bg-blue"><span class="dot db"></span> TLS 443</span>
    </div>
    <div class="vl-code" id="vless-main">در حال دریافت...</div>
    <div class="vl-actions">
      <button class="btn btn-p" onclick="cpText('vless-main')"><i class="ti ti-copy"></i> کپی</button>
      <button class="btn btn-g" onclick="qrFor('vless-main')"><i class="ti ti-qrcode"></i> QR</button>
      <button class="btn btn-o" onclick="navTo('links')"><i class="ti ti-list"></i> کانفیگ‌ها</button>
    </div>
  </div>

  <div class="dash-chart-grid">
    <div class="dash-chart-card">
      <div class="dash-card-head">
        <div>
          <div class="dash-card-title"><i class="ti ti-chart-area"></i> ترافیک (ساعتی)</div>
          <div class="dash-card-sub">Upload / مصرف — ۳۰ بازه اخیر</div>
        </div>
        <span class="badge bg-blue" id="uptime-badge">—</span>
      </div>
      <div class="ch"><canvas id="ch1"></canvas></div>
    </div>
    <div class="dash-chart-card">
      <div class="dash-card-head">
        <div>
          <div class="dash-card-title"><i class="ti ti-chart-donut"></i> کاربران بر اساس پروتکل</div>
          <div class="dash-card-sub">سهم پروتکل‌های فعال</div>
        </div>
      </div>
      <div class="ch-sm"><canvas id="ch2"></canvas><div class="donut-center"><div class="dc-num" id="donut-total">—</div><div class="dc-sub">کل کانفیگ</div></div></div>
    </div>
  </div>

  <div class="g2 ov-bottom">
    <div class="card">
      <div class="card-title"><i class="ti ti-activity"></i> سلامت سرویس</div>
      <div class="sr"><span class="sr-k"><i class="ti ti-shield-check"></i> Path Auth</span><span class="sr-v" style="color:var(--green-t)">فعال</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-clock"></i> آپتایم</span><span class="sr-v" id="uptime-inline">—</span></div>
      <div class="sr" style="flex-direction:column;align-items:flex-start;gap:6px">
        <div style="width:100%;display:flex;justify-content:space-between"><span class="sr-k"><i class="ti ti-gauge"></i> بار نسبی</span><span class="sr-v" id="bw-pct">—%</span></div>
        <div class="spbar" style="width:100%"><div class="spfill" id="bw-bar" style="width:0%"></div></div>
      </div>
    </div>
    <div class="card">
      <div class="card-title"><i class="ti ti-list"></i> خلاصه کانفیگ‌ها <span class="ml-auto badge bg-blue" id="lsummary-badge">۰</span></div>
      <div id="lsummary">—</div>
    </div>
  </div>
</section>
<section class="pg" id="pg-links">
  <div class="topbar">
    <div style="display:flex;justify-content:flex-end;gap:8px;margin-bottom:16px">
      <button class="btn btn-p" onclick="resetCreateModal();openModal('modal-create-link')">
        <i class="ti ti-plus"></i> ساخت کانفیگ جدید
      </button>
    </div>
    <div class="tb-right">
      <span class="badge bg-blue" id="links-pg-cnt">۰ کانفیگ</span>
    </div>
  </div>

  <div class="info-strip">
    <div class="info-item">
      <span class="info-item-label">ارسال / دریافت لحظه‌ای</span>
      <span class="info-item-val"><i class="ti ti-arrows-exchange"></i> <span id="info-sent-recv">0 B / 0 B</span></span>
    </div>
    <div class="info-item">
      <span class="info-item-label">مصرف دوره فعلی</span>
      <span class="info-item-val"><i class="ti ti-chart-pie"></i> <span id="info-usage">0 B</span></span>
    </div>
    <div class="info-item">
      <span class="info-item-label">مصرف کل از ابتدا</span>
      <span class="info-item-val"><i class="ti ti-history"></i> <span id="info-alltime">0 B</span></span>
    </div>
    <div class="info-item">
      <span class="info-item-label">تعداد این‌باندها</span>
      <span class="info-item-val"><i class="ti ti-list-details"></i> <span id="info-inbounds">0</span></span>
    </div>
    <div class="info-item">
      <span class="info-item-label">کلاینت‌ها</span>
      <span class="info-item-val"><i class="ti ti-users"></i> <span class="info-badge" id="info-clients">0</span></span>
    </div>
  </div>

  <div class="cfg-grid" id="links-grid"></div>
  <div class="empty" id="links-empty" style="display:none"><i class="ti ti-link-off"></i><p>هنوز کانفیگی وجود ندارد</p></div>
</section>
<section class="pg" id="pg-subgroups">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-folders"></i> گروه‌های ساب</div><div class="tb-sub">هر گروه یک صفحه پابلیک مجزا با کانفیگ‌های خودش دارد</div></div>
    <div class="tb-right">
      <span class="badge bg-purple" id="subs-pg-cnt">۰ گروه</span>
      <button class="btn btn-pur" onclick="openModal('modal-create-sub')"><i class="ti ti-folder-plus"></i> گروه جدید</button>
    </div>
  </div>
  <div class="subs-toolbar">
    <div class="subs-search">
      <i class="ti ti-search"></i>
      <input type="text" id="subs-search-inp" placeholder="جستجو در گروه‌ها..." oninput="filterSubs(this.value)">
    </div>
  </div>
  <div class="sub-grid" id="subs-grid">
    <div class="subs-empty-v2"><div class="subs-empty-v2-icon"><i class="ti ti-folders"></i></div><div class="subs-empty-v2-title">هنوز گروهی وجود ندارد</div><div class="subs-empty-v2-sub">یک گروه جدید بسازید تا کانفیگ‌ها را دسته‌بندی کنید</div></div>
  </div>
</section>
<section class="pg" id="pg-subscriptions">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-rss"></i> سابسکریپشن</div><div class="tb-sub">لینک‌های اشتراک برای اپ‌های v2ray</div></div></div>
  <div class="g2">
    <div class="card">
      <div class="card-title"><i class="ti ti-rss"></i> سابسکریپشن تکی (هر کانفیگ)</div>
      <p style="font-size:11.5px;color:var(--t3);line-height:1.8;margin-bottom:12px">هر کانفیگ URL سابسکریپشن مخصوص دارد. از کارت کانفیگ روی آیکون <i class="ti ti-rss"></i> کلیک کنید.</p>
    </div>
    <div class="card">
      <div class="card-title"><i class="ti ti-database"></i> سابسکریپشن کامل (ادمین)</div>
      <p style="font-size:11.5px;color:var(--t3);line-height:1.8;margin-bottom:4px">شامل تمام کانفیگ‌های فعال.</p>
      <div class="sub-box"><span class="sub-url" id="sub-all-url">در حال دریافت...</span><div style="display:flex;gap:6px"><button class="btn btn-sm btn-g" onclick="cpSubAll()"><i class="ti ti-copy"></i></button><button class="btn btn-sm btn-g" onclick="window.open(location.protocol+'//'+location.host+'/sub-all')"><i class="ti ti-external-link"></i></button></div></div>
      <div class="cl amber" style="margin-top:11px"><i class="ti ti-alert-triangle"></i><span>این آدرس فقط در مرورگری که به پنل وارد شده کار می‌کند (نیاز به کوکی سشن).</span></div>
    </div>
  </div>
  <div class="card">
    <div class="card-title"><i class="ti ti-folders"></i> لینک سابسکریپشن گروه‌ها</div>
    <div id="sub-groups-list">در حال بارگذاری...</div>
  </div>
</section>
<section class="pg" id="pg-traffic">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-chart-area"></i> ترافیک</div><div class="tb-sub">تحلیل و مانیتورینگ مصرف پهنای باند</div></div>
    <div class="tb-right"><button class="btn btn-p btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i> رفرش</button></div>
  </div>

  <div class="traf-hero">
    <div class="traf-main-stat">
      <div class="traf-main-label"><i class="ti ti-database"></i> کل ترافیک مصرفی</div>
      <div class="traf-main-val" id="t-traffic">—<span>MB</span></div>
      <div class="traf-trend up" id="t-trend"><i class="ti ti-trending-up"></i> <span id="t-trend-val">—</span></div>
    </div>
    <div class="traf-mini">
      <div class="traf-mini-top"><div class="traf-mini-icon"><i class="ti ti-arrow-up-right"></i></div><span class="traf-mini-label">میانگین ساعتی</span></div>
      <div><div class="traf-mini-val" id="t-avg">—</div><div class="traf-mini-sub">MB در ساعت</div></div>
    </div>
    <div class="traf-mini">
      <div class="traf-mini-top"><div class="traf-mini-icon pk"><i class="ti ti-chart-bar"></i></div><span class="traf-mini-label">پیک مصرف</span></div>
      <div><div class="traf-mini-val" id="t-peak">—</div><div class="traf-mini-sub" id="t-peak-time">بالاترین ساعت</div></div>
    </div>
    <div class="traf-mini">
      <div class="traf-mini-top"><div class="traf-mini-icon lo"><i class="ti ti-clock-hour-4"></i></div><span class="traf-mini-label">کمترین مصرف</span></div>
      <div><div class="traf-mini-val" id="t-low">—</div><div class="traf-mini-sub">MB در ساعت</div></div>
    </div>
  </div>

  <div class="traf-chart-card">
    <div class="traf-chart-head">
      <div>
        <div class="traf-chart-title"><i class="ti ti-activity"></i> روند مصرف ترافیک</div>
        <div class="traf-chart-sub">بر اساس مگابایت در هر ساعت</div>
      </div>
      <div class="traf-legend">
        <div class="traf-legend-item"><span class="traf-legend-dot" style="background:var(--accent)"></span> مصرف</div>
        <div class="traf-legend-item"><span class="traf-legend-dot" style="background:var(--amber)"></span> میانگین</div>
      </div>
    </div>
    <div class="traf-chart-body"><canvas id="ch3"></canvas></div>
  </div>
</section>
<section class="pg" id="pg-connections">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-plug-connected"></i> اتصالات فعال</div><div class="tb-sub">مانیتورینگ زنده‌ی آی‌پی و ترافیک هر اتصال</div></div>
    <div class="tb-right"><span class="badge bg-green" id="conns-live">—</span><button class="btn btn-p btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i> رفرش</button></div>
  </div>

  <div class="conn-hero">
    <div class="conn-hero-tile">
      <div class="conn-hero-icon"><i class="ti ti-plug-connected"></i></div>
      <div class="conn-hero-label">اتصالات زنده</div>
      <div class="conn-hero-val" id="ch-count">—</div>
    </div>
    <div class="conn-hero-tile">
      <div class="conn-hero-icon"><i class="ti ti-transfer"></i></div>
      <div class="conn-hero-label">مجموع ترافیک لحظه‌ای</div>
      <div class="conn-hero-val" id="ch-traffic">—</div>
    </div>
    <div class="conn-hero-tile">
      <div class="conn-hero-icon"><i class="ti ti-clock"></i></div>
      <div class="conn-hero-label">میانگین مدت اتصال</div>
      <div class="conn-hero-val" id="ch-avgdur">—</div>
    </div>
    <div class="conn-hero-tile">
      <div class="conn-hero-icon"><i class="ti ti-map-pin"></i></div>
      <div class="conn-hero-label">آی‌پی‌های یکتا</div>
      <div class="conn-hero-val" id="ch-uniq">—</div>
    </div>
  </div>

  <div class="conn-toolbar">
    <div class="conn-toolbar-title"><i class="ti ti-list-details"></i> لیست اتصالات</div>
    <div class="conn-live-badge"><span class="conn-live-dot"></span> بروزرسانی خودکار هر ۵ ثانیه</div>
  </div>

  <div class="conn-grid-v2" id="conns-grid"></div>
  <div class="conn-empty-v2" id="conns-empty" style="display:none">
    <div class="conn-empty-v2-icon"><i class="ti ti-plug-off"></i></div>
    <div class="conn-empty-v2-title">هیچ اتصال فعالی نیست</div>
    <div class="conn-empty-v2-sub">به محض اتصال کلاینت‌ها، اینجا نمایش داده می‌شوند</div>
  </div>
</section>

<section class="pg" id="pg-customers">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-users"></i> کاربران و مشتری‌ها</div><div class="tb-sub">مدیریت کاربر، یادداشت، وضعیت و اتصال به کانفیگ‌ها</div></div><div class="tb-right"><button class="btn btn-p btn-sm" onclick="createCustomer()"><i class="ti ti-user-plus"></i> کاربر جدید</button></div></div>
  <div class="card"><div class="form-row" style="margin-bottom:12px"><input class="fi" id="cust-name" placeholder="نام کاربر" style="flex:1"><input class="fi" id="cust-phone" placeholder="موبایل/شناسه" style="flex:1"><input class="fi" id="cust-note" placeholder="یادداشت" style="flex:1"></div><div id="customers-list">—</div></div>
</section>

<section class="pg" id="pg-cloudflare">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-cloud"></i> کلادفلیر</div><div class="tb-sub">دامنه Cloudflare جدا از دامنه اصلی پنل؛ ساخت ساب با Host/SNI دامنه و Clean IPهای دلخواه</div></div><div class="tb-right"><button class="btn btn-p btn-sm" onclick="saveCloudflareDomain()"><i class="ti ti-device-floppy"></i> ذخیره دامنه</button></div></div>
  <div class="g2">
    <div class="card">
      <div class="card-title"><i class="ti ti-world-www"></i> ثبت دامنه Cloudflare</div>
      <div class="cl" style="margin-top:0;margin-bottom:12px"><i class="ti ti-info-circle"></i><span>دامنه‌ای که روی Cloudflare به همین پنل وصل کرده‌ای را وارد کن. این بخش یک Sub جدا می‌سازد و لینک‌های کانفیگ‌ها را با Host/SNI همان دامنه تولید می‌کند.</span></div>
      <div class="fg"><label>دامنه Cloudflare</label><input class="fi" id="cf-domain" dir="ltr" placeholder="sub.example.com" style="width:100%"></div>
      <div class="fg" style="margin-top:12px"><label>نام نمایشی</label><input class="fi" id="cf-name" placeholder="Cloudflare Main" style="width:100%"></div>
      <input type="hidden" id="cf-edit-key" value="">
      <div class="fg" style="margin-top:12px"><label>IP تمیز</label><textarea class="fi" id="cf-ips" dir="ltr" placeholder="هر خط یک IP، IPv6 یا دامنه تمیز&#10;104.16.1.1&#10;2606:4700:9c67:fc3d:7eb9:81b1:9156:fc79" style="width:100%;min-height:170px"></textarea></div>
      <div class="cl" style="margin-top:12px"><i class="ti ti-route"></i><span>IPv4، IPv6 و دامنه پشتیبانی می‌شود. اگر ۵۰ IP تمیز وارد کنی، در Sub کلادفلیر برای هر کانفیگ ۵۰ لینک ساخته می‌شود؛ آدرس کانفیگ IP تمیز است اما Host و SNI همان دامنه Cloudflare می‌ماند.</span></div>
    </div>
    <div class="card"><div class="card-title"><i class="ti ti-list-details"></i> دامنه‌های Cloudflare <span class="ml-auto badge bg-blue" id="cf-count">۰</span></div><div id="cf-list">در حال بارگذاری...</div></div>
  </div>
  <div class="g2" style="margin-top:16px">
    <div class="card">
      <div class="card-title"><i class="ti ti-link"></i> دامنه فرعی</div>
      <div class="cl" style="margin-top:0;margin-bottom:12px"><i class="ti ti-info-circle"></i><span>دامنه فرعی جدا از دامنه اصلی و Cloudflare است. مثل کلادفلیر می‌توانی برای آن <b>IP یا دامنه تمیز</b> تعریف کنی؛ در ساب برای هر IP یک کانفیگ با SNI همان دامنه فرعی ساخته می‌شود.</span></div>
      <div class="fg"><label>دامنه فرعی</label><input class="fi" id="ex-domain" dir="ltr" placeholder="cdn2.example.com" style="width:100%"></div>
      <div class="fg" style="margin-top:12px"><label>نام نمایشی</label><input class="fi" id="ex-name" placeholder="CDN Secondary" style="width:100%"></div>
      <div class="fg" style="margin-top:12px"><label>IP / دامنه تمیز</label><textarea class="fi" id="ex-ips" dir="ltr" placeholder="هر خط یک IP یا دامنه تمیز&#10;1.2.3.4&#10;clean.example.com" style="width:100%;min-height:120px"></textarea></div>
      <input type="hidden" id="ex-edit-key" value="">
      <div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap">
        <button class="btn btn-p btn-sm" onclick="saveExtraDomain()"><i class="ti ti-device-floppy"></i> ذخیره دامنه فرعی</button>
      </div>
    </div>
    <div class="card"><div class="card-title"><i class="ti ti-list"></i> دامنه‌های فرعی ثبت‌شده <span class="ml-auto badge bg-blue" id="ex-count">۰</span></div><div id="ex-list">در حال بارگذاری...</div></div>
  </div>
</section>

<section class="pg" id="pg-security">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-shield-lock"></i> امنیت</div></div></div>
  <div class="g2">
    <div class="card">
      <div class="card-title"><i class="ti ti-lock"></i> رمزنگاری</div>
      <div class="sr"><span class="sr-k"><i class="ti ti-certificate"></i> TLS/HTTPS</span><span class="sr-v" style="color:var(--green-t)">● فعال (443)</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-fingerprint"></i> Fingerprint</span><span class="sr-v">Chrome Spoof</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-network"></i> پروتکل‌ها</span><span class="sr-v">VLESS/WS + XHTTP Ultra</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-key"></i> هش رمز</span><span class="sr-v">SHA-256+Salt</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-cookie"></i> سشن</span><span class="sr-v">HttpOnly · 7 روز</span></div>
    </div>
    <div class="card">
      <div class="card-title"><i class="ti ti-shield-check"></i> کنترل دسترسی</div>
      <div class="sr"><span class="sr-k"><i class="ti ti-id-badge"></i> Path Auth اختصاصی</span><span class="sr-v" style="color:var(--green-t)">● فعال v1</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-toggle-right"></i> فعال/غیرفعال کانفیگ</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-gauge"></i> سهمیه ترافیک</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-calendar-x"></i> تاریخ انقضا</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-lock"></i> رمز صفحه پابلیک ساب</span><span class="sr-v" style="color:var(--green-t)">● اختیاری · SHA-256</span></div>
      <div class="form-row" style="margin-top:12px"><input class="fi" id="sec-max" type="number" placeholder="حداکثر تلاش ورود"><input class="fi" id="sec-min" type="number" placeholder="دقیقه قفل"><input class="fi" id="sec-ips" placeholder="IPهای مجاز با کاما"></div>
      <button class="btn btn-p btn-sm" onclick="saveSecuritySettings()"><i class="ti ti-shield-check"></i> ذخیره امنیت</button>
    </div>
  </div>
</section>
<section class="pg" id="pg-logs">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-history"></i> لاگ فعالیت‌ها</div><div class="tb-sub">تاریخچه‌ی کامل رخدادهای پنل</div></div><div class="tb-right"><button class="btn btn-p btn-sm" onclick="loadActivity()"><i class="ti ti-refresh"></i></button></div></div>
  <div class="card"><div class="log-timeline" id="logs-list">—</div><div class="empty" id="logs-empty" style="display:none"><i class="ti ti-history-toggle"></i><p>هنوز لاگی ثبت نشده</p></div></div>
</section>
<section class="pg" id="pg-errors">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-alert-triangle"></i> خطاها</div></div><div class="tb-right"><span class="badge bg-red" id="errs-badge">۰</span><button class="btn btn-p btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i></button></div></div>
  <div class="card"><div class="card-title"><i class="ti ti-bug"></i> لاگ خطاها</div><div id="errs-full">—</div></div>
</section>
<section class="pg" id="pg-updates">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-cloud-download"></i> نسخه و بروزرسانی</div><div class="tb-sub">مدیریت نسخه‌ی پنل و تاریخچه‌ی کامل بروزرسانی‌ها</div></div>
    <div class="tb-right"><button class="btn btn-p btn-sm" onclick="loadVersion()"><i class="ti ti-refresh"></i> بررسی مجدد</button></div>
  </div>

  <div class="upd-hero" id="upd-hero">
    <div class="upd-hero-glow"></div>
    <div class="upd-hero-top">
      <div class="upd-hero-cur">
        <div class="upd-hero-icon"><i class="ti ti-package"></i></div>
        <div>
          <div class="upd-hero-label">نسخه‌ی نصب‌شده</div>
          <div class="upd-hero-ver" id="ver-current">—</div>
        </div>
      </div>
      <div class="upd-hero-status" id="ver-status-badge">
        <span class="upd-pill upd-pill-blue"><span class="upd-dot"></span> در حال بررسی...</span>
      </div>
    </div>
    <div class="upd-hero-desc" id="ver-current-desc">—</div>
    <div class="upd-hero-meta">
      <span class="upd-meta-chip"><i class="ti ti-brand-github"></i> <span id="ver-repo">—</span></span>
      <span class="upd-meta-chip"><i class="ti ti-git-branch"></i> <span id="ver-branch">—</span></span>
    </div>
  </div>

  <div class="upd-latest-card" id="upd-latest-card" style="display:none">
    <div class="upd-latest-left">
      <div class="upd-latest-icon"><i class="ti ti-sparkles"></i></div>
      <div>
        <div class="upd-latest-title">نسخه‌ی جدید موجود است</div>
        <div class="upd-latest-ver">نسخه‌ی <span id="ver-latest-num">—</span></div>
        <div class="upd-latest-desc" id="ver-latest-desc">—</div>
      </div>
    </div>
    <button class="upd-install-btn" id="update-btn" onclick="startUpdate()">
      <i class="ti ti-download"></i> نصب بروزرسانی
    </button>
  </div>

  <div class="upd-progress-card" id="update-progress-wrap" style="display:none">
    <div class="upd-progress-head">
      <div class="upd-progress-icon"><i class="ti ti-loader-2" style="animation:spin 1s linear infinite"></i></div>
      <div style="flex:1">
        <div class="upd-progress-title">در حال نصب بروزرسانی...</div>
        <div class="upd-progress-txt" id="update-progress-txt">در حال آماده‌سازی...</div>
      </div>
      <div class="upd-progress-pct" id="update-progress-pct">0%</div>
    </div>
    <div class="upd-progress-track"><div class="upd-progress-fill" id="update-progress-bar" style="width:0%"></div></div>
  </div>

  <div class="upd-log-card">
    <div class="upd-log-head">
      <div class="upd-log-title"><i class="ti ti-terminal-2"></i> لاگ زنده‌ی نصب</div>
      <button class="btn btn-o btn-sm" onclick="loadUpdateLog()"><i class="ti ti-refresh"></i> بروزرسانی لاگ</button>
    </div>
    <div class="upd-log-box" id="update-log-box">
      <p class="upd-log-empty">لاگی موجود نیست</p>
    </div>
  </div>

  <div class="upd-history-head">
    <div class="upd-history-title"><i class="ti ti-history"></i> تاریخچه بروزرسانی غیرفعال است</div>
    <span class="badge bg-blue" id="upd-history-count">۰ مورد</span>
  </div>
  <div class="upd-timeline" id="upd-history-list">
    <div class="upd-history-empty"><i class="ti ti-history-toggle"></i><p>هنوز هیچ بروزرسانی‌ای ثبت نشده</p></div>
  </div>
</section>
<section class="pg" id="pg-support">
  <div class="sup-wrap">
    <div class="sup-head">
      <div class="sup-head-icon"><i class="ti ti-headset"></i></div>
      <div class="sup-head-text">
        <div class="sup-head-title">بخش حذف‌شده</div>
        <div class="sup-head-sub"><span class="sdot"></span> معمولاً در کمتر از چند ساعت پاسخ داده می‌شود</div>
      </div>
    </div>
    <div id="sup-blocked-banner" class="sup-blocked-banner" style="display:none">
      <i class="ti ti-lock"></i> این بخش در نسخه مستقل حذف شده است.
    </div>
    <div id="support-msgs"></div>
    <div class="sup-input-row" id="sup-input-row">
      <input class="fi" id="support-inp" placeholder="پیام خود را بنویسید..." style="flex:1" onkeydown="if(event.key==='Enter')sendSupportMsg()">
      <button class="btn btn-p" onclick="sendSupportMsg()"><i class="ti ti-send-2"></i></button>
    </div>
  </div>
</section>
<section class="pg" id="pg-settings">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-settings"></i> تنظیمات</div></div></div>
  <div class="g2">
    <div class="srv-panel">
      <div class="srv-hero">
        <div class="srv-hero-icon"><i class="ti ti-server-2"></i></div>
        <div class="srv-hero-text">
          <div class="srv-hero-domain" id="set-host">—</div>
          <div class="srv-hero-sub"><span class="dot dg pulse"></span> آنلاین · Railway</div>
        </div>
      </div>
      <div class="srv-tiles">
        <div class="srv-tile"><div class="srv-tile-icon"><i class="ti ti-route"></i></div><div class="srv-tile-text"><div class="srv-tile-label">پورت</div><div class="srv-tile-val">443 (TLS)</div></div></div>
        <div class="srv-tile"><div class="srv-tile-icon"><i class="ti ti-versions"></i></div><div class="srv-tile-text"><div class="srv-tile-label">نسخه</div><div class="srv-tile-val">v2.0.10</div></div></div>
        <div class="srv-tile"><div class="srv-tile-icon"><i class="ti ti-brand-fastapi"></i></div><div class="srv-tile-text"><div class="srv-tile-label">فریم‌ورک</div><div class="srv-tile-val">FastAPI + Uvicorn</div></div></div>
        <div class="srv-tile"><div class="srv-tile-icon"><i class="ti ti-cloud"></i></div><div class="srv-tile-text"><div class="srv-tile-label">پلتفرم</div><div class="srv-tile-val">Railway</div></div></div>
        <div class="srv-tile" style="grid-column:1/-1"><div class="srv-tile-icon"><i class="ti ti-device-floppy"></i></div><div class="srv-tile-text"><div class="srv-tile-label">ذخیره‌سازی</div><div class="srv-tile-val"><span id="storage-mode-label">JSON File</span></div></div></div>
      </div>
    </div>
    <div class="card" style="grid-column:1/-1">
      <div class="card-title"><i class="ti ti-world"></i> دامنه اصلی پنل</div>
      <div class="cl" style="margin-top:0;margin-bottom:12px"><i class="ti ti-info-circle"></i><span>دامنه‌ای که پنل روی آن در دسترس است (مثلاً panel.example.com). بعد از ذخیره، همه ساب‌ها و لینک‌های کانفیگ با این دامنه ساخته می‌شوند. اگر خالی بماند از دامنه پیش‌فرض محیط (Railway) استفاده می‌شود.</span></div>
      <div class="fg"><label>دامنه اصلی</label><input class="fi" id="panel-domain" dir="ltr" placeholder="panel.example.com" style="width:100%"></div>
      <div class="cl" style="margin-top:10px"><i class="ti ti-server"></i><span>دامنه فعلی فعال: <b dir="ltr" id="panel-domain-active">—</b> · پیش‌فرض محیط: <b dir="ltr" id="panel-domain-default">—</b></span></div>
      <div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap">
        <button class="btn btn-p btn-sm" onclick="savePanelDomain()"><i class="ti ti-device-floppy"></i> ذخیره دامنه اصلی</button>
      </div>
    </div>

    <div class="card" style="margin-top:16px">
      <div class="card-title"><i class="ti ti-shield-lock"></i> مسیر مخفی ورود</div>
      <div class="cl" style="margin-bottom:12px"><i class="ti ti-info-circle"></i><span>با تنظیم مسیر سفارشی، لاگین و داشبورد فقط از <b dir="ltr">/{path}/login</b> و <b dir="ltr">/{path}/dashboard</b> در دسترس‌اند و آدرس‌های ساده <b dir="ltr">/login</b> و <b dir="ltr">/dashboard</b> خطای ۴۰۴ می‌دهند. حداقل ۴ کاراکتر انگلیسی یا عدد.</span></div>
      <div class="fg"><label>مسیر ورود</label><input class="fi" id="panel-login-path" dir="ltr" placeholder="lkjsoijefief" style="width:100%"></div>
      <div class="cl" style="margin-top:10px"><i class="ti ti-link"></i><span>آدرس فعلی: <b dir="ltr" id="panel-login-url">/login</b></span></div>
      <div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap">
        <button class="btn btn-p btn-sm" type="button" onclick="saveLoginPath()"><i class="ti ti-device-floppy"></i> ذخیره مسیر ورود</button>
        <button class="btn btn-o btn-sm" type="button" onclick="clearLoginPath()"><i class="ti ti-refresh"></i> بازگشت به /login</button>
      </div>
    </div>

    <div class="card" style="margin-top:16px">
      <div class="card-title"><i class="ti ti-database"></i> ذخیره‌سازی دیتابیس</div>
      <div class="cl" style="margin-bottom:12px"><i class="ti ti-info-circle"></i><span>برای اینکه بعد از Redeploy داده‌ها پاک نشوند، در Railway یک <b>Volume</b> بساز و روی مسیر <b dir="ltr">/data</b> مونت کن. مسیر فعلی: <b dir="ltr" id="data-dir-path">—</b> · پایدار: <b id="data-dir-ok">—</b></span></div>
    </div>

    <div class="card" style="margin-top:16px">
      <div class="card-title"><i class="ti ti-text-recognition"></i> نام کانفیگ‌ها و خطوط آماری</div>
      <div class="cl" style="margin-bottom:12px"><i class="ti ti-info-circle"></i><span>متغیرها: <code dir="ltr">{label} {username} {status} {status_emoji} {remain_traffic} {total_traffic} {used_traffic} {remain_time} {remain_days} {protocol} {target} {domain} {cdn} {flag} {sub_name}</code></span></div>
      <div class="fg"><label>قالب نام کانفیگ (remark)</label><input class="fi" id="remark-template" dir="ltr" placeholder="{status_emoji} {label} · {target}" style="width:100%"></div>
      <div class="fg" style="margin-top:10px"><label>خطوط آماری (هر خط یک مورد)</label><textarea class="fi" id="info-templates" dir="ltr" style="width:100%;min-height:110px" placeholder="{status_emoji} وضعیت اشتراک: {status}"></textarea></div>
      <label style="display:flex;align-items:center;gap:8px;margin-top:10px;font-size:13px"><input type="checkbox" id="info-configs-enabled" checked> نمایش کانفیگ‌های آماری در ابتدای ساب</label>
      <div style="margin-top:14px"><button class="btn btn-p btn-sm" type="button" onclick="saveRemarkTemplates()"><i class="ti ti-device-floppy"></i> ذخیره قالب‌ها</button></div>
    </div>

    <div class="card" style="margin-top:16px">
      <div class="card-title"><i class="ti ti-route"></i> Railway TCP Route</div>
      <div class="cl" style="margin-bottom:12px"><i class="ti ti-info-circle"></i><span>در Railway بخش <b>TCP</b> عمومی را روشن کن. دامنه <b dir="ltr">*.proxy.rlwy.net</b> و پورت عمومی را اینجا بگذار. مهم: هدف TCP باید <b>پورت اپ</b> باشد (الان <b dir="ltr" id="tcp-app-port">—</b>) نه لزوماً 443. مسیر پیش‌فرض <b dir="ltr">path=/</b> است.</span></div>
      <div class="fg"><label>دامنه TCP</label><input class="fi" id="tcp-domain" dir="ltr" placeholder="shuttle.proxy.rlwy.net" style="width:100%"></div>
      <div class="fg" style="margin-top:10px"><label>پورت TCP عمومی</label><input class="fi" id="tcp-port" type="number" min="1" max="65535" placeholder="59740" style="width:100%"></div>
      <div class="fg" style="margin-top:10px"><label>حالت Path</label>
        <select class="fi" id="tcp-path-mode" style="width:100%">
          <option value="root" selected>ساده — / (پیشنهادی · مثل نمونه کارکننده)</option>
          <option value="panel">پنل — /ws/{path}</option>
        </select>
      </div>
      <div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap">
        <button class="btn btn-p btn-sm" type="button" onclick="saveRailwayTcp()"><i class="ti ti-device-floppy"></i> ذخیره TCP Route</button>
      </div>
    </div>

    <div class="card" style="margin-top:16px">
      <div class="card-title"><i class="ti ti-shield-lock"></i> VLESS Reality</div>
      <div class="cl" style="margin-bottom:12px"><i class="ti ti-info-circle"></i><span>فقط <b>Host/IP</b> و <b>پورت</b> را دستی وارد کن. بقیه (pbk، sid، sni، spx) با دکمه تولید تصادفی ساخته می‌شوند. لینک برای کلاینت است؛ سرور Reality (مثلاً Xray) باید همان کلیدها را داشته باشد.</span></div>
      <div class="fg"><label>Host / IP</label><input class="fi" id="reality-host" dir="ltr" placeholder="66.33.22.241" style="width:100%"></div>
      <div class="fg" style="margin-top:10px"><label>پورت</label><input class="fi" id="reality-port" type="number" min="1" max="65535" placeholder="443" style="width:100%"></div>
      <div class="fg" style="margin-top:10px"><label>Public Key (pbk)</label><input class="fi" id="reality-pbk" dir="ltr" placeholder="خودکار" style="width:100%"></div>
      <div class="fg" style="margin-top:10px"><label>Short ID (sid)</label><input class="fi" id="reality-sid" dir="ltr" placeholder="خودکار" style="width:100%"></div>
      <div class="fg" style="margin-top:10px"><label>SNI</label><input class="fi" id="reality-sni" dir="ltr" placeholder="خودکار" style="width:100%"></div>
      <div class="fg" style="margin-top:10px"><label>Fingerprint (fp)</label><input class="fi" id="reality-fp" dir="ltr" placeholder="chrome" style="width:100%"></div>
      <div class="fg" style="margin-top:10px"><label>SpiderX (spx)</label><input class="fi" id="reality-spx" dir="ltr" placeholder="/" style="width:100%"></div>
      <div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap">
        <button class="btn btn-o btn-sm" type="button" onclick="generateRealityParams()"><i class="ti ti-dice"></i> تولید تصادفی pbk/sid/sni</button>
        <button class="btn btn-p btn-sm" type="button" onclick="saveRealitySettings()"><i class="ti ti-device-floppy"></i> ذخیره Reality</button>
      </div>
    </div>

    <div class="pw-panel">
      <div class="pw-hero">
        <div class="pw-hero-icon"><i class="ti ti-key"></i></div>
        <div class="pw-hero-text">
          <div class="pw-hero-title">تغییر رمز عبور</div>
          <div class="pw-hero-sub">رمز قوی انتخاب کنید و آن را جایی امن نگه دارید</div>
        </div>
      </div>
      <div class="pw-body">
        <div class="pw-field">
          <label>رمز فعلی</label>
          <input class="pw-input" type="password" id="cp-cur" placeholder="رمز فعلی را وارد کنید">
          <button class="pw-eye" type="button" onclick="togglePwField('cp-cur',this)"><i class="ti ti-eye"></i></button>
        </div>
        <div class="pw-field" style="margin-bottom:6px">
          <label>رمز جدید</label>
          <input class="pw-input" type="password" id="cp-new" placeholder="حداقل ۴ کاراکتر" oninput="checkPwStrength(this.value)">
          <button class="pw-eye" type="button" onclick="togglePwField('cp-new',this)"><i class="ti ti-eye"></i></button>
        </div>
        <div class="pw-strength" id="pw-strength-bar">
          <div class="pw-strength-seg"></div><div class="pw-strength-seg"></div><div class="pw-strength-seg"></div><div class="pw-strength-seg"></div>
        </div>
        <div class="pw-strength-label" id="pw-strength-label"><i class="ti ti-shield"></i> قدرت رمز</div>
        <div class="pw-reqs">
          <span class="pw-req" id="req-len"><i class="ti ti-circle-dashed"></i> حداقل ۴ کاراکتر</span>
          <span class="pw-req" id="req-num"><i class="ti ti-circle-dashed"></i> شامل عدد</span>
          <span class="pw-req" id="req-case"><i class="ti ti-circle-dashed"></i> حروف بزرگ/کوچک</span>
        </div>
        <div class="pw-field" style="margin-bottom:18px">
          <label>تکرار رمز جدید</label>
          <input class="pw-input" type="password" id="cp-cf" placeholder="تکرار رمز جدید">
          <button class="pw-eye" type="button" onclick="togglePwField('cp-cf',this)"><i class="ti ti-eye"></i></button>
        </div>
        <button class="pw-submit" onclick="changePw()"><i class="ti ti-shield-check"></i> ذخیره رمز جدید</button>
      </div>
    </div>
  </div>
</section>
</main>
<script>
let isDark=localStorage.getItem('oxnet-theme')==='dark';
let updateAvailable = false;
let updateVersion = '';
let updateDescription = '';

function dismissUpdate() {
  sessionStorage.setItem('oxnet-update-dismissed', 'true');
  closeModal('modal-update');
}

function startUpdateFromModal() {
  closeModal('modal-update');
  startUpdate(); // تابع موجود
}

function updateGreeting(){
  const el=document.getElementById('ov-greeting');
  if(!el) return;
  const h=new Date().getHours();
  let g='سلام';
  if(h<12) g='صبح بخیر';
  else if(h<18) g='ظهر بخیر';
  else g='عصر بخیر';
  el.textContent=g+'؛ خوش آمدید';
}

function applyTheme(dark){
  document.documentElement.setAttribute('data-theme',dark?'dark':'light');
  const icon=dark?'ti-sun':'ti-moon',label=dark?'تم روشن':'تم تاریک';
  document.getElementById('theme-icon').className='ti '+icon;
  document.getElementById('theme-label').textContent=label;
  const mobI=document.getElementById('theme-mob-icon');if(mobI)mobI.className='ti '+icon;
}

function toggleTheme(){isDark=!isDark;localStorage.setItem('oxnet-theme',isDark?'dark':'light');applyTheme(isDark)}
applyTheme(isDark);
function toast(msg,type=''){
  const t=document.getElementById('toast');
  t.textContent=msg;t.className='toast show'+(type?' '+type:'');
  setTimeout(()=>t.classList.remove('show'),2400);
}
function fmtB(b){if(!b||b===0)return '0 B';if(b<1024)return b+' B';if(b<1024**2)return (b/1024).toFixed(1)+' KB';if(b<1024**3)return (b/1024**2).toFixed(2)+' MB';return (b/1024**3).toFixed(2)+' GB'}
function toFa(n){return String(n).replace(/\d/g,d=>'۰۱۲۳۴۵۶۷۸۹'[d])}
function esc(s){return String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function daysLeft(exp){if(!exp)return null;return Math.ceil((new Date(exp)-Date.now())/(864e5))}
function expChip(exp,expired){
  if(expired)return '<span class="exp-chip ec-exp"><i class="ti ti-calendar-x"></i> منقضی</span>';
  if(!exp)return '<span class="exp-chip ec-inf"><i class="ti ti-infinity"></i> نامحدود</span>';
  const d=daysLeft(exp);
  if(d<=0)return '<span class="exp-chip ec-exp"><i class="ti ti-calendar-x"></i> منقضی</span>';
  if(d<=3)return `<span class="exp-chip ec-warn"><i class="ti ti-alert-triangle"></i> ${toFa(d)} روز مانده</span>`;
  return `<span class="exp-chip ec-ok"><i class="ti ti-calendar-check"></i> ${toFa(d)} روز مانده</span>`;
}

const PROTO_MAP={
  'vless-ws':['VLESS · WS','pc-ws'],
  'xhttp-packet-up':['VLESS · XHTTP packet-up','pc-xhttp'],
  'xhttp-stream-up':['VLESS · XHTTP stream-up','pc-xhttp'],
  'xhttp-stream-one':['XHTTP Stream','pc-xh'],
  'trojan-ws':['Trojan · WS','pc-trojan'],
  'trojan-xhttp-packet-up':['Trojan · XHTTP packet-up','pc-trojan'],
  'trojan-xhttp-stream-up':['Trojan · XHTTP stream-up','pc-trojan'],
  'shadowsocks-tls':['Shadowsocks · TLS','pc-ss'],
  'mtproto':['Telegram Proxy · MTProto','pc-trojan'],
  'multi':['Multi Protocol','pc-xhttp']
};

function protoBadge(p){
  const v=PROTO_MAP[p]||['ناشناخته','pc-ws'];
  return `<span class="proto-chip ${v[1]}">${v[0]}</span>`;
}
async function checkAuth(){try{const r=await fetch('/api/me');const d=await r.json();if(!d.authenticated)location.href=(window.OXNET_LOGIN||(function(){try{return localStorage.getItem('oxnet-login-url')||'/login'}catch(e){return '/login'}})());}catch(e){location.href=(window.OXNET_LOGIN||(function(){try{return localStorage.getItem('oxnet-login-url')||'/login'}catch(e){return '/login'}})())}}
async function logout(){try{await fetch('/api/logout',{method:'POST'})}catch(e){}var u='/login';try{u=localStorage.getItem('oxnet-login-url')||'/login'}catch(e){}location.href=u}
document.getElementById('logout-btn').addEventListener('click',logout);
async function authF(url,opts={}){
  opts = opts || {};
  if(!opts.credentials) opts.credentials='same-origin';
  try{
    const r=await fetch(url,opts);
    if(r.status===401){location.href=(window.OXNET_LOGIN||(function(){try{return localStorage.getItem('oxnet-login-url')||'/login'}catch(e){return '/login'}})());throw new Error('unauthorized')}
    return r;
  }catch(e){
    console.error('fetch failed', url, e);
    throw new Error('ارتباط با سرور برقرار نشد؛ اگر عملیات در حال اجراست وضعیت را رفرش کن');
  }
}
function setQuota(val,unit,el){
  document.getElementById('nl-val').value = val===0?'':val;
  document.getElementById('nl-unit').value = unit;
  document.querySelectorAll('#quota-chips .qc-pill').forEach(c=>c.classList.remove('active'));
  el.classList.add('active');
}
function setExpiry(days,el){
  document.getElementById('nl-exp').value = days===0?'':days;
  document.querySelectorAll('#exp-chips .qc-pill').forEach(c=>c.classList.remove('active'));
  el.classList.add('active');
}
function selectProto(val,el){
  document.getElementById('nl-proto').value = val;
  document.querySelectorAll('.proto-card').forEach(c=>c.classList.remove('active'));
  el.classList.add('active');
}
const sb=document.getElementById('sb'),overlay=document.getElementById('overlay');
function openSb(){sb.classList.add('open');overlay.classList.add('show')}
function closeSb(){sb.classList.remove('open');overlay.classList.remove('show')}
document.getElementById('open-sb').addEventListener('click',openSb);
document.getElementById('close-sb').addEventListener('click',closeSb);
overlay.addEventListener('click',closeSb);
function navTo(name){
  document.querySelectorAll('.nav-it').forEach(n=>n.classList.toggle('on',n.dataset.pg===name));
  document.querySelectorAll('.pg').forEach(p=>p.classList.toggle('on',p.id==='pg-'+name));
  const loaders={links:loadLinks,connections:loadConns,errors:loadErrs,subscriptions:loadSubsPage,subgroups:loadSubs,logs:loadActivity,settings:()=>{loadDbStatus();loadPanelDomain();},customers:loadCustomers,cloudflare:()=>{loadCloudflareDomains();loadExtraDomains();},security:loadSecuritySettings};  if(loaders[name])loaders[name]();
  closeSb();window.scrollTo({top:0,behavior:'smooth'});
}
document.querySelectorAll('.nav-it').forEach(el=>el.addEventListener('click',()=>navTo(el.dataset.pg)));
function openModal(id){const el=document.getElementById(id);if(!el){console.error('modal missing',id);toast('پنجره پیدا نشد: '+id,'err');return}el.classList.add('open')}
function closeModal(id){const el=document.getElementById(id);if(el)el.classList.remove('open')}
function resetCreateModal(){try{cmSelectBase('vless',document.querySelector('#dd-base .cm-opt[data-base="vless"]'));cmSelectTransport('ws',document.querySelector('#dd-transport .cm-opt'));}catch(e){console.warn(e)}const p=document.getElementById('nl-proto');if(p)p.value='vless-ws'}
function dashCreateConfig(){try{resetCreateModal();openModal('modal-create-link')}catch(e){console.error(e);toast('خطا در باز کردن ساخت کانفیگ','err')}}
function dashGoTraffic(){try{navTo('traffic')}catch(e){console.error(e);toast('خطا در نمایش ترافیک','err')}}
function dashRefresh(){try{refreshAll()}catch(e){console.error(e);toast('خطا در رفرش','err')}}

let prevTraf=0,ch1,ch2,ch3;
async function fetchStats(){
  try{
    const r=await authF('/stats'),d=await r.json();
    document.getElementById('m-conns').textContent=d.active_connections;
    document.getElementById('conns-nb').textContent=d.active_connections;
    document.getElementById('m-traffic').textContent=d.total_traffic_mb.toFixed(1)+' MB';
    document.getElementById('m-alinks').textContent=d.active_links??'—';
    document.getElementById('m-lsub').textContent='از '+d.links_count+' کانفیگ';
    document.getElementById('m-subs').textContent=d.subs_count??'—';
    const errsBadge=document.getElementById('errs-badge'); if(errsBadge) errsBadge.textContent=d.total_errors+' خطا';
    document.getElementById('uptime-inline').textContent=d.uptime;
    document.getElementById('uptime-badge').textContent='Railway · '+d.uptime;
    const lastUpd=document.getElementById('last-upd'); if(lastUpd) lastUpd.textContent='آخرین بروزرسانی: '+new Date().toLocaleTimeString('fa-IR');
    const connsLive=document.getElementById('conns-live'); if(connsLive) connsLive.innerHTML='<span class="dot dg pulse"></span> '+d.active_connections+' اتصال';
    const tTraffic=document.getElementById('t-traffic'); if(tTraffic) tTraffic.innerHTML=d.total_traffic_mb.toFixed(1)+'<span class="m-unit">MB</span>';
    const delta=d.total_traffic_mb-prevTraf,pct=Math.min(100,Math.round((delta/50)*100));
    document.getElementById('bw-pct').textContent=pct+'%';
    document.getElementById('bw-bar').style.width=pct+'%';
    prevTraf=d.total_traffic_mb;
    if(d.hourly){
      const labels=Object.keys(d.hourly).sort(),vals=labels.map(k=>+(d.hourly[k]/1024**2).toFixed(2));
      [ch1,ch3].forEach(c=>{if(!c)return;c.data.labels=labels;c.data.datasets[0].data=vals;c.update()}); try{seedSparks(d.hourly);}catch(e){}
      const pc=d.protocol_counts||{};
      if(ch2){ch2.data.labels=['VLESS WS','Trojan WS','XHTTP','Shadowsocks TLS','MTProto'];ch2.data.datasets[0].data=[pc.vless_ws||0,pc.trojan_ws||0,pc.xhttp||0,pc.shadowsocks_tls||0,pc.mtproto||0];
    try{const s=(ch2.data.datasets[0].data||[]).reduce((a,b)=>a+Number(b||0),0);const el=document.getElementById("donut-total");if(el)el.textContent=toFa?toFa(s):s;}catch(e){}ch2.update();}
      renderFallbackCharts(labels, vals, pc);
      if(vals.length){const avg=vals.reduce((a,b)=>a+b,0)/vals.length,peak=Math.max(...vals);const tAvg=document.getElementById('t-avg'),tPeak=document.getElementById('t-peak');if(tAvg)tAvg.innerHTML=avg.toFixed(2)+'<span class="m-unit">MB</span>';if(tPeak)tPeak.innerHTML=peak.toFixed(2)+'<span class="m-unit">MB</span>';}
    }
    renderErrs(d.recent_errors||[]);
  }catch(e){console.error(e)}
}
function renderErrs(errs){
  const el=document.getElementById('errs-full');if(!el)return;
  if(!errs.length){el.innerHTML='<div style="color:var(--green-t);padding:10px;font-size:12px;display:flex;align-items:center;gap:5px"><i class="ti ti-circle-check"></i> هیچ خطایی نیست</div>';return}
  el.innerHTML=errs.slice().reverse().map(e=>`<div class="erow"><div class="etime"><i class="ti ti-clock"></i>${new Date(e.time).toLocaleString('fa-IR')}</div><div class="emsg">${esc(e.error)}${e.url?' — '+esc(e.url):''}</div></div>`).join('');
}
async function loadActivity(){
  try{
    const r=await authF('/api/activity'),d=await r.json();
    const logs=(d.logs||[]).slice().reverse();
    const el=document.getElementById('logs-list'),em=document.getElementById('logs-empty');
    if(!logs.length){el.innerHTML='';em.style.display='block';return}
    em.style.display='none';
    const icMap={ok:'ti-circle-check',err:'ti-circle-x',warn:'ti-alert-triangle',info:'ti-info-circle'};
    const kindFa={link:'کانفیگ',sub:'گروه',auth:'ورود',connection:'اتصال',system:'سیستم'};
    el.innerHTML=logs.map(l=>`
      <div class="log-item">
        <div class="log-ic ${l.level}"><i class="ti ${icMap[l.level]||'ti-info-circle'}"></i></div>
        <div class="log-body">
          <div class="log-msg">${esc(l.message)}</div>
          <div class="log-time"><i class="ti ti-clock"></i> ${new Date(l.time).toLocaleString('fa-IR')} <span class="log-kind">${kindFa[l.kind]||l.kind}</span></div>
        </div>
      </div>
    `).join('');
  }catch(e){console.error(e)}
}
let allSubsList=[],allLinksList=[];
async function loadLinks(){
  try{
    const [lres,sres]=await Promise.allSettled([authF('/api/links'),authF('/api/subs')]);
    if(lres.status!=='fulfilled' || !lres.value.ok) throw new Error('links failed');
    const lr=lres.value, sr=(sres.status==='fulfilled' && sres.value.ok) ? sres.value : null;
    const lj=await lr.json().catch(()=>({links:[]}));
    const sj=sr ? await sr.json().catch(()=>({subs:[]})) : {subs:[]};
    let rawLinks=Array.isArray(lj.links)?lj.links:[];
    const subs=Array.isArray(sj.subs)?sj.subs:[];
    rawLinks=(rawLinks||[]).filter(l=>l&&l.uuid&&!l.archived).map(l=>({label:'بدون نام',used_bytes:0,limit_bytes:0,active:true,expired:false,created_at:new Date().toISOString(),vless_link:'',sub_url:'',protocol:'vless-ws',...l}));
    const multiSubs=subs.filter(s=>String(s.desc||'').includes('Multi Protocol') || rawLinks.some(l=>l.is_multi_child && (l.multi_group_id===s.sub_id || (s.link_ids||[]).includes(l.uuid))));
    // فقط بچه‌های واقعی مولتی را داخل کارت گروهی مخفی/گروه‌بندی کن؛
    // کانفیگ یا پروکسی معمولی که بعداً داخل همان گروه اضافه شده باید جدا نمایش داده شود.
    const childIds=new Set(rawLinks.filter(l=>l.is_multi_child).map(l=>l.uuid));
    const groupCards=multiSubs.map(s=>{
      const kids=rawLinks.filter(l=>l.is_multi_child && (l.multi_group_id===s.sub_id || (s.link_ids||[]).includes(l.uuid)));
      return {uuid:s.sub_id,label:s.name,protocol:'multi',is_multi_group:true,child_count:kids.length,children:kids,active:kids.some(k=>k.active&&!k.expired),expired:false,used_bytes:kids.reduce((a,k)=>a+(k.used_bytes||0),0),limit_bytes:kids.reduce((a,k)=>a+(k.limit_bytes||0),0),created_at:s.created_at,sub_url:s.sub_url,vless_link:s.sub_url,sub_id:s.sub_id};
    });
    const links=[...groupCards,...rawLinks.filter(l=>!childIds.has(l.uuid))];
    allSubsList=subs;allLinksList=links;window.__rawLinksList=rawLinks;
    document.getElementById('info-inbounds').textContent = toFa(links.length);
    document.getElementById('info-clients').textContent = toFa(links.filter(l=>l.active).length);
    document.getElementById('info-alltime').textContent = fmtB(links.reduce((s,l)=>s+l.used_bytes,0));
    const nlSub=document.getElementById('nl-sub');
    nlSub.innerHTML='<option value="">— بدون گروه —</option>'+subs.map(s=>`<option value="${esc(s.sub_id)}">${esc(s.name)}</option>`).join('');
    document.getElementById('links-nb').textContent=links.length;
    document.getElementById('links-pg-cnt').textContent=toFa(links.length)+' کانفیگ';
    document.getElementById('lsummary-badge').textContent=toFa(links.length);
    const grid=document.getElementById('links-grid'),empty=document.getElementById('links-empty');
    if(!links.length){grid.innerHTML='';empty.style.display='block';document.getElementById('lsummary').innerHTML='<div class="empty"><i class="ti ti-link-off"></i><p>کانفیگی وجود ندارد</p></div>';return}
    empty.style.display='none';
    const subMap=Object.fromEntries(subs.map(s=>[s.sub_id,s.name]));
    grid.innerHTML=links.map(l=>{
  if(l.is_multi_group){return `<div class="multi-group-card"><div class="multi-group-head"><div><div class="multi-group-title"><i class="ti ti-layers-intersect"></i>${esc(l.label)}</div><div class="multi-protos">${(l.children||[]).map(k=>`<span>${esc((PROTO_MAP[k.protocol]||[k.protocol])[0])}</span>`).join('')||'<span>Multi</span>'}</div></div><div style="display:flex;gap:6px;flex-wrap:wrap;justify-content:flex-end"><span class="badge bg-blue">${toFa(l.child_count||0)} پروتکل</span><button class="btn btn-sm btn-p" onclick="navigator.clipboard.writeText('${esc(l.sub_url)}').then(()=>toast('ساب مولتی کپی شد','ok'))"><i class="ti ti-copy"></i> ساب</button><button class="btn btn-sm btn-g" onclick="openSubLinks('${esc(l.sub_id)}','${esc(l.label)}')"><i class="ti ti-link-plus"></i> کانفیگ‌ها</button><button class="btn btn-sm btn-amber btn-icon" onclick="editSubQuick('${esc(l.sub_id)}','${esc(l.label)}')" title="ویرایش"><i class="ti ti-edit"></i></button><button class="btn btn-sm btn-g btn-icon" onclick="showQR('${esc(l.sub_url)}')"><i class="ti ti-qrcode"></i></button></div></div><div class="utxt"><span>مصرف کل: ${fmtB(l.used_bytes||0)}</span><span>${esc(l.sub_url||'')}</span></div></div>`}
  const lim=l.limit_bytes===0?'∞':fmtB(l.limit_bytes);
  const pct=l.limit_bytes===0?0:Math.min(100,l.used_bytes/l.limit_bytes*100);
  const bc=pct>90?'var(--red)':pct>70?'var(--amber)':'var(--accent)';
  const allowed=l.active&&!l.expired;
  const cardCls=!l.active?'is-off':(l.expired?'is-exp':'');
  const isMt = l.protocol === 'mtproto';
  const adBtn = isMt
    ? `<button class="btn btn-sm btn-pur btn-icon" onclick="openAdTagModal('${l.uuid}','${esc(l.label)}','${esc(l.ad_tag||'')}')" title="تنظیم تبلیغ کانال"><i class="ti ti-speakerphone"></i></button>`
    : '';
  const idChip = isMt
    ? `<span class="cfg-uuid-mini" onclick="navigator.clipboard.writeText('${esc(l.mtproto_secret||'')}').then(()=>toast('سکرت کپی شد ','ok'))" title="سکرت کامل: ${esc(l.mtproto_secret||'')}"><i class="ti ti-key"></i> ${esc((l.mtproto_secret||'').slice(0,10))}…</span>`
    : `<span class="cfg-uuid-mini" onclick="navigator.clipboard.writeText('${l.uuid}').then(()=>toast('UUID کپی شد','ok'))" title="${l.uuid}"><i class="ti ti-fingerprint"></i> ${l.uuid.slice(0,10)}…</span>`;
  return `<div class="cfg-card ${cardCls}">
    <div class="cfg-row">
      <span class="cfg-status-dot ${allowed?'pulse':''}"></span>
      <div class="cfg-identity">
        <div class="cfg-label">${esc(l.label)}</div>
        <div class="cfg-sub-meta">
          ${idChip}
          <span>${new Date(l.created_at).toLocaleDateString('fa-IR')}</span>
        </div>
      </div>
      <div class="cfg-divider-v"></div>
      <div class="cfg-usage-col">
        <div class="ubar"><div class="ubar-f" style="width:${pct}%;background:${bc}"></div></div>
        <div class="utxt"><span>${fmtB(l.used_bytes)}</span><span>از ${lim}</span></div>
      </div>
      <div class="cfg-divider-v"></div>
      <div class="cfg-exp-col">${expChip(l.expires_at,l.expired)}</div>
      <div class="cfg-divider-v"></div>
      <div class="cfg-badges-col">
        ${protoBadge(l.protocol)}
        ${l.sub_id&&allSubsList.find(s=>s.sub_id===l.sub_id)?`<span class="cfg-sub-tag"><i class="ti ti-folder"></i> ${esc(allSubsList.find(s=>s.sub_id===l.sub_id).name)}</span>`:''}
      </div>
      <div class="cfg-divider-v"></div>
      <div class="cfg-actions">
        <button class="tog${allowed?' on':''}" onclick="toggleActive('${l.uuid}',${!l.active})" title="فعال/غیرفعال"></button>
        ${adBtn}
        <button class="btn btn-sm btn-g btn-icon" onclick="navigator.clipboard.writeText('${esc(l.vless_link)}').then(()=>toast('لینک کپی شد','ok'))" title="کپی لینک"><i class="ti ti-copy"></i></button>
        ${isMt
          ? `<button class="btn btn-sm btn-g btn-icon" onclick="openMtInfoModal('${esc(l.label)}','${esc(l.mtproto_secret||'')}','${esc(l.vless_link)}',${!!l.mtproto_public_host})" title="اطلاعات پروکسی"><i class="ti ti-info-circle"></i></button>`
          : `<button class="btn btn-sm btn-g btn-icon" onclick="navigator.clipboard.writeText('${esc(l.sub_url)}').then(()=>toast('Sub کپی شد','ok'))" title="Sub URL"><i class="ti ti-rss"></i></button>
        <button class="btn btn-sm btn-g btn-icon" onclick="showQR('${esc(l.vless_link)}')" title="QR"><i class="ti ti-qrcode"></i></button>`
        }
        <button class="btn btn-sm btn-amber btn-icon" onclick="openEditLink('${l.uuid}')" title="ویرایش"><i class="ti ti-edit"></i></button>
        <button class="btn btn-sm btn-g btn-icon" onclick="resetUsage('${l.uuid}')" title="ریست مصرف"><i class="ti ti-rotate"></i></button>
        <button class="btn btn-sm btn-d btn-icon" onclick="deleteLink('${l.uuid}')" title="حذف"><i class="ti ti-trash"></i></button>
      </div>
    </div>
  </div>`;
}).join('');
    document.getElementById('lsummary').innerHTML=links.slice(0,6).map(l=>`<div class="sr"><span class="sr-k" style="gap:5px"><i class="ti ${l.expired?'ti-calendar-x':l.active?'ti-circle-check':'ti-circle-x'}" style="color:${l.expired?'var(--amber)':l.active?'var(--green)':'var(--red)'}"></i>${esc(l.label)}</span><span class="sr-v" style="font-size:10px">${fmtB(l.used_bytes)} / ${l.limit_bytes===0?'∞':fmtB(l.limit_bytes)}</span></div>`).join('');
  }catch(e){console.error(e);const grid=document.getElementById('links-grid');if(grid&&!grid.innerHTML){grid.innerHTML='<div class="empty"><i class="ti ti-alert-circle"></i><p>خطا در نمایش کانفیگ‌ها برطرف شد؛ اگر هنوز می‌بینی صفحه را کامل Reload کن</p></div>'}}
}

let protoBase = 'vless', protoTransport = 'ws';

function qcTab(name, el){
  document.querySelectorAll('.qc-tab').forEach(t=>t.classList.remove('active'));
  el.classList.add('active');
  document.querySelectorAll('.qc-pane').forEach(p=>p.classList.remove('active'));
  document.getElementById('qc-pane-'+name).classList.add('active');
}

let cmBase = 'vless', cmTransport = 'ws';

function cmToggleDD(id){
  const el = document.getElementById(id);
  const isOpen = el.classList.contains('open');
  document.querySelectorAll('.cm-dd').forEach(d => d.classList.remove('open'));
  if(!isOpen) el.classList.add('open');
}

const BASE_INFO = {
  vless:    { icon:'ti-bolt',           title:'VLESS',          desc:'سبک، سریع و پرکاربردترین گزینه' },
  trojan:   { icon:'ti-shield-lock',    title:'Trojan',         desc:'شبیه‌سازی ترافیک HTTPS معمولی' },
  telproxy: { icon:'ti-brand-telegram', title:'Telegram Proxy', desc:'پروکسی MTProto مستقیم روی یک پورت TCP اختصاصی' },
  multi:    { icon:'ti-layers-intersect', title:'Multi Protocol', desc:'یک ساب شامل همه پروتکل‌ها + TCP/Reality' },
  shadowsocks: { icon:'ti-lock-bolt', title:'Shadowsocks TLS', desc:'شادوساکس روی TLS/WebSocket با مسیر اختصاصی' },
  'vless-tcp': { icon:'ti-route', title:'VLESS TCP Proxy', desc:'دامنه و پورت TCP Proxy ریلوی · بدون TLS' },
  'vless-reality': { icon:'ti-shield-lock', title:'VLESS Reality', desc:'Reality با pbk / sid / sni' }
};
const TRANSPORT_INFO = {
  'ws':               { icon:'ti-link',    title:'WebSocket',            desc:'پایدار و سازگار با همه شرایط شبکه' },
  'xhttp-packet-up':  { icon:'ti-package', title:'XHTTP · packet-up',    desc:'سازگاری بالا با CDN و پروکسی‌ها' },
  'xhttp-stream-up':  { icon:'ti-rocket',  title:'XHTTP · stream-up',    desc:'تاخیر پایین‌تر برای اتصال‌های پرسرعت' }
};

function cmSelectBase(val, el){
  cmBase = val;
  const show=(node,display)=>{if(node)node.style.display=display};
  document.querySelectorAll('#dd-base .cm-opt').forEach(o => o.classList.remove('sel'));
  if(el)el.classList.add('sel');
  const info = BASE_INFO[val];
  document.getElementById('dd-base-icon').innerHTML = `<i class="ti ${info.icon}"></i>`;
  document.getElementById('dd-base-current').textContent = info.title;
  document.getElementById('dd-base-current-desc').textContent = info.desc;
  cmToggleDD('dd-base');

  const transportSection = document.getElementById('transport-section');
  const normalNote = document.getElementById('transport-note');
  const mtNote = document.getElementById('mtproto-note');
  const tcpNote = document.getElementById('tcp-note');
  const realityNote = document.getElementById('reality-note');
  const portField = document.getElementById('mtproto-port-field');
  const tcpField = document.getElementById('tcp-proxy-field');
  const realityField = document.getElementById('reality-field');
  const hideExtra = ()=>{show(mtNote,'none');show(tcpNote,'none');show(realityNote,'none');show(portField,'none');show(tcpField,'none');show(realityField,'none');};
  if (val === 'multi') {
    show(transportSection,'none');
    show(normalNote,'flex');
    hideExtra();
    document.getElementById('cm-head-title').textContent = 'ساخت ساب مولتی پروتکل';
    document.getElementById('cm-head-sub').textContent = 'همه پروتکل‌ها + TCP Proxy و Reality در یک ساب';
    document.getElementById('cm-submit-text').textContent = 'ساخت ساب مولتی';
    document.getElementById('cm-head-icon').innerHTML = '<i class="ti ti-layers-intersect"></i>';
    document.getElementById('nl-proto').value = 'multi';
    cmBase='multi';
    return;
  }
  if (val === 'shadowsocks') {
    show(transportSection,'none');
    show(normalNote,'flex');
    hideExtra();
    document.getElementById('cm-head-title').textContent = 'ساخت Shadowsocks TLS';
    document.getElementById('cm-head-sub').textContent = 'شادوساکس با TLS و مسیر اختصاصی';
    document.getElementById('cm-submit-text').textContent = 'ساخت Shadowsocks';
    document.getElementById('cm-head-icon').innerHTML = '<i class="ti ti-lock-bolt"></i>';
    document.getElementById('nl-proto').value = 'shadowsocks-tls';
    return;
  }
  if (val === 'vless-tcp') {
    show(transportSection,'none');
    show(normalNote,'none');
    hideExtra();
    show(tcpNote,'flex');
    show(tcpField,'block');
    document.getElementById('cm-head-title').textContent = 'ساخت VLESS TCP Proxy';
    document.getElementById('cm-head-sub').textContent = 'لینک روی دامنه و پورت TCP Proxy ریلوی · بدون TLS';
    document.getElementById('cm-submit-text').textContent = 'ساخت TCP Proxy';
    document.getElementById('cm-head-icon').innerHTML = '<i class="ti ti-route"></i>';
    document.getElementById('nl-proto').value = 'vless-tcp';
    return;
  }
  if (val === 'vless-reality') {
    show(transportSection,'none');
    show(normalNote,'none');
    hideExtra();
    show(realityNote,'flex');
    show(realityField,'block');
    document.getElementById('cm-head-title').textContent = 'ساخت VLESS Reality';
    document.getElementById('cm-head-sub').textContent = 'لینک Reality با pbk / sid / sni';
    document.getElementById('cm-submit-text').textContent = 'ساخت Reality';
    document.getElementById('cm-head-icon').innerHTML = '<i class="ti ti-shield-lock"></i>';
    document.getElementById('nl-proto').value = 'vless-reality';
    return;
  }
  if (val === 'telproxy') {
    show(transportSection,'none');
    show(normalNote,'none');
    hideExtra();
    show(mtNote,'flex');
    show(portField,'block');
    document.getElementById('cm-head-title').textContent = 'ساخت مسیر تلگرام';
    document.getElementById('cm-head-sub').textContent = 'ساخت مسیر MTProto با پورت TCP اختصاصی';
    document.getElementById('cm-submit-text').textContent = 'ساخت مسیر';
    document.getElementById('cm-head-icon').innerHTML = '<i class="ti ti-brand-telegram"></i>';
  } else {
    show(transportSection,'');
    show(normalNote,'flex');
    hideExtra();
    document.getElementById('cm-head-title').textContent = 'ساخت کانفیگ جدید';
    document.getElementById('cm-head-sub').textContent = 'تنظیمات کامل پروتکل، ترابرد و محدودیت‌ها در یک صفحه';
    document.getElementById('cm-submit-text').textContent = 'ساخت کانفیگ';
    document.getElementById('cm-head-icon').innerHTML = '<i class="ti ti-plus"></i>';
  }
  cmApplyProto();
}

function cmSelectTransport(val, el){
  cmTransport = val;
  document.querySelectorAll('#dd-transport .cm-opt').forEach(o => o.classList.remove('sel'));
  if(el)el.classList.add('sel');
  const info = TRANSPORT_INFO[val];
  document.getElementById('dd-transport-icon').innerHTML = `<i class="ti ${info.icon}"></i>`;
  document.getElementById('dd-transport-current').textContent = info.title;
  document.getElementById('dd-transport-current-desc').textContent = info.desc;
  cmToggleDD('transport-section');
  cmApplyProto();
}
function cmApplyProto(){
  if (cmBase === 'telproxy') {
    document.getElementById('nl-proto').value = 'mtproto';
    return;
  }
  let val;
  if (cmTransport === 'ws') val = (cmBase === 'trojan' ? 'trojan-ws' : 'vless-ws');
  else val = (cmBase === 'trojan' ? `trojan-${cmTransport}` : cmTransport);
  document.getElementById('nl-proto').value = val;
}

/* ── سهمیه ترافیک و انقضا: هم با پیل، هم با تایپ مستقیم قابل تنظیم‌اند ── */
function cmQuota(val, unit, el){
  document.getElementById('nl-val').value = val === 0 ? '' : val;
  document.getElementById('nl-unit').value = unit;
  el.parentElement.querySelectorAll('.cm-pill').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
}
function cmExpiry(days, el){
  document.getElementById('nl-exp').value = days === 0 ? '' : days;
  el.parentElement.querySelectorAll('.cm-pill').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
}

function cmSetSni(domain, el){
  document.getElementById('nl-mtproto-domain').value = domain;
  el.parentElement.querySelectorAll('.cm-pill').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
}
function cmClearSniPills(){
  const wrap = document.getElementById('nl-mtproto-domain').closest('.cm-section').querySelector('.cm-pills');
  wrap?.querySelectorAll('.cm-pill').forEach(c => c.classList.remove('active'));
}

/* وقتی کاربر خودش عدد رو دستی تایپ می‌کنه، انتخاب پیل‌ها برداشته بشه */
document.getElementById('nl-val')?.addEventListener('input', () => {
  document.querySelectorAll('#nl-val').forEach(()=>{});
  const wrap = document.getElementById('nl-val').closest('.cm-field').querySelector('.cm-pills');
  wrap?.querySelectorAll('.cm-pill').forEach(c => c.classList.remove('active'));
});
document.getElementById('nl-exp')?.addEventListener('input', () => {
  const wrap = document.getElementById('nl-exp').closest('.cm-field').querySelector('.cm-pills');
  wrap?.querySelectorAll('.cm-pill').forEach(c => c.classList.remove('active'));
});

async function createLink(){
  const label=document.getElementById('nl-label').value.trim()||'کانفیگ جدید';
  const val=document.getElementById('nl-val').value;
  const unit=document.getElementById('nl-unit').value;
  const exp=document.getElementById('nl-exp').value;
  const note=document.getElementById('nl-note').value.trim();
  const custom_path=document.getElementById('nl-path').value.trim();
  const sub_id=document.getElementById('nl-sub').value||null;
  let protocol=document.getElementById('nl-proto').value||'vless-ws';
  if(cmBase==='multi') protocol='multi';
  if(cmBase==='telproxy') protocol='mtproto';
  if(cmBase==='shadowsocks') protocol='shadowsocks-tls';
  if(cmBase==='vless-tcp') protocol='vless-tcp';
  if(cmBase==='vless-reality') protocol='vless-reality';
  const isMt = protocol === 'mtproto';
  const mtproto_port = isMt ? (document.getElementById('nl-mtproto-port').value || null) : null;
  const mtproto_domain = isMt ? (document.getElementById('nl-mtproto-domain').value.trim() || null) : null;
  const body={label,custom_path,limit_value:val||0,limit_unit:unit,expires_days:exp||0,note,sub_id,protocol,mtproto_port,mtproto_domain};
  if(protocol==='vless-tcp'){
    body.tcp_domain=(document.getElementById('nl-tcp-domain').value||'').trim()||null;
    body.tcp_port=document.getElementById('nl-tcp-port').value||null;
    body.tcp_path_mode=document.getElementById('nl-tcp-path-mode').value||'panel';
  }
  if(protocol==='vless-reality'){
    body.reality_host=(document.getElementById('nl-reality-host').value||'').trim()||null;
    body.reality_port=document.getElementById('nl-reality-port').value||null;
    body.reality_pbk=(document.getElementById('nl-reality-pbk').value||'').trim()||null;
    body.reality_sid=(document.getElementById('nl-reality-sid').value||'').trim()||null;
    body.reality_sni=(document.getElementById('nl-reality-sni').value||'').trim()||null;
    body.reality_fp=(document.getElementById('nl-reality-fp').value||'').trim()||'chrome';
    body.reality_spx=(document.getElementById('nl-reality-spx').value||'').trim()||'/';
  }
  try{
    const r=await authF('/api/links',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
    if(!r.ok){
      const d=await r.json().catch(()=>({}));
      throw new Error(d.detail||'failed');
    }
    const d=await r.json().catch(()=>({}));
    const copyTarget = d.sub_url || d.vless_link;
    if(copyTarget && navigator.clipboard) navigator.clipboard.writeText(copyTarget).catch(()=>{});
    ['nl-label','nl-path','nl-val','nl-exp','nl-note','nl-mtproto-port','nl-mtproto-domain','nl-tcp-domain','nl-tcp-port','nl-reality-host','nl-reality-port','nl-reality-pbk','nl-reality-sid','nl-reality-sni'].forEach(id=>{const el=document.getElementById(id);if(el)el.value='';});
    const msg = protocol==='multi' ? 'ساب مولتی ساخته شد و لینک کپی شد'
      : isMt ? 'پروکسی ساخته شد و لینک کپی شد'
      : protocol==='shadowsocks-tls' ? 'Shadowsocks TLS ساخته شد و لینک کپی شد'
      : protocol==='vless-tcp' ? 'VLESS TCP Proxy ساخته شد و لینک کپی شد'
      : protocol==='vless-reality' ? 'VLESS Reality ساخته شد و لینک کپی شد'
      : 'کانفیگ ساخته شد';
    toast(msg,'ok');
    closeModal('modal-create-link');
    loadLinks();
    if(protocol==='multi'){loadSubs();loadSubsPage();}
  }catch(e){toast(' '+e.message,'err')}
}


function openEditLink(uuid){
  const l=(window.__rawLinksList||allLinksList||[]).find(x=>x.uuid===uuid);
  if(!l){toast('کانفیگ پیدا نشد؛ رفرش کن','err');return}
  const set=(id,val)=>{const el=document.getElementById(id); if(el) el.value=val ?? ''};
  set('el-uuid',uuid); set('el-label',l.label||''); set('el-note',l.note||'');
  if(l.limit_bytes===0){set('el-val','');set('el-unit','GB')}
  else{set('el-val',(l.limit_bytes/1024/1024).toFixed(0));set('el-unit','MB')}
  set('el-exp','');
  openModal('modal-edit-link');
}
async function saveEditLink(){
  const uuid=document.getElementById('el-uuid').value;
  const label=document.getElementById('el-label').value.trim();
  const note=document.getElementById('el-note').value.trim();
  const val=document.getElementById('el-val').value;
  const unit=document.getElementById('el-unit').value;
  const exp=document.getElementById('el-exp').value;
  const body={label,note,limit_value:val||0,limit_unit:unit};
  if(exp&&Number(exp)>0)body.expires_days=Number(exp);
  try{
    const r=await authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
    if(!r.ok)throw new Error();
    closeModal('modal-edit-link');
    toast('کانفیگ ویرایش شد ','ok');loadLinks();
  }catch(e){toast('خطا در ویرایش','err')}
}
async function toggleActive(uuid,newState){
  try{const r=await authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({active:newState})});if(!r.ok)throw new Error();toast(newState?'فعال شد ':'غیرفعال شد','ok');loadLinks();}catch(e){toast('خطا','err')}
}
async function resetUsage(uuid){
  try{const r=await authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({reset_usage:true})});if(!r.ok)throw new Error();toast('مصرف ریست شد ','ok');loadLinks();}catch(e){toast('خطا','err')}
}
let atCurrentUuid = null;

function openAdTagModal(uuid, label, currentTag){
  atCurrentUuid = uuid;
  document.getElementById('at-cfg-name').textContent = label;
  document.getElementById('at-tag').value = currentTag || '';
  openModal('modal-ad-tag');
  setTimeout(()=>document.getElementById('at-tag').focus(), 150);
}

function mtPlainSecret(fullSecret){
  if (!fullSecret) return '';
  // فرمت mtg: "ee" + 32 کاراکتر هگز سکرت + دامنه‌ی fake-TLS به‌صورت هگز
  if (fullSecret.startsWith('ee') && fullSecret.length > 34) {
    return fullSecret.slice(2, 34);
  }
  return fullSecret;
}

function openMtInfoModal(label, secret, fullLink, hasPublicHost){
  document.getElementById('mti-cfg-name').textContent = label;
  document.getElementById('mti-secret').textContent = mtPlainSecret(secret) || '—';
  document.getElementById('mti-link').textContent = fullLink || '—';
  const warnEl = document.getElementById('mti-warn');
  if (warnEl) warnEl.style.display = hasPublicHost ? 'none' : 'flex';
  openModal('modal-mt-info');
}

function cpMtiField(id, msg){
  const el = document.getElementById(id);
  navigator.clipboard.writeText(el.textContent).then(()=>toast(msg,'ok'));
}

async function submitAdTag(){
  if(!atCurrentUuid) return;
  const tag = document.getElementById('at-tag').value.trim();
  if(!tag){ toast('ad_tag نمی‌تواند خالی باشد','err'); return; }

  const btn = document.getElementById('at-submit-btn');
  btn.disabled = true;
  btn.innerHTML = '<i class="ti ti-loader-2" style="animation:spin 1s linear infinite"></i> در حال اعمال...';

  try{
    const r = await authF('/api/links/'+atCurrentUuid+'/ad-tag', {
      method:'PATCH', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ad_tag: tag})
    });
    if(!r.ok){ const d = await r.json().catch(()=>({})); throw new Error(d.detail || 'خطا'); }
    closeModal('modal-ad-tag');
    toast('تبلیغ ثبت شد، پروکسی در حال ری‌استارت است...','ok');
    setTimeout(loadLinks, 2000);
  }catch(e){
    toast(' '+e.message,'err');
  }
  btn.disabled = false;
  btn.innerHTML = '<i class="ti ti-check"></i> ذخیره و اعمال';
}
async function deleteLink(uuid){
  if(!confirm('این کانفیگ غیرفعال شود؟'))return;
  try{const r=await authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({active:false})});if(!r.ok)throw new Error();toast('کانفیگ غیرفعال شد','ok');loadLinks();}catch(e){toast('خطا','err')}
}
function showQR(link){window.open('https://api.qrserver.com/v1/create-qr-code/?size=300x300&data='+encodeURIComponent(link),'_blank')}
let allSubsRaw=[];
async function loadSubs(){
  try{
    const r=await authF('/api/subs'),d=await r.json();
    const subs=d.subs||[];
    allSubsRaw=subs;
    document.getElementById('subs-nb').textContent=subs.length;
    document.getElementById('subs-pg-cnt').textContent=toFa(subs.length)+' گروه';
    renderSubsGrid(subs);
  }catch(e){console.error(e)}
}
function renderSubsGrid(subs){
  const grid=document.getElementById('subs-grid');
  if(!subs.length){
    grid.innerHTML='<div class="subs-empty-v2"><div class="subs-empty-v2-icon"><i class="ti ti-folders"></i></div><div class="subs-empty-v2-title">هنوز گروهی وجود ندارد</div><div class="subs-empty-v2-sub">یک گروه جدید بسازید تا کانفیگ‌ها را دسته‌بندی کنید</div></div>';
    return;
  }
  grid.innerHTML=subs.map(s=>`
    <div class="sub-card">
      <div class="sub-card-top">
        <div class="sub-card-head-v2">
          <div class="sub-card-icon"><i class="ti ti-folder"></i></div>
          <div class="sub-card-titles">
            <div class="sub-card-name-v2">${esc(s.name)}</div>
            ${s.desc?`<div class="sub-card-desc-v2">${esc(s.desc)}</div>`:'<div class="sub-card-desc-v2" style="opacity:.5">بدون توضیحات</div>'}
          </div>
          <div class="sub-card-lock-badge ${s.has_password?'locked':'open'}" title="${s.has_password?'رمزدار':'پابلیک'}">
            <i class="ti ${s.has_password?'ti-lock':'ti-lock-open'}"></i>
          </div>
        </div>
        <div class="sub-card-stats">
          <div class="sub-card-stat"><div class="sub-card-stat-val">${toFa(s.links_count)}</div><div class="sub-card-stat-label">کانفیگ</div></div>
          <div class="sub-card-stat"><div class="sub-card-stat-val" style="color:var(--green-t)">${toFa(s.active_count)}</div><div class="sub-card-stat-label">فعال</div></div>
          <div class="sub-card-stat"><div class="sub-card-stat-val" style="font-size:12px">${esc(s.total_used_fmt)}</div><div class="sub-card-stat-label">مصرف</div></div>
        </div>
      </div>
      <div class="sub-card-url-row">
        <span class="sub-card-url-text">${esc(s.public_url)}</span>
        <button class="sub-card-url-copy" onclick="navigator.clipboard.writeText('${esc(s.public_url)}').then(()=>toast('لینک پابلیک کپی شد','ok'))" title="کپی"><i class="ti ti-copy"></i></button>
        <button class="sub-card-url-copy" onclick="window.open('${esc(s.public_url)}','_blank')" title="باز کردن"><i class="ti ti-external-link"></i></button>
      </div>
      <div class="sub-card-bottom">
        <button class="btn btn-sm btn-g" onclick="openSubLinks('${esc(s.sub_id)}','${esc(s.name)}')"><i class="ti ti-link-plus"></i> کانفیگ‌ها</button>
        <button class="btn btn-sm btn-o" onclick="navigator.clipboard.writeText('${esc(s.sub_url)}').then(()=>toast('لینک ساب کپی شد','ok'))"><i class="ti ti-rss"></i> ساب</button>
        <button class="btn btn-sm ${s.active===false?'btn-p':'btn-amber'}" onclick="toggleSubActive('${esc(s.sub_id)}', ${s.active===false?'true':'false'})" title="فعال/غیرفعال">${s.active===false?'<i class="ti ti-player-play"></i> فعال':'<i class="ti ti-player-pause"></i> قطع'}</button>
        <button class="btn btn-sm btn-g btn-icon" onclick="showQR('${esc(s.sub_url)}')" title="QR"><i class="ti ti-qrcode"></i></button>
        <button class="btn btn-sm btn-d btn-icon" onclick="deleteSub('${esc(s.sub_id)}')" title="حذف"><i class="ti ti-trash"></i></button>
      </div>
    </div>
  `).join('');
}
function filterSubs(q){
  q=q.trim().toLowerCase();
  if(!q){renderSubsGrid(allSubsRaw);return}
  renderSubsGrid(allSubsRaw.filter(s=>s.name.toLowerCase().includes(q)||(s.desc||'').toLowerCase().includes(q)));
}
async function createSub(){
  const name=document.getElementById('ns-name').value.trim()||'گروه جدید';
  const desc=document.getElementById('ns-desc').value.trim();
  const pw=document.getElementById('ns-pw').value;
  try{
    const r=await authF('/api/subs',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,desc,password:pw})});
    if(!r.ok){const d=await r.json().catch(()=>({}));throw new Error(d.detail||'failed')}
    ['ns-name','ns-desc','ns-pw'].forEach(id=>{const el=document.getElementById(id); if(el)el.value=''});
    closeModal('modal-create-sub');
    toast('گروه ساخته شد ','ok');loadSubs();
  }catch(e){toast('خطا در ساخت گروه: '+(e.message||''),'err')}
}
async function editSubQuick(sub_id, oldName){
  const name=prompt('نام جدید گروه/مولتی:', oldName||'');
  if(!name)return;
  try{const r=await authF('/api/subs/'+sub_id,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({name})});if(!r.ok)throw new Error();toast('ویرایش شد','ok');loadSubs();loadLinks();}catch(e){toast('خطا در ویرایش','err')}
}
async function deleteSub(sub_id){
  if(!confirm('حذف این گروه؟ کانفیگ‌ها حذف نمی‌شوند.'))return;
  try{const r=await authF('/api/subs/'+sub_id,{method:'DELETE'});if(!r.ok)throw new Error();toast('گروه حذف شد ','ok');loadSubs();loadLinks();}catch(e){toast('خطا','err')}
}
let lmodalLinks=[],lmodalInSub=new Set();
async function openSubLinks(sub_id,name){
  currentSubId=sub_id;
  document.getElementById('modal-sub-name').textContent=name;
  document.getElementById('modal-links-body').innerHTML='<div style="color:var(--t3);font-size:12px;padding:20px;text-align:center"><i class="ti ti-loader-2" style="animation:spin 1s linear infinite;font-size:20px"></i></div>';
  document.getElementById('lmodal-search-inp').value='';
  openModal('modal-links');
  try{
    const [lr,sr]=await Promise.all([authF('/api/links'),authF('/api/subs')]);
    const {links=[]}=await lr.json();
    const {subs=[]}=await sr.json();
    const thisSub=subs.find(s=>s.sub_id===sub_id);
    lmodalInSub=new Set(thisSub?.link_ids||[]);
    lmodalLinks=links;
    renderLmodalList(links);
  }catch(e){toast('خطا در بارگذاری','err')}
}
function renderLmodalList(links){
  const body=document.getElementById('modal-links-body');
  if(!links.length){body.innerHTML='<div class="empty" style="padding:30px"><i class="ti ti-link-off"></i><p>هنوز کانفیگی وجود ندارد</p></div>';updateLmodalCount();return}
  body.innerHTML=links.map(l=>{
    const checked=lmodalInSub.has(l.uuid);
    const on=l.active&&!l.expired;
    return `<div class="lrow-v2 ${checked?'checked':''}" data-uuid="${l.uuid}" data-name="${esc(l.label).toLowerCase()}" onclick="toggleLrow('${l.uuid}',this)">
      <div class="lrow-v2-check"><i class="ti ti-check"></i></div>
      <div class="lrow-v2-avatar"><i class="ti ti-key"></i></div>
      <div class="lrow-v2-info">
        <div class="lrow-v2-name">${esc(l.label)}</div>
        <div class="lrow-v2-meta"><i class="ti ti-database" style="font-size:10px"></i> ${fmtB(l.used_bytes)}</div>
      </div>
      <span class="lrow-v2-status ${on?'on':'off'}">${on?'فعال':'غیرفعال'}</span>
    </div>`;
  }).join('');
  updateLmodalCount();
}
function toggleLrow(uuid,el){
  if(lmodalInSub.has(uuid)){lmodalInSub.delete(uuid);el.classList.remove('checked')}
  else{lmodalInSub.add(uuid);el.classList.add('checked')}
  updateLmodalCount();
}
function lmodalSelectAll(state){
  lmodalLinks.forEach(l=>{if(state)lmodalInSub.add(l.uuid);else lmodalInSub.delete(l.uuid)});
  renderLmodalList(lmodalLinks);
}
function updateLmodalCount(){
  const el=document.getElementById('lmodal-count');
  if(el)el.textContent=toFa(lmodalInSub.size)+' انتخاب شده';
}
function filterLmodal(q){
  q=q.trim().toLowerCase();
  document.querySelectorAll('#modal-links-body .lrow-v2').forEach(row=>{
    row.style.display = !q || row.dataset.name.includes(q) ? '' : 'none';
  });
}
async function saveSubLinks(){
  if(!currentSubId)return;
  const link_ids=[...lmodalInSub];
  try{
    const r=await authF('/api/subs/'+currentSubId,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({link_ids})});
    if(!r.ok)throw new Error();
    await Promise.all(lmodalLinks.map(l=>
      authF('/api/links/'+l.uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({sub_id:lmodalInSub.has(l.uuid)?currentSubId:null})})
    ));
    closeModal('modal-links');
    toast('کانفیگ‌های گروه ذخیره شدند ','ok');
    loadSubs();loadLinks();
  }catch(e){toast('خطا در ذخیره','err')}
}
async function loadSubsPage(){
  document.getElementById('sub-all-url').textContent=location.protocol+'//'+location.host+'/sub-all';
  try{
    const r=await authF('/api/subs'),d=await r.json();
    const subs=d.subs||[];
    const el=document.getElementById('sub-groups-list');
    if(!subs.length){el.innerHTML='<div class="empty"><i class="ti ti-rss-off"></i><p>هنوز گروهی ندارید</p></div>';return}
    el.innerHTML=subs.map(s=>`
      <div style="padding:13px 15px;background:var(--accent-d);border:1px solid var(--card-b);border-radius:10px;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap">
        <div>
          <div style="font-weight:700;font-size:13px;margin-bottom:3px">${esc(s.name)}</div>
          <div style="font-family:ui-monospace,monospace;font-size:10px;color:var(--purple-t)">${esc(s.sub_url)}</div>
          <div style="font-size:10px;color:var(--t3);margin-top:3px">${toFa(s.links_count)} کانفیگ · ${esc(s.total_used_fmt)} مصرف ${s.has_password?'·  رمزدار':''}</div>
        </div>
        <div style="display:flex;gap:5px;flex-wrap:wrap">
          <button class="btn btn-sm btn-pur" onclick="navigator.clipboard.writeText('${esc(s.sub_url)}').then(()=>toast('کپی شد','ok'))"><i class="ti ti-copy"></i> ساب</button>
          <button class="btn btn-sm btn-pur" onclick="navigator.clipboard.writeText('${esc(s.public_url)}').then(()=>toast('کپی شد','ok'))"><i class="ti ti-globe"></i> پابلیک</button>
          <button class="btn btn-sm btn-g" onclick="showQR('${esc(s.sub_url)}')"><i class="ti ti-qrcode"></i></button>
        </div>
      </div>
    `).join('');
  }catch(e){}
}
function cpSubAll(){navigator.clipboard.writeText(location.protocol+'//'+location.host+'/sub-all').then(()=>toast('کپی شد ','ok'))}
function parseBytesFmt(s){
  if(!s)return 0;
  const m=String(s).match(/([\d.]+)\s*([A-Za-z]+)/);
  if(!m)return 0;
  const n=parseFloat(m[1]),u=m[2].toUpperCase();
  const mult={B:1,KB:1024,MB:1024**2,GB:1024**3,TB:1024**4};
  return n*(mult[u]||1);
}
async function loadConns(){
  try{
    const r=await authF('/api/connections'),d=await r.json();
    const grid=document.getElementById('conns-grid'),ce=document.getElementById('conns-empty');
    document.getElementById('conns-live').innerHTML='<span class="dot dg pulse"></span> '+d.count+' اتصال';
    document.getElementById('ch-count').textContent=toFa(d.count);
    const conns=d.connections||[];
    if(!d.count){
      grid.innerHTML='';ce.style.display='block';
      document.getElementById('ch-traffic').textContent='—';
      document.getElementById('ch-avgdur').textContent='—';
      document.getElementById('ch-uniq').textContent='—';
      return;
    }
    ce.style.display='none';
    const totalBytes=conns.reduce((s,c)=>s+parseBytesFmt(c.bytes_fmt),0);
    document.getElementById('ch-traffic').textContent=fmtB(totalBytes);
    const uniqIps=new Set(conns.map(c=>c.ip)).size;
    document.getElementById('ch-uniq').textContent=toFa(uniqIps);
    const durs=conns.map(c=>c.connected_at?Math.max(0,Math.floor((Date.now()-new Date(c.connected_at).getTime())/1000)):0);
    const avgSec=durs.length?Math.floor(durs.reduce((a,b)=>a+b,0)/durs.length):0;
    document.getElementById('ch-avgdur').textContent=avgSec<60?avgSec+' ث':avgSec<3600?Math.floor(avgSec/60)+' د':Math.floor(avgSec/3600)+' س';
    const maxDur=Math.max(...durs,1);
    grid.innerHTML=conns.map(c=>{
      const secs=c.connected_at?Math.max(0,Math.floor((Date.now()-new Date(c.connected_at).getTime())/1000)):0;
      const dur=secs<60?secs+' ثانیه':secs<3600?Math.floor(secs/60)+' دقیقه':Math.floor(secs/3600)+' ساعت';
      const durPct=Math.min(100,Math.round((secs/maxDur)*100));
      const protoVal=c.transport==='vless-ws'?'vless-ws':(c.transport||'').replace('xhttp-','xhttp-');
      return `<div class="conn-card-v2">
        <div class="conn-card-v2-glow"></div>
        <div class="conn-card-v2-top">
          <div class="conn-avatar"><i class="ti ti-device-desktop"></i></div>
          <div class="conn-card-v2-id">
            <div class="conn-ip-v2">${esc(c.ip)}
              <button class="conn-ip-copy" onclick="navigator.clipboard.writeText('${esc(c.ip)}').then(()=>toast('IP کپی شد','ok'))" title="کپی IP"><i class="ti ti-copy"></i></button>
            </div>
            <div class="conn-label-v2">${esc(c.label)}</div>
          </div>
          <span class="conn-status-pill"><span class="dot dg pulse"></span> زنده</span>
        </div>
        <div class="conn-card-v2-divider"></div>
        <div class="conn-card-v2-body">
          <div class="conn-proto-row">${protoBadge(protoVal)}</div>
          <div class="conn-stat-row">
            <div class="conn-stat-box">
              <div class="conn-stat-icon"><i class="ti ti-transfer"></i></div>
              <div>
                <div class="conn-stat-text-label">ترافیک</div>
                <div class="conn-stat-text-val">${esc(c.bytes_fmt)}</div>
              </div>
            </div>
            <div class="conn-stat-box">
              <div class="conn-stat-icon time"><i class="ti ti-clock"></i></div>
              <div>
                <div class="conn-stat-text-label">مدت اتصال</div>
                <div class="conn-stat-text-val">${dur}</div>
              </div>
            </div>
          </div>
          <div class="conn-duration-track"><div class="conn-duration-fill" style="width:${durPct}%"></div></div>
        </div>
      </div>`;
    }).join('');
  }catch(e){console.error(e)}
}
async function loadErrs(){try{const r=await authF('/stats'),d=await r.json();renderErrs(d.recent_errors||[]);}catch(e){}}
async function fetchDefaultVless(){
  try{const r=await authF('/api/links'),d=await r.json();const links=d.links||[];const def=links.find(l=>l.limit_bytes===0&&l.active&&!l.expired)||links.find(l=>l.active&&!l.expired)||links[0];document.getElementById('vless-main').textContent=def?def.vless_link:'هنوز کانفیگی وجود ندارد';}catch(e){}
}
function cpText(id){navigator.clipboard.writeText(document.getElementById(id).textContent).then(()=>toast('کپی شد ','ok'))}
function qrFor(id){showQR(document.getElementById(id).textContent)}
function refreshAll(){fetchStats();fetchDefaultVless();loadLinks();if(document.getElementById('pg-subgroups').classList.contains('on'))loadSubs();if(document.getElementById('pg-subscriptions').classList.contains('on'))loadSubsPage();if(document.getElementById('pg-connections').classList.contains('on'))loadConns();if(document.getElementById('pg-logs').classList.contains('on'))loadActivity();toast('رفرش شد','ok')}


let cfEditingKey='';
async function loadCloudflareDomains(){
  try{
    const r=await authF('/api/cloudflare/domains'),d=await r.json();
    const list=d.domains||[]; window.__cfDomains=list; const cnt=document.getElementById('cf-count'); if(cnt)cnt.textContent=toFa(list.length);
    const el=document.getElementById('cf-list'); if(!el)return;
    el.innerHTML=list.map(x=>`<div class="health-row"><div><b>${esc(x.name||x.domain)}</b><div class="pro-muted" dir="ltr">${esc(x.domain)} · ${toFa((x.clean_ips||[]).length)} IP</div><div class="vl-code" style="margin-top:8px" dir="ltr">${esc(x.sub_url)}</div></div><div style="display:flex;gap:6px;flex-wrap:wrap"><button class="btn btn-p btn-sm" onclick="navigator.clipboard.writeText('${esc(x.sub_url)}').then(()=>toast('ساب کلادفلیر کپی شد','ok'))"><i class="ti ti-copy"></i></button><button class="btn btn-amber btn-sm" onclick="editCloudflareDomain('${esc(x.id||x.slug||x.domain)}')"><i class="ti ti-edit"></i> ویرایش</button><button class="btn btn-d btn-sm" onclick="deleteCloudflareDomain('${esc(x.slug||x.domain)}')"><i class="ti ti-trash"></i></button></div></div>`).join('')||'<div class="empty"><i class="ti ti-cloud-off"></i><p>دامنه‌ای ثبت نشده</p></div>';
  }catch(e){console.error(e);toast('خطا در بارگذاری کلادفلیر','err')}
}
function editCloudflareDomain(key){
  const x=(window.__cfDomains||[]).find(d=>d.id===key||d.slug===key||d.domain===key); if(!x)return;
  cfEditingKey=x.id||x.slug||x.domain; const ek=document.getElementById('cf-edit-key'); if(ek)ek.value=cfEditingKey;
  document.getElementById('cf-domain').value=x.domain||''; document.getElementById('cf-name').value=x.name||''; document.getElementById('cf-ips').value=(x.clean_ips||[]).join('\n');
  toast('دامنه برای ویرایش آماده شد','ok'); window.scrollTo({top:0,behavior:'smooth'});
}
async function saveCloudflareDomain(){
  const domain=document.getElementById('cf-domain').value.trim(); const name=document.getElementById('cf-name').value.trim(); const clean_ips=document.getElementById('cf-ips').value.trim(); const key=(document.getElementById('cf-edit-key')?.value||cfEditingKey||'').trim();
  if(!domain){toast('دامنه را وارد کن','err');return}
  try{const r=await authF('/api/cloudflare/domains',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key,domain,name,clean_ips})}); const d=await r.json().catch(()=>({})); if(!r.ok)throw new Error(d.detail||'خطا'); navigator.clipboard?.writeText(d.sub_url||''); toast(key?'دامنه کلادفلیر ویرایش شد':'دامنه کلادفلیر ذخیره شد و ساب کپی شد','ok'); cfEditingKey=''; const ek=document.getElementById('cf-edit-key'); if(ek)ek.value=''; loadCloudflareDomains();loadExtraDomains();}
  catch(e){toast(' '+e.message,'err')}
}
async function deleteCloudflareDomain(key){if(!confirm('دامنه کلادفلیر حذف شود؟'))return; try{await authF('/api/cloudflare/domains/'+encodeURIComponent(key),{method:'DELETE'});toast('حذف شد','ok');loadCloudflareDomains();loadExtraDomains()}catch(e){toast('خطا','err')}}

async function loadExtraDomains(){
  try{
    const r=await authF('/api/extra-domains'); const d=await r.json();
    const list=d.domains||[]; window.__exDomains=list;
    document.getElementById('ex-count').textContent=toFa(list.length);
    document.getElementById('ex-list').innerHTML=list.map(x=>`<div class="row-item" style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:10px 0;border-bottom:1px solid var(--border)">
      <div style="flex:1;min-width:160px"><div style="font-weight:600">${esc(x.name||x.domain)}</div><div class="muted" dir="ltr" style="font-size:12px">${esc(x.domain)} · ${toFa((x.clean_ips||[]).length)} IP تمیز</div></div>
      <button class="btn btn-sm btn-g" onclick="navigator.clipboard.writeText('${esc(x.sub_url||'')}').then(()=>toast('ساب دامنه فرعی کپی شد','ok'))"><i class="ti ti-copy"></i> ساب</button>
      <button class="btn btn-sm btn-g" onclick="editExtraDomain('${esc(x.id||x.slug||x.domain)}')"><i class="ti ti-edit"></i></button>
      <button class="btn btn-sm btn-d" onclick="deleteExtraDomain('${esc(x.slug||x.domain)}')"><i class="ti ti-trash"></i></button>
    </div>`).join('')||'<div class="empty"><i class="ti ti-link-off"></i><p>دامنه فرعی ثبت نشده</p></div>';
  }catch(e){console.error(e);toast('خطا در بارگذاری دامنه فرعی','err')}
}
function editExtraDomain(key){
  const x=(window.__exDomains||[]).find(d=>d.id===key||d.slug===key||d.domain===key); if(!x)return;
  document.getElementById('ex-edit-key').value=x.id||x.slug||x.domain||'';
  document.getElementById('ex-domain').value=x.domain||'';
  document.getElementById('ex-name').value=x.name||'';
  const ips=document.getElementById('ex-ips'); if(ips) ips.value=(x.clean_ips||[]).join('\n');
  toast('دامنه فرعی برای ویرایش آماده شد','ok'); window.scrollTo({top:0,behavior:'smooth'});
}
async function saveExtraDomain(){
  const key=(document.getElementById('ex-edit-key').value||'').trim();
  const domain=(document.getElementById('ex-domain').value||'').trim();
  const name=(document.getElementById('ex-name').value||'').trim();
  const clean_ips=(document.getElementById('ex-ips')?.value||'').trim();
  if(!domain){toast('دامنه فرعی را وارد کن','err');return}
  try{
    const r=await authF('/api/extra-domains',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key,domain,name,clean_ips})});
    const d=await r.json().catch(()=>({}));
    if(!r.ok)throw new Error(d.detail||'خطا');
    navigator.clipboard?.writeText(d.sub_url||'');
    toast(key?'دامنه فرعی ویرایش شد':'دامنه فرعی ذخیره شد و ساب کپی شد','ok');
    document.getElementById('ex-edit-key').value='';
    document.getElementById('ex-domain').value='';
    document.getElementById('ex-name').value='';
    const ips=document.getElementById('ex-ips'); if(ips) ips.value='';
    loadExtraDomains();
  }catch(e){toast(e.message||'خطا','err')}
}
async function deleteExtraDomain(key){if(!confirm('دامنه فرعی حذف شود؟'))return; try{await authF('/api/extra-domains/'+encodeURIComponent(key),{method:'DELETE'});toast('حذف شد','ok');loadExtraDomains()}catch(e){toast('خطا','err')}}

async function saveRemarkTemplates(){
  const remark_template=(document.getElementById('remark-template')?.value||'').trim();
  const info_templates=(document.getElementById('info-templates')?.value||'');
  const info_configs_enabled=!!(document.getElementById('info-configs-enabled')?.checked);
  try{
    const r=await authF('/api/settings',{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({remark_template,info_templates,info_configs_enabled})});
    const d=await r.json().catch(()=>({}));
    if(!r.ok) throw new Error(d.detail||'خطا');
    toast('قالب نام کانفیگ و خطوط آماری ذخیره شد','ok');
  }catch(e){toast(String(e.message||e),'err')}
}
async function toggleSubActive(sub_id, active){
  try{
    const r=await authF('/api/subs/'+sub_id,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({active:!!active})});
    if(!r.ok) throw new Error('خطا');
    toast(active?'اشتراک فعال شد':'اشتراک غیرفعال شد و کانفیگ‌ها قطع شدند', active?'ok':'warn');
    loadSubs(); loadLinks();
  }catch(e){toast('خطا','err')}
}

async function loadPanelDomain(){
  try{
    const r=await authF('/api/settings'); const d=await r.json();
    const panel=(d.settings&&d.settings.panel)||{};
    const inp=document.getElementById('panel-domain');
    if(inp) inp.value=panel.domain||'';
    const dd=document.getElementById('data-dir-path'); if(dd) dd.textContent=d.data_dir||'—';
    const dok=document.getElementById('data-dir-ok'); if(dok) dok.textContent=d.data_persistent?'بله (Volume)':'خیر — Volume روی /data بساز';
    const rt=document.getElementById('remark-template'); if(rt) rt.value=(d.settings&&d.settings.remark_template)||'{status_emoji} {label} · {target}';
    const it=document.getElementById('info-templates'); if(it) it.value=((d.settings&&d.settings.info_templates)||[]).join('\n');
    const ice=document.getElementById('info-configs-enabled'); if(ice) ice.checked=d.settings?d.settings.info_configs_enabled!==false:true;
    const act=document.getElementById('panel-domain-active');
    const def=document.getElementById('panel-domain-default');
    if(act) act.textContent=d.host||location.host;
    if(def) def.textContent=d.default_host||location.host;
    const sh=document.getElementById('set-host');
    if(sh) sh.textContent=d.host||location.host;
    loadLoginPathSettings(d);
    loadTcpRealitySettings(d);
  }catch(e){console.error(e)}
}

function loadTcpRealitySettings(d){
  try{
    const s=(d&&d.settings)||{};
    const tcp=s.railway_tcp||{};
    const real=s.reality||{};
    const set=(id,v)=>{const el=document.getElementById(id);if(el)el.value=(v==null||v===0)?'':v;};
    set('tcp-domain',tcp.domain||'');
    set('tcp-port',tcp.port||'');
    const pm=document.getElementById('tcp-path-mode'); if(pm) pm.value=tcp.path_mode||'root';
    const ap=document.getElementById('tcp-app-port'); if(ap) ap.textContent=String(d.app_port||'—');
    set('reality-host',real.host||'');
    set('reality-port',real.port||'');
    set('reality-pbk',real.pbk||'');
    set('reality-sid',real.sid||'');
    set('reality-sni',real.sni||'');
    set('reality-fp',real.fp||'chrome');
    set('reality-spx',real.spx||'/');
  }catch(e){}
}
async function saveRailwayTcp(){
  const domain=(document.getElementById('tcp-domain').value||'').trim();
  const port=Number(document.getElementById('tcp-port').value||0);
  const path_mode=document.getElementById('tcp-path-mode').value||'root';
  try{
    const r=await authF('/api/settings',{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({railway_tcp:{domain,port,path_mode}})});
    const d=await r.json().catch(()=>({}));
    if(!r.ok) throw new Error(d.detail||'خطا');
    toast('تنظیمات Railway TCP Route ذخیره شد','ok');
    loadTcpRealitySettings(d);
  }catch(e){toast(String(e.message||e),'err')}
}
async function saveRealitySettings(){
  const host=(document.getElementById('reality-host').value||'').trim();
  const port=Number(document.getElementById('reality-port').value||443);
  const pbk=(document.getElementById('reality-pbk').value||'').trim();
  const sid=(document.getElementById('reality-sid').value||'').trim();
  const sni=(document.getElementById('reality-sni').value||'').trim();
  const fp=(document.getElementById('reality-fp').value||'').trim()||'chrome';
  const spx=(document.getElementById('reality-spx').value||'').trim()||'/';
  try{
    const r=await authF('/api/settings',{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({reality:{host,port,pbk,sid,sni,fp,spx}})});
    const d=await r.json().catch(()=>({}));
    if(!r.ok) throw new Error(d.detail||'خطا');
    toast('تنظیمات Reality ذخیره شد','ok');
    loadTcpRealitySettings(d);
  }catch(e){toast(String(e.message||e),'err')}
}
async function generateRealityParams(){
  try{
    const r=await authF('/api/settings/reality/generate',{method:'POST'});
    const d=await r.json().catch(()=>({}));
    if(!r.ok) throw new Error(d.detail||'خطا');
    loadTcpRealitySettings({settings:{reality:d.reality||{},railway_tcp:(window.__lastSettings&&window.__lastSettings.railway_tcp)||{}},app_port:d.app_port});
    // reload full settings for consistency
    const r2=await authF('/api/settings'); const full=await r2.json();
    loadTcpRealitySettings(full);
    toast('pbk / sid / sni به‌صورت تصادفی ساخته شد','ok');
  }catch(e){toast(String(e.message||e),'err')}
}

async function loadLoginPathSettings(d){
  try{
    if(!d){const r=await authF('/api/settings'); d=await r.json();}
    const path=(d.login_path || (d.settings&&d.settings.panel&&d.settings.panel.login_path) || '');
    const url=d.login_url || (path?('/'+path+'/login'):'/login');
    const dash=d.dashboard_url || (path?('/'+path+'/dashboard'):'/dashboard');
    const inp=document.getElementById('panel-login-path');
    if(inp) inp.value=path||'';
    const u=document.getElementById('panel-login-url');
    if(u) u.textContent=url;
    const du=document.getElementById('panel-dashboard-url');
    if(du) du.textContent=dash;
    try{
      localStorage.setItem('oxnet-login-url', url);
      localStorage.setItem('oxnet-dash-url', dash);
    }catch(e){}
    window.OXNET_LOGIN=url;
    window.OXNET_DASH=dash;
    window.OXNET_BASE=d.panel_base || (path?('/'+path):'');
  }catch(e){}
}
async function saveLoginPath(){
  const login_path=(document.getElementById('panel-login-path').value||'').trim();
  try{
    const r=await authF('/api/settings',{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({panel:{login_path}})});
    const d=await r.json();
    if(!r.ok) throw new Error((d.detail&&(d.detail.message||d.detail))||'خطا');
    await loadLoginPathSettings(d);
    toast('مسیر ذخیره شد — ورود: '+(d.login_url||'/login')+' | داشبورد: '+(d.dashboard_url||'/dashboard'),'ok');
  }catch(e){toast(String(e.message||e),'err')}
}
async function clearLoginPath(){
  const inp=document.getElementById('panel-login-path');
  if(inp) inp.value='';
  await saveLoginPath();
}

async function savePanelDomain(){
  const domain=(document.getElementById('panel-domain').value||'').trim();
  try{
    const r=await authF('/api/settings',{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({panel:{domain}})});
    const d=await r.json().catch(()=>({}));
    if(!r.ok)throw new Error(d.detail||'خطا');
    toast('دامنه اصلی پنل ذخیره شد','ok');
    loadPanelDomain();
  }catch(e){toast(e.message||'خطا','err')}
}

async function loadDbStatus(){try{const el=document.getElementById('storage-mode-label');if(el)el.textContent='JSON File';}catch(e){}}
async function saveThemeStudio(){try{await authF('/api/settings',{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({theme:{accent:selectedThemeColor}})});toast('قالب ذخیره شد','ok')}catch(e){toast('خطا','err')}}
async function createSmartSub(){const label=document.getElementById('smart-label').value||'Smart Iran';const profile=document.getElementById('smart-profile').value;try{const r=await authF('/api/smart-subscription',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({label,profile})});const d=await r.json();if(!r.ok)throw new Error(d.detail||'خطا');navigator.clipboard?.writeText(d.sub_url);toast('ساب هوشمند ساخته و کپی شد','ok');loadLinks();loadSubs();}catch(e){toast(' '+e.message,'err')}}
async function loadHealth(){try{const r=await authF('/api/config-health'),d=await r.json();const el=document.getElementById('health-list');if(!el)return;el.innerHTML=(d.items||[]).slice(0,8).map(x=>`<div class="health-row"><div><b>${esc(x.label)}</b><div class="pro-muted">${esc(x.protocol)} · ${esc(x.status)} · ${(x.reasons||[]).join('، ')||'بدون مشکل'}</div></div><span class="score-pill">${toFa(x.score)}</span></div>`).join('')||'<div class="pro-muted">کانفیگی نیست</div>'}catch(e){}}
async function loadMonitoring(){try{const r=await authF('/api/monitoring'),d=await r.json();const el=document.getElementById('monitoring-box');if(!el)return;el.innerHTML=`<div class="sr"><span class="sr-k">دیتابیس</span><span class="sr-v">${esc(d.db_mode)}</span></div><div class="sr"><span class="sr-k">Top مصرف</span><span class="sr-v">${(d.top_links||[]).slice(0,3).map(x=>esc(x.label)).join('، ')||'—'}</span></div><div class="sr"><span class="sr-k">IP آنلاین</span><span class="sr-v">${(d.top_ips||[]).length}</span></div>`}catch(e){}}
function exportBackup(){window.open('/api/backup/export','_blank')}
async function saveRestorePoint(){const name=prompt('نام بکاپ/ریستور پوینت؟','Backup '+new Date().toLocaleString('fa-IR'));if(!name)return;try{await authF('/api/backup/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name})});toast('Restore Point ذخیره شد','ok');loadRestorePoints()}catch(e){toast('خطا','err')}}
async function loadRestorePoints(){try{const r=await authF('/api/backup/restore-points'),d=await r.json();const el=document.getElementById('restore-points');if(!el)return;el.innerHTML=(d.items||[]).slice().reverse().map(b=>`<div class="health-row"><div><b>${esc(b.name)}</b><div class="pro-muted">${new Date(b.created_at).toLocaleString('fa-IR')}</div></div><button class="btn btn-p btn-sm" onclick="restorePoint('${b.id}')"><i class="ti ti-history-toggle"></i> ریستور</button></div>`).join('')||'<div class="pro-muted">هنوز Restore Point ندارید</div>'}catch(e){}}
async function restorePoint(id){if(!confirm('ریستور انجام شود؟ اطلاعات فعلی با بکاپ جایگزین می‌شود.'))return;try{const r=await authF('/api/backup/restore/'+id,{method:'POST'});const d=await r.json();if(!r.ok)throw new Error(d.detail||'خطا');toast('ریستور انجام شد','ok');refreshAll();loadProTools();loadCustomers()}catch(e){toast(' '+e.message,'err')}}
async function importBackup(){const raw=document.getElementById('backup-import').value.trim();if(!raw){toast('JSON بکاپ را وارد کن','err');return}try{const data=JSON.parse(raw);const r=await authF('/api/backup/import',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});const d=await r.json();if(!r.ok)throw new Error(d.detail||'خطا');toast('بکاپ ایمپورت شد','ok');refreshAll()}catch(e){toast(' '+e.message,'err')}}
async function runCleanup(){const expired_days=Number(document.getElementById('clean-expired').value||0),inactive_days=Number(document.getElementById('clean-inactive').value||0);try{const r=await authF('/api/cleanup/run',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({expired_days,inactive_days,reset_logs:false})});const d=await r.json();toast(`پاک‌سازی: ${toFa(d.deleted)} حذف، ${toFa(d.archived)} آرشیو`,'ok');refreshAll()}catch(e){toast('خطا','err')}}
async function loadCustomers(){try{const r=await authF('/api/customers'),d=await r.json();const el=document.getElementById('customers-list');if(!el)return;el.innerHTML=(d.customers||[]).map(c=>`<div class="cust-row"><div><b>${esc(c.name)}</b><div class="pro-muted">${esc(c.phone||'')} · ${esc(c.note||'')}</div></div><span class="badge bg-blue">${toFa((c.link_ids||[]).length)} کانفیگ</span><button class="btn btn-d btn-sm" onclick="deleteCustomer('${c.customer_id}')"><i class="ti ti-trash"></i></button></div>`).join('')||'<div class="empty"><i class="ti ti-users"></i><p>کاربری ثبت نشده</p></div>'}catch(e){}}
async function createCustomer(){const name=document.getElementById('cust-name').value,phone=document.getElementById('cust-phone').value,note=document.getElementById('cust-note').value;if(!name){toast('نام را وارد کن','err');return}try{await authF('/api/customers',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,phone,note})});['cust-name','cust-phone','cust-note'].forEach(id=>document.getElementById(id).value='');toast('کاربر ساخته شد','ok');loadCustomers()}catch(e){toast('خطا','err')}}
async function deleteCustomer(id){if(!confirm('حذف کاربر؟'))return;await authF('/api/customers/'+id,{method:'DELETE'});toast('حذف شد','ok');loadCustomers()}
async function loadSecuritySettings(){try{const r=await authF('/api/settings'),d=await r.json();const sec=d.settings.security||{};document.getElementById('sec-max').value=sec.max_attempts||5;document.getElementById('sec-min').value=sec.lock_minutes||10;document.getElementById('sec-ips').value=(sec.allowed_ips||[]).join(',')}catch(e){}}
async function saveSecuritySettings(){const max_attempts=Number(document.getElementById('sec-max').value||5),lock_minutes=Number(document.getElementById('sec-min').value||10),allowed_ips=document.getElementById('sec-ips').value.split(',').map(x=>x.trim()).filter(Boolean);try{await authF('/api/settings',{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({security:{max_attempts,lock_minutes,allowed_ips}})});toast('تنظیمات امنیت ذخیره شد','ok')}catch(e){toast('خطا','err')}}
applyAccent(selectedThemeColor);

async function changePw(){
  const cur=document.getElementById('cp-cur').value,nw=document.getElementById('cp-new').value,cf=document.getElementById('cp-cf').value;
  if(!cur||!nw||!cf){toast('همه فیلدها را پر کنید','err');return}
  if(nw.length<4){toast('حداقل ۴ کاراکتر','err');return}
  if(nw!==cf){toast('تکرار رمز اشتباه','err');return}
  try{
    const r=await authF('/api/change-password',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({current_password:cur,new_password:nw})});
    const d=await r.json().catch(()=>({}));
    if(!r.ok)throw new Error(d.detail||'خطا');
    toast('رمز تغییر کرد و در دیتابیس/بکاپ ذخیره شد','ok');
    ['cp-cur','cp-new','cp-cf'].forEach(id=>document.getElementById(id).value='');
  }catch(e){toast(' '+e.message,'err')}
}
function togglePwField(id,btn){
  const inp=document.getElementById(id);
  const icon=btn.querySelector('i');
  const toText=inp.type==='password';
  inp.type=toText?'text':'password';
  icon.className='ti '+(toText?'ti-eye-off':'ti-eye');
}
function checkPwStrength(val){
  const segs=document.querySelectorAll('#pw-strength-bar .pw-strength-seg');
  const label=document.getElementById('pw-strength-label');
  const reqLen=document.getElementById('req-len'),reqNum=document.getElementById('req-num'),reqCase=document.getElementById('req-case');
  const hasLen=val.length>=4,hasNum=/\d/.test(val),hasCase=/[a-z]/.test(val)&&/[A-Z]/.test(val),hasLong=val.length>=8;
  reqLen.classList.toggle('met',hasLen);
  reqNum.classList.toggle('met',hasNum);
  reqCase.classList.toggle('met',hasCase);
  let score=0;if(hasLen)score++;if(hasNum)score++;if(hasCase)score++;if(hasLong)score++;
  const colors=['#EF4444','#F59E0B','#475569','#10B981'],labels=['خیلی ضعیف','ضعیف','متوسط','قوی'];
  segs.forEach((s,i)=>{s.style.background=i<score?colors[Math.max(0,score-1)]:'rgba(100,116,139,.2)'});
  if(val.length===0){label.innerHTML='<i class="ti ti-shield"></i> قدرت رمز';return}
  label.innerHTML=`<i class="ti ti-shield-check" style="color:${colors[Math.max(0,score-1)]}"></i> ${labels[Math.max(0,score-1)]}`;
}

function renderFallbackCharts(labels=[], vals=[], pc={}){
  const ch1Box=document.getElementById('ox-fallback-ch1');
  if(ch1Box){
    const max=Math.max(...vals,1);
    ch1Box.innerHTML = labels.map((l,i)=>`<div class="fb-bar" title="${esc(l)} · ${(vals[i]||0).toFixed(2)} MB"><span style="height:${Math.max(4,((vals[i]||0)/max)*100)}%"></span><b>${esc(String(l).slice(-5))}</b></div>`).join('') || '<div class="pro-muted">هنوز مصرفی ثبت نشده</div>';
  }
  const ch2Box=document.getElementById('ox-fallback-ch2');
  if(ch2Box){
    const items=[['VLESS',pc.vless_ws||0],['Trojan',pc.trojan_ws||0],['XHTTP',pc.xhttp||0],['SS',pc.shadowsocks_tls||0],['MTProto',pc.mtproto||0]];
    const total=Math.max(items.reduce((a,x)=>a+x[1],0),1);
    ch2Box.innerHTML=items.map(([k,v])=>`<div class="fb-proto"><span>${k}</span><div><i style="width:${(v/total*100).toFixed(1)}%"></i></div><b>${toFa(v)}</b></div>`).join('');
  }
}
function setupFallbackCharts(){
  const c1=document.getElementById('ch1'), c2=document.getElementById('ch2');
  if(c1) c1.parentElement.innerHTML='<div id="ox-fallback-ch1" class="fallback-bars"></div>';
  if(c2) c2.parentElement.innerHTML='<div id="ox-fallback-ch2" class="fallback-protos"></div>';
  renderFallbackCharts([],[],{});
}

function makeGradient(ctx,color1,color2){
  const g=ctx.createLinearGradient(0,0,0,260);
  g.addColorStop(0,color1);g.addColorStop(1,color2);
  return g;
}

function drawSpark(id, values, color){
  const c=document.getElementById(id); if(!c) return;
  const ctx=c.getContext('2d');
  const w=c.width, h=c.height;
  ctx.clearRect(0,0,w,h);
  const data=(values&&values.length)?values:[2,3,2,4,3,5,4,6,5,7,6,8];
  const max=Math.max(...data,1), min=Math.min(...data,0);
  const range=Math.max(max-min, 0.1);
  ctx.beginPath();
  data.forEach((v,i)=>{
    const x=(i/(data.length-1))*w;
    const y=h-4-((v-min)/range)*(h-8);
    if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
  });
  ctx.strokeStyle=color||'#2563EB';
  ctx.lineWidth=2;
  ctx.lineJoin='round';
  ctx.lineCap='round';
  ctx.stroke();
  // soft fill
  const lastX=w, lastY=h-4-((data[data.length-1]-min)/range)*(h-8);
  ctx.lineTo(lastX,h); ctx.lineTo(0,h); ctx.closePath();
  ctx.fillStyle=(color||'#2563EB').replace(')', ',0.12)').replace('rgb', 'rgba').replace('#2563EB','rgba(37,99,235,0.12)').replace('#16A34A','rgba(22,163,74,0.12)');
  if((color||'').startsWith('#')){
    const hex=color||'#2563EB';
    const r=parseInt(hex.slice(1,3),16), g=parseInt(hex.slice(3,5),16), b=parseInt(hex.slice(5,7),16);
    ctx.fillStyle=`rgba(${r},${g},${b},0.12)`;
  }
  ctx.fill();
}
function seedSparks(hourly){
  const vals=Object.values(hourly||{}).map(Number);
  const series=vals.length?vals.slice(-12):null;
  drawSpark('spark-conns', series, '#2563EB');
  drawSpark('spark-traffic', series, '#16A34A');
  drawSpark('spark-links', series, '#0EA5E9');
  drawSpark('spark-subs', series, '#D97706');
}

function initCharts(){
  if(typeof Chart==='undefined'){setupFallbackCharts();return;}
  try{
    const el1=document.getElementById('ch1');
    const el2=document.getElementById('ch2');
    const el3=document.getElementById('ch3');
    if(!el1 && !el2 && !el3) return;

    const tick = '#94A3B8';
    const grid = 'rgba(37,99,235,.06)';
    const tipBg = 'rgba(15,23,42,.96)';

    if(el1){
      const c1=el1.getContext('2d');
      const grad1=makeGradient(c1,'rgba(37,99,235,.15)','rgba(37,99,235,0)');
      const opts={
        responsive:true,maintainAspectRatio:false,
        interaction:{mode:'index',intersect:false},
        plugins:{
          legend:{display:false},
          tooltip:{
            backgroundColor:tipBg,borderColor:'rgba(37,99,235,.15)',borderWidth:1,
            titleColor:'#F8FAFC',bodyColor:'#CBD5E1',padding:10,cornerRadius:10,displayColors:false,
            titleFont:{family:'Vazirmatn',size:11,weight:'700'},bodyFont:{family:'Vazirmatn',size:11},
            callbacks:{label:v=>`${v.parsed.y.toFixed(2)} مگابایت`}
          }
        },
        scales:{
          x:{grid:{display:false},border:{display:false},ticks:{color:tick,font:{size:9,family:'Vazirmatn'}}},
          y:{grid:{color:grid},border:{display:false},ticks:{color:tick,font:{size:9,family:'Vazirmatn'},callback:v=>v+' MB'}}
        },
        elements:{line:{capBezierPoints:true}}
      };
      const ds1={label:'MB',data:[],borderColor:'#2563EB',backgroundColor:grad1,fill:true,tension:.4,pointRadius:0,pointHoverRadius:5,pointHoverBackgroundColor:'#2563EB',pointHoverBorderColor:'#fff',pointHoverBorderWidth:2,borderWidth:3};
      ch1=new Chart(el1,{type:'line',data:{labels:[],datasets:[ds1]},options:opts});
    }

    if(el3){
      const c3ctx=el3.getContext('2d');
      function makeGradientV2(ctx,a,b,c){
        const g=ctx.createLinearGradient(0,0,0,320);
        g.addColorStop(0,a);g.addColorStop(.6,b);g.addColorStop(1,c);
        return g;
      }
      const gradFill3=makeGradientV2(c3ctx,'rgba(37,99,235,.15)','rgba(37,99,235,.05)','rgba(37,99,235,0)');
      ch3=new Chart(el3,{
        type:'line',
        data:{labels:[],datasets:[
          {label:'مصرف',data:[],borderColor:'#2563EB',backgroundColor:gradFill3,fill:true,tension:.4,pointRadius:0,pointHoverRadius:5,pointHoverBackgroundColor:'#fff',pointHoverBorderColor:'#2563EB',pointHoverBorderWidth:2,borderWidth:3,order:2},
          {label:'میانگین',data:[],borderColor:'#D97706',borderDash:[6,5],borderWidth:1.5,pointRadius:0,fill:false,tension:0,order:1}
        ]},
        options:{
          responsive:true,maintainAspectRatio:false,
          interaction:{mode:'index',intersect:false},
          plugins:{
            legend:{display:false},
            tooltip:{
              backgroundColor:tipBg,borderColor:'rgba(37,99,235,.15)',borderWidth:1,
              titleColor:'#F8FAFC',bodyColor:'#CBD5E1',padding:10,cornerRadius:10,displayColors:true,boxPadding:4,
              titleFont:{family:'Vazirmatn',size:11,weight:'700'},bodyFont:{family:'Vazirmatn',size:11},
              callbacks:{label:v=>` ${v.dataset.label}: ${v.parsed.y.toFixed(2)} MB`}
            }
          },
          scales:{
            x:{grid:{display:false},border:{display:false},ticks:{color:tick,font:{size:9,family:'Vazirmatn'}}},
            y:{grid:{color:grid},border:{display:false},ticks:{color:tick,font:{size:9,family:'Vazirmatn'},callback:v=>v+' MB'}}
          }
        }
      });
    }

    if(el2){
      const cardBg=(getComputedStyle(document.documentElement).getPropertyValue('--card')||'#FFFFFF').trim()||'#FFFFFF';
      ch2=new Chart(el2,{
        type:'doughnut',
        data:{labels:['VLESS WS','Trojan WS','XHTTP','Shadowsocks','MTProto'],datasets:[{
          data:[1,1,1,1,1],
          backgroundColor:['#2563EB','#16A34A','#0EA5E9','#D97706','#94A3B8'],
          borderColor:cardBg,
          borderWidth:3,hoverOffset:6,borderRadius:6,spacing:2
        }]},
        options:{
          responsive:true,maintainAspectRatio:false,cutout:'72%',
          plugins:{
            legend:{position:'bottom',labels:{color:'#6B7280',font:{size:10,family:'Vazirmatn'},padding:12,usePointStyle:true,pointStyle:'circle'}},
            tooltip:{backgroundColor:tipBg,borderColor:'rgba(37,99,235,.15)',borderWidth:1,padding:10,cornerRadius:10}
          }
        }
      });
    }
  }catch(e){
    console.error('initCharts',e);
    setupFallbackCharts();
  }
}
const ICON_MAP={ad:'ti-speakerphone',news:'ti-news',warning:'ti-alert-triangle',urgent:'ti-alert-octagon'};
const LABEL_MAP={ad:'تبلیغ',news:'خبر',warning:'هشدار',urgent:'فوری'};
async function loadAnnouncements(){
  try{
    const r=await authF('/api/announcements'),d=await r.json();
    const seen=JSON.parse(localStorage.getItem('oxnet-seen-ann')||'[]');
    const list=(d.announcements||[]).filter(a=>!seen.includes(a.id));
    document.getElementById('ann-banner-wrap').innerHTML=list.map(a=>`
      <div class="ann-card ${a.type}" id="ann-${a.id}">
        <button class="ann-close" onclick="dismissAnn('${a.id}')"><i class="ti ti-x"></i></button>
        <div class="ann-icon"><i class="ti ${ICON_MAP[a.type]||'ti-bell'}"></i></div>
        <div class="ann-body">
          <div class="ann-title">${esc(a.title)} <span style="font-size:9px;color:var(--t3)">· ${LABEL_MAP[a.type]||''}</span></div>
          <div class="ann-text">${esc(a.body)}</div>
          ${a.image_url?`<img class="ann-img" src="${esc(a.image_url)}">`:''}
        </div>
      </div>`).join('');
      if (list.length) {
      authF('/api/announcements/view', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ids: list.map(a => a.id) })
      }).catch(() => {});
    }
  }catch(e){}
}
function dismissAnn(id){
  const seen=JSON.parse(localStorage.getItem('oxnet-seen-ann')||'[]');
  seen.push(id);localStorage.setItem('oxnet-seen-ann',JSON.stringify(seen));
  document.getElementById('ann-'+id)?.remove();
}
let lastSupportMsgId = null;
 
function fmtSupTime(ts){
  const d = new Date(ts);
  return d.toLocaleTimeString('fa-IR',{hour:'2-digit',minute:'2-digit'});
}
function fmtSupDate(ts){
  const d = new Date(ts);
  const today = new Date();
  const isToday = d.toDateString() === today.toDateString();
  if (isToday) return 'امروز';
  const y = new Date(today); y.setDate(y.getDate()-1);
  if (d.toDateString() === y.toDateString()) return 'دیروز';
  return d.toLocaleDateString('fa-IR');
}
 
async function loadSupportMsgs() {
  try {
    const r = await authF('/api/support/messages'),
      d = await r.json();
    const msgs = d.messages || [];
    const blocked = !!d.blocked;
    const el = document.getElementById('support-msgs');

    if (el) {
      if (!msgs.length) {
        el.innerHTML =
          '<div class="sup-empty"><i class="ti ti-message-circle-2"></i><b>هنوز گفتگویی نیست</b><span>این بخش در نسخه مستقل حذف شده است</span></div>';
      } else {
        let html = '',
          lastDate = '';
        msgs.forEach((m, idx) => {
          const dateLabel = fmtSupDate(m.created_at);
          if (dateLabel !== lastDate) {
            html +=
              '<div class="sup-date-sep"><span>' + dateLabel + '</span></div>';
            lastDate = dateLabel;
          }
          const isLastClientMsg =
            m.sender === 'client' && idx === msgs.length - 1; // not used, but kept
          const seenTick =
            m.sender === 'client'
              ? m.read_by_admin
                ? '<i class="ti ti-checks seen"></i>'
                : '<i class="ti ti-check"></i>'
              : '';
          //  Fixed: removed backslashes before backticks
          html += `
            <div class="sup-msg-row ${m.sender}">
              <div class="sup-msg ${m.sender}">
                ${esc(m.body)}
                <span class="sup-time">${fmtSupTime(m.created_at)} ${seenTick}</span>
              </div>
              <div class="sup-avatar ${m.sender}"><i class="ti ${m.sender === 'admin' ? 'ti-headset' : 'ti-user'}"></i></div>
            </div>`;
        });
        el.innerHTML = html;
      }
      const shouldScroll =
        !lastSupportMsgId ||
        (msgs.length && msgs[msgs.length - 1].id !== lastSupportMsgId);
      if (shouldScroll) el.scrollTop = el.scrollHeight;
      if (msgs.length) lastSupportMsgId = msgs[msgs.length - 1].id;
    }

    const banner = document.getElementById('sup-blocked-banner');
    const inputRow = document.getElementById('sup-input-row');
    if (banner) banner.style.display = blocked ? 'flex' : 'none';
    if (inputRow) inputRow.classList.toggle('disabled', blocked);

    const nb = document.getElementById('support-nb');
    if (nb) {
      const lastAdmin = [...msgs].reverse().find((m) => m.sender === 'admin');
      const seenId = localStorage.getItem('oxnet-last-seen-support-msg');
      const onSupportPage = document
        .getElementById('pg-support')
        .classList.contains('on');
      const hasNew = lastAdmin && lastAdmin.id !== seenId && !onSupportPage;
      nb.style.display = hasNew ? 'inline-flex' : 'none';
      if (lastAdmin && onSupportPage)
        localStorage.setItem('oxnet-last-seen-support-msg', lastAdmin.id);
    }
  } catch (e) {
    // silent fail
  }
}
 
async function sendSupportMsg(){
  const inp=document.getElementById('support-inp');const msg=inp.value.trim();if(!msg)return;
  inp.disabled = true;
  try{
    const r=await authF('/api/support/send',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg})});
    if(r.status===403){toast('این بخش حذف شده است','err');loadSupportMsgs();inp.disabled=false;return}
    if(!r.ok)throw new Error();
    inp.value='';loadSupportMsgs();
  }catch(e){toast('خطا در ارسال پیام','err')}
  inp.disabled = false;
  inp.focus();
}
document.addEventListener('DOMContentLoaded', async () => {
  await checkAuth();
  initCharts();
  updateGreeting();
  loadPanelDomain();
  document.getElementById('sub-all-url') && (document.getElementById('sub-all-url').textContent = location.protocol + '//' + location.host + '/sub-all');
  
  // ابتدا نسخه را بررسی کن
  // بروزرسانی خودکار در نسخه مستقل حذف شده است

  // بقیه‌ی کدهای اولیه
  fetchStats();
  fetchDefaultVless();
  loadLinks();
  loadSubs();
  loadAnnouncements();
  loadDbStatus();
  renderThemeSwatches();
  // بخش مرکزی حذف شده است

  setInterval(fetchStats, 2000);
  setInterval(() => {
    if (document.getElementById('pg-links').classList.contains('on')) loadLinks();
    if (document.getElementById('pg-subgroups').classList.contains('on')) loadSubs();
    if (document.getElementById('pg-subscriptions').classList.contains('on')) loadSubsPage();
    if (document.getElementById('pg-connections').classList.contains('on')) loadConns();
    if (document.getElementById('pg-logs').classList.contains('on')) loadActivity();
    if (document.getElementById('pg-support').classList.contains('on')) loadSupportMsgs();
    // بروزرسانی خودکار حذف شده است
  }, 5000);
  setInterval(loadAnnouncements, 3000);
});

function timeAgoFa(ts){
  const diff = Math.max(0, (Date.now()/1000) - ts);
  if(diff < 60) return 'همین الان';
  if(diff < 3600) return toFa(Math.floor(diff/60))+' دقیقه پیش';
  if(diff < 86400) return toFa(Math.floor(diff/3600))+' ساعت پیش';
  if(diff < 2592000) return toFa(Math.floor(diff/86400))+' روز پیش';
  return new Date(ts*1000).toLocaleDateString('fa-IR');
}

async function loadVersion(){
  try{
    const r=await authF('/api/version'), d=await r.json();
    const cur=d.current||{}, lat=d.latest||{};

    document.getElementById('ver-current').textContent=cur.version||'—';
    document.getElementById('ver-current-desc').textContent=cur.description||'بدون توضیحات ثبت‌شده برای این نسخه';
    document.getElementById('ver-repo').textContent=d.repo||'تنظیم نشده';
    document.getElementById('ver-branch').textContent=d.branch||'—';

    const badge=document.getElementById('ver-status-badge'), nb=document.getElementById('update-nb');
    const latestCard=document.getElementById('upd-latest-card');

    if(lat.error){
      badge.innerHTML='<span class="upd-pill upd-pill-amber"><i class="ti ti-alert-triangle"></i> '+esc(lat.error)+'</span>';
      latestCard.style.display='none';
      nb.style.display='none';
      updateAvailable = false;
    } else if(d.update_available){
      badge.innerHTML='<span class="upd-pill upd-pill-amber"><span class="upd-dot"></span> بروزرسانی جدید موجود است</span>';
      document.getElementById('ver-latest-num').textContent=lat.version||'—';
      document.getElementById('ver-latest-desc').textContent=lat.description||'بدون توضیحات';
      latestCard.style.display='flex';
      nb.style.display='inline-flex';
      nb.textContent='1';
      // تنظیم متغیرهای سراسری برای مودال
      updateAvailable = true;
      updateVersion = lat.version || '—';
      updateDescription = lat.description || 'بدون توضیحات';
    } else {
      badge.innerHTML='<span class="upd-pill upd-pill-green"><i class="ti ti-circle-check"></i> پنل بروز است</span>';
      latestCard.style.display='none';
      nb.style.display='none';
      updateAvailable = false;
    }
  } catch(e) {
    console.error(e);
    updateAvailable = false;
  }
  loadUpdateHistory();
}

let updatePolling=null, pollTicks=0;
async function startUpdate(){
  if(!confirm('نصب بروزرسانی سرور را چند ثانیه ری‌استارت می‌کند. ادامه می‌دهید؟'))return;
  const btn=document.getElementById('update-btn');
  btn.disabled=true;btn.innerHTML='<i class="ti ti-loader-2" style="animation:spin 1s linear infinite"></i> در حال نصب...';
  document.getElementById('update-progress-wrap').style.display='block';
  pollTicks=0;
  try{
    await authF('/api/update',{method:'POST'});
    toast('بروزرسانی شروع شد','ok');
    updatePolling=setInterval(pollUpdate,900);
  }catch(e){
    toast('خطا در شروع بروزرسانی','err');
    btn.disabled=false;btn.innerHTML='<i class="ti ti-download"></i> نصب بروزرسانی';
  }
}
</script>
</body></html>"""


def get_public_page_html(uuid_key: str) -> str:
    """صفحه پابلیک ساب — طراحی آرام و مدرن (بدون نئون)"""
    html = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>اشتراک · OXNET</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#F8FAFC; --card:#FFFFFF; --ink:#111827; --muted:#6B7280;
  --line:#E5E7EB; --accent:#2563EB; --accent-soft:rgba(37,99,235,.12);
  --ok:#16A34A; --ok-bg:rgba(22,163,74,.12); --err:#DC2626; --err-bg:rgba(220,38,38,.12);
  --shadow:0 12px 32px rgba(15,23,42,.06); --radius:16px;
  --font:"Vazirmatn", system-ui, -apple-system, "Segoe UI", Tahoma, sans-serif;
}
@media (prefers-color-scheme: dark){
  :root{
    --bg:#0F172A; --card:#1E293B; --ink:#F8FAFC; --muted:#CBD5E1;
    --line:#334155; --accent:#3B82F6; --accent-soft:rgba(59,130,246,.15);
    --ok:#22C55E; --ok-bg:rgba(34,197,94,.14); --err:#EF4444; --err-bg:rgba(239,68,68,.14);
    --shadow:0 16px 40px rgba(0,0,0,.45);
  }
}
html{font-size:15px;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;text-rendering:optimizeLegibility}
body{
  font-family:var(--font);background:var(--bg);color:var(--ink);
  min-height:100vh;padding:28px 16px 48px;line-height:1.65;font-weight:400;
  background-image:
    radial-gradient(900px 420px at 10% 0%, rgba(37,99,235,.06), transparent 55%),
    radial-gradient(700px 380px at 100% 100%, rgba(5,150,105,.05), transparent 50%);
}
.shell{max-width:720px;margin:0 auto}
.top{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:22px;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:12px}
.brand-mark{width:42px;height:42px;border-radius:13px;display:flex;align-items:center;justify-content:center;background:var(--accent);color:#fff;font-size:18px}
.brand-name{font-weight:700;font-size:1.05rem;letter-spacing:-.02em}
.brand-sub{font-size:.78rem;color:var(--muted);margin-top:2px;font-weight:500}
.pill{font-size:.72rem;font-weight:600;color:var(--muted);background:var(--card);border:1px solid var(--line);border-radius:999px;padding:7px 12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:22px;margin-bottom:14px}
.sub-eyebrow{font-size:.72rem;font-weight:600;color:var(--muted);letter-spacing:.06em;text-transform:uppercase;margin-bottom:6px;display:flex;align-items:center;gap:6px}
.sub-name{font-size:1.55rem;font-weight:700;letter-spacing:-.03em;margin-bottom:6px;line-height:1.35}
.sub-desc{font-size:.9rem;color:var(--muted);line-height:1.75;margin-bottom:10px;font-weight:400}
.sub-meta-row{font-size:.78rem;color:var(--muted);display:flex;align-items:center;gap:6px;margin-bottom:14px;font-weight:500}
.sub-sub-box{display:flex;align-items:center;gap:8px;flex-wrap:wrap;background:var(--accent-soft);border:1px solid var(--line);border-radius:14px;padding:10px 12px}
.sub-sub-url{flex:1;min-width:160px;font-size:.8rem;color:var(--muted);direction:ltr;text-align:left;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-weight:500}
.btn{border:none;border-radius:12px;padding:9px 14px;font-family:inherit;font-size:.8rem;font-weight:600;cursor:pointer;display:inline-flex;align-items:center;gap:6px;transition:transform .15s, opacity .15s;letter-spacing:-.01em}
.btn:hover{transform:translateY(-1px)}
.btn-pur{background:var(--accent);color:#faf7f2}
.btn-g{background:transparent;border:1px solid var(--line);color:var(--ink)}
.copy-all-bar{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;background:var(--card);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:16px 18px;margin-bottom:12px}
.copy-all-title{font-size:.9rem;font-weight:700;display:flex;align-items:center;gap:6px;letter-spacing:-.015em}
.copy-all-sub{font-size:.75rem;color:var(--muted);margin-top:3px;font-weight:500}
.copy-all-btn{background:var(--accent);color:#faf7f2;border:none;border-radius:12px;padding:10px 16px;font-family:inherit;font-size:.8rem;font-weight:600;cursor:pointer;display:inline-flex;align-items:center;gap:6px}
.stats-bar{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:14px 0}
.stat-card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:14px;box-shadow:var(--shadow)}
.stat-label{font-size:.72rem;color:var(--muted);font-weight:600}
.stat-val{font-size:1.35rem;font-weight:700;letter-spacing:-.03em;margin-top:4px;line-height:1.2}
.stat-sub{font-size:.72rem;color:var(--muted);margin-top:4px;font-weight:500}
.cfg-title{font-size:.75rem;font-weight:700;color:var(--muted);margin:18px 0 10px;display:flex;align-items:center;gap:6px;letter-spacing:.04em;text-transform:uppercase}
.cfg-grid{display:grid;gap:12px}
.cfg-card{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden;box-shadow:var(--shadow)}
.cfg-top{padding:16px 16px 12px;position:relative}
.cfg-top::after{content:'';position:absolute;top:0;right:0;width:3px;height:100%;background:var(--ok)}
.cfg-card.inactive .cfg-top::after{background:var(--err)}
.cfg-head{display:flex;justify-content:space-between;gap:8px;align-items:flex-start;flex-wrap:wrap;margin-bottom:10px}
.cfg-label{font-size:.95rem;font-weight:700;letter-spacing:-.02em}
.cfg-badges{display:flex;gap:5px;flex-wrap:wrap;margin-top:6px}
.proto-chip{font-size:.68rem;padding:3px 8px;border-radius:999px;font-weight:600;background:var(--accent-soft);color:var(--accent)}
.cfg-status{font-size:.68rem;font-weight:600;padding:4px 10px;border-radius:999px}
.cfg-status.ok{background:var(--ok-bg);color:var(--ok)}
.cfg-status.no{background:var(--err-bg);color:var(--err)}
.ubar{height:6px;border-radius:99px;background:rgba(28,25,23,.06);overflow:hidden;margin-bottom:5px}
.ubar-f{height:100%;border-radius:99px;background:var(--accent)}
.utxt{font-size:.72rem;color:var(--muted);display:flex;justify-content:space-between;font-weight:500}
.cfg-actions{display:flex;gap:8px;flex-wrap:wrap;padding:0 16px 16px}
.foot{text-align:center;margin-top:22px;font-size:.75rem;color:var(--muted);font-weight:500}
.lock-wrap{max-width:420px;margin:12vh auto 0;text-align:center}
.lock-wrap h1{font-size:1.5rem;font-weight:700;margin:14px 0 8px;letter-spacing:-.03em}
.lock-wrap p{color:var(--muted);font-size:.9rem;line-height:1.75;margin-bottom:18px}
.lock-wrap input{width:100%;height:48px;border-radius:12px;border:1px solid var(--line);background:var(--card);padding:0 14px;font-family:inherit;font-size:.92rem;color:var(--ink);margin-bottom:10px;outline:none}
.lock-wrap input:focus{box-shadow:0 0 0 4px var(--accent-soft);border-color:rgba(37,99,235,.35)}
.toast{position:fixed;bottom:22px;left:50%;transform:translateX(-50%) translateY(20px);background:var(--ink);color:#fff;padding:10px 16px;border-radius:999px;font-size:.82rem;font-weight:600;opacity:0;pointer-events:none;transition:.25s;z-index:50}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.qr-modal{position:fixed;inset:0;background:rgba(15,23,42,.5);display:none;align-items:center;justify-content:center;z-index:60;padding:20px}
.qr-modal.on{display:flex}
.qr-box{background:var(--card);border-radius:20px;padding:22px;width:min(340px,100%);text-align:center;border:1px solid var(--line)}
.qr-box h3{margin-bottom:12px;font-size:1rem;font-weight:700}
.dot{width:7px;height:7px;border-radius:50%;background:var(--ok);display:inline-block}
.empty{text-align:center;padding:40px 16px;color:var(--muted);font-weight:500}
@media(max-width:640px){.stats-bar{grid-template-columns:1fr} body{padding:18px 12px 36px} .sub-name{font-size:1.3rem}}
</style>
</head>
<body>
<div class="qr-modal" id="qr-modal" onclick="if(event.target===this)this.classList.remove('on')">
  <div class="qr-box">
    <h3 id="qr-title">QR Code</h3>
    <div id="qr-box"></div>
    <button class="btn btn-g" style="margin-top:14px" onclick="document.getElementById('qr-modal').classList.remove('on')">بستن</button>
  </div>
</div>
<div class="shell">
  <div class="top">
    <div class="brand">
      <div class="brand-mark"><i class="ti ti-network"></i></div>
      <div>
        <div class="brand-name">OXNET</div>
        <div class="brand-sub">OXNET Stable · v2.0.10</div>
      </div>
    </div>
    <div class="pill" id="live-pill">در حال بارگذاری</div>
  </div>
  <div id="root"><div class="empty">در حال بارگذاری...</div></div>
  <div class="foot">OXNET v2.0.10</div>
</div>
<div class="toast" id="toast"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
<script>
const UUID_KEY = "__UUID_KEY__";
const PW_KEY = "oxnet_pw_" + UUID_KEY;
function esc(s){return String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[m]);}
function toFa(n){return String(n).replace(/\d/g,d=>'۰۱۲۳۴۵۶۷۸۹'[d]);}
function toast(msg){
  const t=document.getElementById('toast'); t.textContent=msg; t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'),2200);
}
function showQR(title, text){
  document.getElementById('qr-title').textContent = title || 'QR';
  const box=document.getElementById('qr-box'); box.innerHTML='';
  try{ new QRCode(box, {text, width:180, height:180, correctLevel: QRCode.CorrectLevel.M}); }catch(e){}
  document.getElementById('qr-modal').classList.add('on');
}
function copyAllConfigs(){
  const lines=(window._oxnetLinks||[]).filter(l=>l.vless).map(l=>l.vless);
  if(!lines.length){toast('کانفیگ فعالی نیست');return;}
  navigator.clipboard.writeText(lines.join('\n')).then(()=>toast('همه کانفیگ‌ها کپی شد'));
}
function renderLocked(name){
  document.getElementById('live-pill').textContent = 'محافظت‌شده';
  document.getElementById('root').innerHTML = `
    <div class="card lock-wrap">
      <div class="brand-mark" style="margin:0 auto"><i class="ti ti-lock"></i></div>
      <h1>${esc(name||'گروه خصوصی')}</h1>
      <p>برای مشاهده کانفیگ‌ها و لینک اشتراک، رمز صفحه را وارد کنید.</p>
      <input id="pw" type="password" placeholder="رمز صفحه عمومی" autofocus>
      <button class="btn btn-pur" style="width:100%;justify-content:center;height:46px" onclick="unlock()"><i class="ti ti-login-2"></i> ورود</button>
    </div>`;
  document.getElementById('pw')?.addEventListener('keydown', e=>{ if(e.key==='Enter') unlock(); });
}
async function unlock(){
  const pw = document.getElementById('pw')?.value || '';
  localStorage.setItem(PW_KEY, pw);
  await load();
}
async function load(){
  const savedPw = localStorage.getItem(PW_KEY) || '';
  const url = '/api/public/sub/' + UUID_KEY + (savedPw ? ('?pw=' + encodeURIComponent(savedPw)) : '');
  try{
    const r = await fetch(url);
    const d = await r.json();
    if(d.locked){ renderLocked(d.name); return; }
    document.getElementById('live-pill').innerHTML = '<span class="dot"></span>&nbsp; آنلاین';
    const activeCount = (d.links||[]).filter(l=>l.active).length;
    const baseSubUrl = d.sub_url || (window.location.protocol + '//' + window.location.host + '/sub-group/' + UUID_KEY);
    const subUrl = baseSubUrl + (savedPw ? '?pw=' + encodeURIComponent(savedPw) : '');
    window._oxnetSubUrl = subUrl;
    window._oxnetSubName = d.name;
    window._oxnetLinks = (d.links||[]).map(l => ({
      vless: l.vless_link, sub: (l.sub_url||'') + (savedPw ? '?pw=' + encodeURIComponent(savedPw) : ''), label: l.label
    }));
    window._oxnetCfSubs = (d.cloudflare_subs||[]).map(c => ({...c, sub_url: c.sub_url + (savedPw ? '?pw=' + encodeURIComponent(savedPw) : '')}));
    const ds = d.domain_subs || {};
    window._oxnetMainSubUrl = (ds.main_sub_url || '') + (savedPw ? '?pw=' + encodeURIComponent(savedPw) : '');
    window._oxnetExtraSubs = (ds.extra_subs||[]).map(c => ({...c, sub_url: c.sub_url + (savedPw ? '?pw=' + encodeURIComponent(savedPw) : '')}));

    document.getElementById('root').innerHTML = `
      <div class="card">
        <div class="sub-eyebrow"><i class="ti ti-folders"></i> گروه دسترسی</div>
        <div class="sub-name">${esc(d.name)}</div>
        ${d.desc ? `<div class="sub-desc">${esc(d.desc)}</div>` : ''}
        <div class="sub-meta-row"><i class="ti ti-clock"></i> آخرین بروزرسانی: ${new Date().toLocaleTimeString('fa-IR')}</div>
        <div class="sub-sub-box">
          <span class="sub-sub-url">${esc(subUrl)}</span>
          <button class="btn btn-pur" onclick="navigator.clipboard.writeText(window._oxnetSubUrl).then(()=>toast('لینک ساب کپی شد'))"><i class="ti ti-copy"></i> کپی لینک ساب</button>
          <button class="btn btn-g" onclick="showQR(window._oxnetSubName + ' — کل گروه', window._oxnetSubUrl)"><i class="ti ti-qrcode"></i> QR</button>
        </div>
        <div style="margin-top:10px;font-size:12px;color:var(--muted);line-height:1.7"><i class="ti ti-info-circle"></i> ساب اصلی شامل کانفیگ‌های <b>همه دامنه‌ها</b> است.</div>
      </div>

      ${(d.domain_subs && d.domain_subs.main_sub_url) ? `<div class="copy-all-bar"><div class="copy-all-text"><div class="copy-all-title"><i class="ti ti-world"></i> ساب دامنه اصلی</div><div class="copy-all-sub">فقط دامنه اصلی پنل · ${esc((d.domain_subs||{}).main_domain||'')}</div></div><button class="copy-all-btn" onclick="navigator.clipboard.writeText(window._oxnetMainSubUrl).then(()=>toast('ساب دامنه اصلی کپی شد'))"><i class="ti ti-world"></i> دامنه اصلی</button></div>` : ''}

      ${((d.domain_subs||{}).extra_subs||[]).length ? `<div class="copy-all-bar"><div class="copy-all-text"><div class="copy-all-title"><i class="ti ti-link"></i> ساب‌های دامنه فرعی</div><div class="copy-all-sub">هر دامنه فرعی به‌صورت جدا</div></div><div style="display:flex;gap:8px;flex-wrap:wrap">${window._oxnetExtraSubs.map(c=>`<button class="copy-all-btn" onclick="navigator.clipboard.writeText('${esc(c.sub_url)}').then(()=>toast('ساب دامنه فرعی کپی شد'))"><i class="ti ti-link"></i> ${esc(c.domain)}</button>`).join('')}</div></div>` : ''}

      ${(d.cloudflare_subs||[]).length ? `<div class="copy-all-bar"><div class="copy-all-text"><div class="copy-all-title"><i class="ti ti-cloud"></i> ساب‌های Cloudflare</div><div class="copy-all-sub">Host/SNI دامنه Cloudflare و IP تمیز</div></div><div style="display:flex;gap:8px;flex-wrap:wrap">${window._oxnetCfSubs.map(c=>`<button class="copy-all-btn" onclick="navigator.clipboard.writeText('${esc(c.sub_url)}').then(()=>toast('ساب کلادفلیر کپی شد'))"><i class="ti ti-cloud"></i> ${esc(c.domain)} · ${toFa(c.clean_ip_count||0)} IP</button>`).join('')}</div></div>` : ''}

      <div class="copy-all-bar">
        <div class="copy-all-text">
          <div class="copy-all-title"><i class="ti ti-copy"></i> کپی همه کانفیگ‌ها</div>
          <div class="copy-all-sub">لینک‌های فعال این گروه</div>
        </div>
        <button class="copy-all-btn" onclick="copyAllConfigs()"><i class="ti ti-clipboard-copy"></i> کپی همه (${toFa(activeCount)})</button>
      </div>

      <div class="stats-bar">
        <div class="stat-card"><div class="stat-label">کانفیگ فعال</div><div class="stat-val">${toFa(activeCount)}</div><div class="stat-sub">از ${toFa((d.links||[]).length)} کانفیگ</div></div>
        <div class="stat-card"><div class="stat-label">اتصالات زنده</div><div class="stat-val">${toFa(d.active_connections||0)}</div><div class="stat-sub" style="display:flex;align-items:center;gap:5px"><span class="dot"></span> آنلاین</div></div>
        <div class="stat-card"><div class="stat-label">کل مصرف</div><div class="stat-val" style="font-size:1.05rem">${esc(d.total_used_fmt||'0 B')}</div></div>
      </div>

      <div class="cfg-title"><i class="ti ti-list-details"></i> کانفیگ‌ها</div>
      <div class="cfg-grid">
        ${(d.links||[]).map(l=>{
          const lim = l.limit_bytes||0; const used=l.used_bytes||0;
          const pct = lim>0 ? Math.min(100, Math.round(used/lim*100)) : 0;
          return `<div class="cfg-card ${l.active?'':'inactive'}">
            <div class="cfg-top">
              <div class="cfg-head">
                <div>
                  <div class="cfg-label">${esc(l.label)}</div>
                  <div class="cfg-badges"><span class="proto-chip">${esc(l.protocol||'')}</span></div>
                </div>
                <div class="cfg-status ${l.active?'ok':'no'}">${l.active?'فعال':'غیرفعال'}</div>
              </div>
              <div class="ubar"><div class="ubar-f" style="width:${pct}%"></div></div>
              <div class="utxt"><span>${esc(l.used_fmt||'0 B')}</span><span>${esc(l.limit_fmt||'∞')}</span></div>
            </div>
            <div class="cfg-actions">
              <button class="btn btn-pur" onclick="navigator.clipboard.writeText('${esc(l.vless_link||'')}').then(()=>toast('لینک کانفیگ کپی شد'))"><i class="ti ti-copy"></i> کپی</button>
              <button class="btn btn-g" onclick="showQR('${esc(l.label)}','${esc(l.vless_link||'')}')"><i class="ti ti-qrcode"></i> QR</button>
              <button class="btn btn-g" onclick="navigator.clipboard.writeText('${esc((l.sub_url||'') + (savedPw ? ('?pw=' + encodeURIComponent(savedPw)) : ''))}').then(()=>toast('ساب تکی کپی شد'))"><i class="ti ti-rss"></i> ساب</button>
            </div>
          </div>`;
        }).join('') || '<div class="empty">کانفیگی در این گروه نیست</div>'}
      </div>`;
  }catch(e){
    document.getElementById('root').innerHTML = '<div class="empty">خطا در بارگذاری</div>';
  }
}
load();
</script>
</body></html>"""
    return html.replace("__UUID_KEY__", str(uuid_key))
