# pages.py - پنل عقاب نسخه کامل با انتخاب آی‌پی تمیز

LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🦅 ورود · پنل عقاب</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
@keyframes fireBG{0%{background-position:0% 50%}25%{background-position:50% 0%}50%{background-position:100% 50%}75%{background-position:50% 100%}100%{background-position:0% 50%}}
@keyframes flameFlicker{0%{opacity:0.6;transform:scale(1)}50%{opacity:1;transform:scale(1.02)}100%{opacity:0.6;transform:scale(1)}}
html,body{height:100%;overflow:hidden}
body{font-family:'Vazirmatn',sans-serif;background:linear-gradient(135deg,#0a0a0f,#1a0a0a,#0a0a1a);background-size:400% 400%;animation:fireBG 8s ease infinite;display:flex;align-items:center;justify-content:center;padding:20px;color:#F0EEFF}
.fire-particles{position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden}
.fire-particle{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(255,120,50,0.3),rgba(255,50,0,0));width:6px;height:6px;animation:floatFire 12s ease-in-out infinite}
@keyframes floatFire{0%{transform:translateY(100vh) scale(0) rotate(0deg);opacity:0}20%{opacity:1}80%{opacity:1}100%{transform:translateY(-10vh) scale(1.5) rotate(720deg);opacity:0}}
.glow-orb{position:fixed;border-radius:50%;filter:blur(150px);z-index:0;animation:flameFlicker 3s ease-in-out infinite;pointer-events:none}
.orb1{width:500px;height:500px;background:rgba(255,80,20,0.05);top:-200px;right:-100px}
.orb2{width:400px;height:400px;background:rgba(255,150,50,0.04);bottom:-100px;left:-80px;animation-delay:2s}
.wrap{position:relative;z-index:10;width:100%;max-width:420px}
.card{background:rgba(20,10,10,0.85);backdrop-filter:blur(30px);border:1px solid rgba(255,100,50,0.15);border-radius:28px;padding:44px 38px 38px;box-shadow:0 0 100px rgba(255,80,20,0.04),0 25px 70px rgba(0,0,0,0.6);animation:cardIn 0.6s ease}
@keyframes cardIn{from{opacity:0;transform:translateY(30px) scale(0.96)}to{opacity:1;transform:translateY(0) scale(1)}}
.brand{display:flex;align-items:center;gap:16px;margin-bottom:30px}
.brand-icon{width:56px;height:56px;border-radius:16px;background:linear-gradient(135deg,#FF6B35,#FF4500);display:flex;align-items:center;justify-content:center;font-size:28px;flex-shrink:0;box-shadow:0 0 60px rgba(255,80,20,0.15)}
.brand-name{font-size:20px;font-weight:800;background:linear-gradient(135deg,#FF8C00,#FF4500,#FF6B35);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.brand-sub{font-size:11px;color:#8A4A3A;margin-top:2px}
h1{font-size:22px;font-weight:800;color:#F0EEFF;margin-bottom:6px}
.sub{font-size:12.5px;color:#A06040;margin-bottom:26px;line-height:1.7}
.hint{display:flex;align-items:center;gap:10px;background:rgba(255,80,20,0.06);border:1px solid rgba(255,80,20,0.12);border-radius:12px;padding:10px 16px;margin-bottom:22px}
.hint-label{font-size:11px;color:#8A4A3A;flex:1}
.hint-val{font-family:ui-monospace,monospace;font-size:14px;font-weight:700;color:#FF8C00;background:rgba(255,80,20,0.1);border:1px solid rgba(255,80,20,0.2);padding:3px 13px;border-radius:8px;cursor:pointer}
.field{margin-bottom:20px}
.field label{display:block;font-size:10.5px;font-weight:600;color:#A06040;margin-bottom:8px;text-transform:uppercase;letter-spacing:.08em}
.inp-wrap{position:relative}
input[type=password]{width:100%;padding:14px 48px 14px 18px;border-radius:12px;border:1px solid rgba(255,100,50,0.15);background:rgba(0,0,0,.3);color:#F0EEFF;font-family:inherit;font-size:14px;outline:none;transition:.3s}
input[type=password]:focus{border-color:rgba(255,100,50,.5);background:rgba(0,0,0,.4);box-shadow:0 0 0 4px rgba(255,80,20,.06)}
.ic{position:absolute;left:16px;top:50%;transform:translateY(-50%);color:#8A4A3A;font-size:18px}
input:focus+.ic{color:#FF8C00}
.err{display:none;background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.2);border-radius:10px;padding:10px 14px;margin-bottom:14px;font-size:12px;color:#F87171;align-items:center;gap:8px}
.err.show{display:flex}
.btn{width:100%;padding:14px;border-radius:12px;border:none;cursor:pointer;background:linear-gradient(135deg,#FF6B35,#FF4500,#FF8C00);background-size:200% 200%;animation:btnFire 3s ease infinite;color:#fff;font-family:inherit;font-size:14px;font-weight:700;display:flex;align-items:center;justify-content:center;gap:10px;box-shadow:0 4px 30px rgba(255,80,20,.25);transition:all .3s}
@keyframes btnFire{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
.btn:hover{transform:translateY(-2px);box-shadow:0 8px 40px rgba(255,80,20,.35)}
.btn:disabled{opacity:.5;cursor:not-allowed}
.footer{margin-top:24px;padding-top:20px;border-top:1px solid rgba(255,100,50,0.08);text-align:center;font-size:11px;color:#8A4A3A}
@keyframes spin{to{transform:rotate(360deg)}}
</style>
</head>
<body>
<div class="fire-particles">
    <div class="fire-particle" style="left:5%;animation-delay:0s;width:8px;height:8px"></div>
    <div class="fire-particle" style="left:15%;animation-delay:2s;width:5px;height:5px"></div>
    <div class="fire-particle" style="left:25%;animation-delay:4s;width:10px;height:10px"></div>
    <div class="fire-particle" style="left:35%;animation-delay:1s;width:6px;height:6px"></div>
    <div class="fire-particle" style="left:45%;animation-delay:5s;width:7px;height:7px"></div>
    <div class="fire-particle" style="left:55%;animation-delay:3s;width:9px;height:9px"></div>
    <div class="fire-particle" style="left:65%;animation-delay:6s;width:5px;height:5px"></div>
    <div class="fire-particle" style="left:75%;animation-delay:2s;width:8px;height:8px"></div>
    <div class="fire-particle" style="left:85%;animation-delay:4s;width:6px;height:6px"></div>
    <div class="fire-particle" style="left:95%;animation-delay:7s;width:7px;height:7px"></div>
</div>
<div class="glow-orb orb1"></div><div class="glow-orb orb2"></div>
<div class="wrap">
  <div class="card">
    <div class="brand"><div class="brand-icon">🦅</div><div><div class="brand-name">پنل عقاب</div><div class="brand-sub">مدیریت کاربران</div></div></div>
    <h1>ورود به پنل عقاب</h1>
    <p class="sub">رمز عبور را برای دسترسی به داشبورد وارد کنید</p>
    <div class="err" id="err"><i class="ti ti-alert-circle"></i><span id="err-text"></span></div>
    <div class="hint"><span class="hint-label">رمز پیش‌فرض</span><span class="hint-val" onclick="document.getElementById('pw').value='123456';document.getElementById('pw').focus()">123456</span></div>
    <form id="form">
      <div class="field"><label>رمز عبور</label><div class="inp-wrap"><input type="password" id="pw" placeholder="رمز عبور را وارد کنید" autofocus required><i class="ti ti-lock ic"></i></div></div>
      <button class="btn" type="submit" id="btn"><i class="ti ti-login-2"></i> ورود به پنل</button>
    </form>
    <div class="footer">🦅 پنل عقاب · v10.0</div>
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
    location.href='/dashboard';
  }catch(e){
    et.textContent=e.message;err.classList.add('show');
    btn.disabled=false;btn.innerHTML='<i class="ti ti-login-2"></i> ورود به پنل';
  }
});
</script>
</body></html>"""

# ===== ادامه DASHBOARD_HTML =====

# به دلیل حجم بالا، DASHBOARD_HTML رو در فایل جداگانه در پاسخ بعدی میدم
# یا میتونی از نسخه قبلی استفاده کنی با تغییرات زیر:

# 1. "خانم" رو به "خانه" تغییر بده
# 2. بخش اسکن رو حذف کن
# 3. توی مودال ساخت کاربر، بخش انتخاب آی‌پی تمیز رو اضافه کن

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🦅 پنل عقاب · خانه</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#0a0a0f;--bg2:#12122a;--bg3:#1a1a3a;
  --card:rgba(15,15,30,0.7);--card-b:rgba(255,255,255,0.05);--card-bh:rgba(255,255,255,0.1);
  --accent:#FF6B35;--accent2:#FF8C00;--accent-d:rgba(255,80,20,0.08);
  --green:#10B981;--green-bg:rgba(16,185,129,0.08);--green-t:#34D399;
  --red:#EF4444;--red-bg:rgba(239,68,68,0.08);--red-t:#F87171;
  --amber:#F59E0B;--amber-bg:rgba(245,158,11,0.08);--amber-t:#FCD34D;
  --blue:#3B82F6;--blue-bg:rgba(59,130,246,0.08);
  --t1:#F0EEFF;--t2:#8888AA;--t3:#555577;
  --sidebar-w:180px;--radius:12px;
  --shadow:0 8px 32px rgba(0,0,0,0.5);
}
body{font-family:'Vazirmatn',sans-serif;background:var(--bg);color:var(--t1);min-height:100vh;display:flex;font-size:13px}
.sidebar{width:var(--sidebar-w);min-height:100vh;background:var(--card);backdrop-filter:blur(30px);border-left:1px solid var(--card-b);display:flex;flex-direction:column;flex-shrink:0;position:fixed;right:0;top:0;bottom:0;z-index:200;transition:transform .3s}
.logo{display:flex;align-items:center;gap:10px;padding:16px 12px 12px;border-bottom:1px solid var(--card-b)}
.logo-icon{width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,#FF6B35,#FF4500);display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0}
.logo-name{font-size:13px;font-weight:800;background:linear-gradient(135deg,#FF8C00,#FF4500);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.logo-sub{font-size:7px;color:var(--t3);margin-top:0px}
.nav-wrap{flex:1;overflow-y:auto;padding:6px 0}
.nav-it{display:flex;align-items:center;gap:8px;padding:8px 10px;color:var(--t3);font-size:11px;cursor:pointer;border-right:2px solid transparent;transition:all .2s;margin:1px 4px;border-radius:6px}
.nav-it i{font-size:14px;width:18px;text-align:center;flex-shrink:0}
.nav-it:hover{background:var(--accent-d);color:var(--t2)}
.nav-it.on{background:linear-gradient(135deg,var(--accent-d),rgba(255,80,20,0.05));color:var(--t1);border-right-color:var(--accent);font-weight:600}
.sb-foot{padding:10px 12px;border-top:1px solid var(--card-b)}
.logout-btn{display:flex;align-items:center;justify-content:center;gap:6px;background:var(--red-bg);color:var(--red-t);border-radius:6px;padding:6px;font-size:10px;font-weight:500;font-family:inherit;border:1px solid rgba(239,68,68,0.15);cursor:pointer;width:100%;transition:.2s}
.logout-btn:hover{background:rgba(239,68,68,0.2)}
.mob-top{display:none;position:fixed;top:0;right:0;left:0;height:48px;background:var(--card);backdrop-filter:blur(30px);border-bottom:1px solid var(--card-b);z-index:150;align-items:center;justify-content:space-between;padding:0 10px}
.mob-top .ml{display:flex;align-items:center;gap:6px}
.mob-logo{width:26px;height:26px;border-radius:6px;background:linear-gradient(135deg,#FF6B35,#FF4500);display:flex;align-items:center;justify-content:center;font-size:13px}
.mob-title{color:var(--t1);font-size:11px;font-weight:700}
.menu-btn{background:var(--accent-d);border:1px solid var(--card-b);color:var(--t2);width:30px;height:30px;border-radius:6px;font-size:14px;display:flex;align-items:center;justify-content:center;cursor:pointer}
.overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:190;backdrop-filter:blur(4px)}
.overlay.show{display:block}
.main{margin-right:var(--sidebar-w);flex:1;padding:16px 20px 80px;min-width:0;transition:margin .3s}
.pg{display:none;animation:pageIn .3s ease}
.pg.on{display:block}
@keyframes pageIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
.topbar{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;flex-wrap:wrap;gap:8px}
.tb-title{font-size:17px;font-weight:800;color:var(--t1);display:flex;align-items:center;gap:6px}
.tb-title i{color:var(--accent);font-size:19px}
.tb-sub{font-size:10px;color:var(--t3);margin-top:1px}
.tb-right{display:flex;align-items:center;gap:5px;flex-wrap:wrap}
.badge{font-size:8px;padding:2px 8px;border-radius:12px;font-weight:700;display:inline-flex;align-items:center;gap:3px;white-space:nowrap}
.bg-green{background:var(--green-bg);color:var(--green-t)}
.bg-blue{background:var(--blue-bg);color:var(--blue)}
.bg-fire{background:rgba(255,80,20,0.12);color:#FF8C00}
.bg-amber{background:var(--amber-bg);color:var(--amber-t)}
.dot{width:5px;height:5px;border-radius:50%;flex-shrink:0;display:inline-block}
.dg{background:var(--green)}.dr{background:var(--red)}.da{background:var(--amber)}.db{background:var(--blue)}
.pulse{animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}

.stats-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-bottom:16px}
.stat-card{background:var(--card);backdrop-filter:blur(20px);border:1px solid var(--card-b);border-radius:var(--radius);padding:12px 8px;transition:all .3s;text-align:center}
.stat-card:hover{border-color:var(--card-bh);transform:translateY(-2px)}
.stat-card .icon{font-size:18px;margin-bottom:3px;display:block}
.stat-card .number{font-size:18px;font-weight:800;color:var(--t1);line-height:1.2}
.stat-card .number.small{font-size:13px}
.stat-card .label{font-size:9px;color:var(--t3);margin-top:2px;font-weight:500}
.stat-card .sub{font-size:7px;color:var(--t3);margin-top:0px;opacity:.6}

.user-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:10px}
.user-card{background:var(--card);backdrop-filter:blur(20px);border:1px solid var(--card-b);border-radius:var(--radius);padding:12px 14px;transition:all .3s}
.user-card:hover{border-color:var(--card-bh);transform:translateY(-2px)}
.user-card .head{display:flex;align-items:center;justify-content:space-between;margin-bottom:3px}
.user-card .name{font-size:12px;font-weight:700;color:var(--t1);display:flex;align-items:center;gap:4px}
.user-card .status{font-size:8px;font-weight:700;padding:1px 8px;border-radius:8px}
.user-card .status.on{background:var(--green-bg);color:var(--green-t)}
.user-card .status.off{background:var(--red-bg);color:var(--red-t)}
.user-card .uuid{font-family:monospace;font-size:7px;color:var(--t3);margin-bottom:4px;word-break:break-all}
.user-card .info{display:grid;grid-template-columns:1fr 1fr;gap:2px 8px;font-size:9px;color:var(--t2);margin-bottom:3px}
.user-card .quota-info{display:flex;justify-content:space-between;font-size:9px;color:var(--t2);margin-bottom:2px}
.user-card .quota-bar{height:3px;border-radius:2px;background:var(--accent-d);overflow:hidden;margin-bottom:6px}
.user-card .quota-fill{height:100%;border-radius:2px;background:linear-gradient(90deg,#FF6B35,#FF4500);transition:width .6s ease}
.user-card .last-seen{font-size:8px;color:var(--t3);margin-bottom:4px}
.user-card .actions{display:flex;gap:3px;flex-wrap:wrap}
.user-card .actions .btn{font-size:8px;padding:3px 6px;border-radius:4px;flex:1;justify-content:center}
.user-card .lock-badge{font-size:7px;color:var(--amber-t);background:var(--amber-bg);padding:0px 5px;border-radius:4px}

.btn{font-family:inherit;font-size:10px;font-weight:600;border-radius:6px;padding:5px 10px;cursor:pointer;display:inline-flex;align-items:center;gap:4px;border:none;transition:all .2s;white-space:nowrap}
.btn i{font-size:11px}
.btn-p{background:linear-gradient(135deg,#FF6B35,#FF4500,#FF8C00);background-size:200% 200%;animation:btnFire 3s ease infinite;color:#fff;box-shadow:0 3px 15px rgba(255,80,20,.2)}
@keyframes btnFire{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
.btn-p:hover{transform:translateY(-1px);box-shadow:0 6px 20px rgba(255,80,20,.3)}
.btn-o{background:rgba(255,255,255,0.03);border:1px solid var(--card-b);color:var(--t2)}
.btn-o:hover{background:rgba(255,255,255,0.06)}
.btn-d{background:var(--red-bg);color:var(--red-t);border:1px solid rgba(239,68,68,.15)}
.btn-d:hover{background:rgba(239,68,68,.2)}
.btn-pur{background:rgba(139,92,246,0.1);color:#A78BFA;border:1px solid rgba(139,92,246,.15)}
.btn-pur:hover{background:rgba(139,92,246,.2)}
.btn-amber{background:var(--amber-bg);color:var(--amber-t);border:1px solid rgba(245,158,11,0.15)}
.btn-amber:hover{background:rgba(245,158,11,0.2)}
.btn-sm{padding:2px 6px;font-size:8px;border-radius:4px}
.btn-icon{width:22px;height:22px;padding:0;justify-content:center}

.modal-bg{display:none;position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:500;align-items:center;justify-content:center;backdrop-filter:blur(8px)}
.modal-bg.open{display:flex}
.modal{background:var(--card);backdrop-filter:blur(30px);border:1px solid var(--card-b);border-radius:14px;padding:20px 18px;max-width:460px;width:calc(100% - 20px);max-height:90vh;overflow-y:auto;position:relative;animation:pageIn .3s ease;box-shadow:var(--shadow)}
.modal-close{position:absolute;top:10px;left:10px;background:rgba(255,255,255,0.03);border:1px solid var(--card-b);color:var(--t2);width:24px;height:24px;border-radius:6px;font-size:12px;display:flex;align-items:center;justify-content:center;cursor:pointer;border:none;transition:.2s}
.modal-close:hover{background:var(--red-bg);color:var(--red-t)}
.modal-title{font-size:14px;font-weight:700;color:var(--t1);margin-bottom:12px;display:flex;align-items:center;gap:6px}
.modal-title i{color:var(--accent);font-size:15px}
.fg{display:flex;flex-direction:column;gap:2px;margin-bottom:8px}
.fg label{font-size:8px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.04em;display:flex;align-items:center;gap:3px}
.fi{width:100%;padding:6px 10px;border-radius:6px;border:1px solid var(--card-b);background:rgba(0,0,0,.2);color:var(--t1);font-family:inherit;font-size:10px;outline:none;transition:.2s}
.fi:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(255,80,20,.06)}
.fi::placeholder{color:var(--t3)}
select.fi{appearance:none;cursor:pointer}
.fg-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px}

.clean-ips-container{display:flex;flex-wrap:wrap;gap:6px;padding:4px 0}
.clean-ips-container .ip-item{display:flex;align-items:center;gap:4px;font-size:9px;color:var(--t2);cursor:pointer;background:rgba(255,255,255,0.02);padding:3px 8px;border-radius:4px;border:1px solid rgba(255,255,255,0.03)}
.clean-ips-container .ip-item input[type="checkbox"]{accent-color:#FF6B35;width:13px;height:13px;cursor:pointer}
.clean-ips-container .ip-item.selected{background:rgba(255,80,20,0.08);border-color:rgba(255,80,20,0.2)}

.conn-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:8px}
.conn-card{background:var(--card);backdrop-filter:blur(20px);border:1px solid var(--card-b);border-radius:10px;padding:10px 12px;transition:.2s}
.conn-card:hover{border-color:var(--card-bh)}
.conn-card .ip{font-family:monospace;font-size:11px;font-weight:700;color:var(--t1);display:flex;align-items:center;gap:4px}
.conn-card .label{font-size:8px;color:var(--t3);margin-top:1px}
.conn-card .conn-info{display:flex;justify-content:space-between;margin-top:4px;font-size:8px;color:var(--t2);gap:3px;flex-wrap:wrap}
.conn-status-dot{display:inline-block;width:5px;height:5px;border-radius:50%;background:#34D399;animation:pulse 1.5s infinite;margin-left:3px}

.settings-card{background:var(--card);backdrop-filter:blur(20px);border:1px solid var(--card-b);border-radius:var(--radius);padding:14px 16px;max-width:480px;margin-bottom:10px}
.settings-card .title{font-size:13px;font-weight:700;color:var(--t1);margin-bottom:10px;display:flex;align-items:center;gap:6px}
.settings-card .title i{color:var(--accent)}
.settings-card .field{margin-bottom:8px}
.settings-card .field label{font-size:9px;color:var(--t3);display:block;margin-bottom:2px;font-weight:600}
.settings-card .field input{width:100%;padding:6px 10px;border-radius:6px;border:1px solid var(--card-b);background:rgba(0,0,0,.2);color:var(--t1);font-family:inherit;font-size:11px;outline:none;transition:.2s}
.settings-card .field input:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(255,80,20,.06)}
.settings-card .btn{width:100%;justify-content:center;margin-top:3px;font-size:11px;padding:6px}

.toast{position:fixed;bottom:70px;left:50%;transform:translateX(-50%) translateY(50px);background:var(--card);backdrop-filter:blur(30px);border:1px solid var(--card-b);color:var(--t1);border-radius:8px;padding:8px 16px;font-size:11px;opacity:0;transition:all .3s;z-index:999;pointer-events:none;box-shadow:var(--shadow);display:flex;align-items:center;gap:5px}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.toast.ok{border-color:rgba(16,185,129,.3);background:var(--green-bg);color:var(--green-t)}
.toast.err{border-color:rgba(239,68,68,.3);background:var(--red-bg);color:var(--red-t)}

.empty{text-align:center;padding:30px 15px;color:var(--t3)}
.empty i{font-size:28px;opacity:.3;display:block;margin-bottom:6px}
.empty p{font-size:10px}

.bottom-nav{display:none;position:fixed;bottom:0;right:0;left:0;background:var(--card);backdrop-filter:blur(30px);border-top:1px solid var(--card-b);z-index:300;padding:4px 2px 6px;justify-content:space-around;align-items:center}
.bottom-nav .nav-item{display:flex;flex-direction:column;align-items:center;gap:1px;color:var(--t3);font-size:7px;cursor:pointer;padding:3px 6px;border-radius:6px;transition:all .2s;border:none;background:none;font-family:inherit;min-width:40px;position:relative}
.bottom-nav .nav-item i{font-size:16px;transition:all .2s}
.bottom-nav .nav-item:hover{color:var(--t2)}
.bottom-nav .nav-item.active{color:var(--accent)}
.bottom-nav .nav-item.active i{transform:scale(1.1)}
@media(max-width:768px){
  .bottom-nav{display:flex !important}
  .main{padding-bottom:65px !important;margin-right:0 !important;padding-top:55px !important}
  .sidebar{transform:translateX(100%);padding-bottom:60px}
  .sidebar.open{transform:translateX(0)}
  .mob-top{display:flex}
  .stats-grid{grid-template-columns:repeat(3,1fr)}
  .user-grid{grid-template-columns:1fr}
}
@media(max-width:480px){
  .stats-grid{grid-template-columns:1fr 1fr}
  .main{padding:50px 8px 65px}
  .bottom-nav .nav-item{min-width:32px;padding:2px 4px}
  .bottom-nav .nav-item i{font-size:14px}
  .bottom-nav .nav-item span{font-size:6px}
}
@media(min-width:769px){.bottom-nav{display:none !important}}
</style>
</head>
<body>
<div class="toast" id="toast"></div>

<!-- ===== مودال ساخت کاربر با انتخاب آی‌پی تمیز ===== -->
<div class="modal-bg" id="modal-user">
  <div class="modal">
    <button class="modal-close" onclick="closeModal('modal-user')"><i class="ti ti-x"></i></button>
    <div class="modal-title"><i class="ti ti-user-plus"></i> ساخت کاربر جدید</div>
    <div class="fg"><label><i class="ti ti-tag"></i> نام کاربری</label><input class="fi" id="user-label" placeholder="مثلاً: کاربر علی"></div>
    <div class="fg-grid">
      <div class="fg"><label><i class="ti ti-database"></i> حجم (GB)</label><input class="fi" id="user-quota" type="number" min="0.5" step="0.5" value="2"></div>
      <div class="fg"><label><i class="ti ti-calendar"></i> انقضا (روز)</label><input class="fi" id="user-exp" type="number" min="0" value="30" placeholder="0"></div>
      <div class="fg"><label><i class="ti ti-devices"></i> دستگاه</label><input class="fi" id="user-devices" type="number" min="0" max="10" value="1" placeholder="0"></div>
    </div>
    <div class="fg">
      <label><i class="ti ti-shield"></i> آی‌پی‌های تمیز (حداکثر ۳ عدد)</label>
      <div id="clean-ips-checkboxes" class="clean-ips-container"></div>
      <div style="font-size:7px;color:var(--t3);margin-top:2px;">💡 آی‌پی‌های انتخاب شده به صورت جداگانه در کانفیگ قرار می‌گیرند</div>
    </div>
    <div class="fg"><label><i class="ti ti-lock"></i> رمز (اختیاری)</label><input class="fi" id="user-password" type="password" placeholder="برای حذف/ویرایش" dir="ltr"></div>
    <div style="display:flex;gap:6px;margin-top:10px">
      <button class="btn btn-p" onclick="saveUser()" style="flex:2"><i class="ti ti-check"></i> ساخت</button>
      <button class="btn btn-o" onclick="closeModal('modal-user')" style="flex:1">انصراف</button>
    </div>
  </div>
</div>

<div class="modal-bg" id="modal-edit">
  <div class="modal">
    <button class="modal-close" onclick="closeModal('modal-edit')"><i class="ti ti-x"></i></button>
    <div class="modal-title"><i class="ti ti-edit"></i> ویرایش کاربر</div>
    <input type="hidden" id="edit-uuid">
    <div class="fg" id="edit-password-section"><label><i class="ti ti-lock"></i> رمز</label><input class="fi" id="edit-password" type="password" placeholder="رمز کانفیگ" dir="ltr"></div>
    <div class="fg"><label><i class="ti ti-tag"></i> نام</label><input class="fi" id="edit-label" placeholder="نام کاربری"></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px">
      <div class="fg"><label><i class="ti ti-database"></i> حجم (GB)</label><input class="fi" id="edit-quota" type="number" min="0" step="0.5"></div>
      <div class="fg"><label><i class="ti ti-calendar"></i> انقضا (روز)</label><input class="fi" id="edit-exp" type="number" min="0" placeholder="0"></div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px">
      <div class="fg"><label><i class="ti ti-devices"></i> دستگاه</label><input class="fi" id="edit-devices" type="number" min="0" max="10" placeholder="0"></div>
      <div class="fg"><label><i class="ti ti-toggle-left"></i> وضعیت</label><select class="fi" id="edit-status"><option value="true">✅ فعال</option><option value="false">❌ غیرفعال</option></select></div>
    </div>
    <div style="display:flex;gap:6px;margin-top:10px">
      <button class="btn btn-p" onclick="saveEdit()" style="flex:2"><i class="ti ti-check"></i> ذخیره</button>
      <button class="btn btn-o" onclick="closeModal('modal-edit')" style="flex:1">انصراف</button>
    </div>
  </div>
</div>

<div class="modal-bg" id="modal-delete">
  <div class="modal" style="max-width:340px">
    <button class="modal-close" onclick="closeModal('modal-delete')"><i class="ti ti-x"></i></button>
    <div class="modal-title"><i class="ti ti-trash"></i> حذف کاربر</div>
    <input type="hidden" id="delete-uuid">
    <p style="font-size:10px;color:var(--t2);margin-bottom:10px">برای حذف، رمز کانفیگ را وارد کنید.</p>
    <div class="fg"><label><i class="ti ti-lock"></i> رمز</label><input class="fi" id="delete-password" type="password" placeholder="رمز کانفیگ" dir="ltr"></div>
    <div style="display:flex;gap:6px;margin-top:10px">
      <button class="btn btn-d" onclick="confirmDelete()" style="flex:2"><i class="ti ti-trash"></i> حذف</button>
      <button class="btn btn-o" onclick="closeModal('modal-delete')" style="flex:1">انصراف</button>
    </div>
  </div>
</div>

<!-- ===== هدر موبایل ===== -->
<div class="mob-top">
  <div class="ml"><div class="mob-logo">🦅</div><span class="mob-title">پنل عقاب</span></div>
  <button class="menu-btn" id="open-sb"><i class="ti ti-menu-2"></i></button>
</div>
<div class="overlay" id="overlay"></div>

<!-- ===== سایدبار ===== -->
<aside class="sidebar" id="sb">
  <div class="logo"><div class="logo-icon">🦅</div><div><div class="logo-name">پنل عقاب</div><div class="logo-sub">مدیریت کاربران</div></div></div>
  <div class="nav-wrap">
    <div class="nav-it on" data-pg="dashboard"><i class="ti ti-layout-dashboard"></i> خانه</div>
    <div class="nav-it" data-pg="settings"><i class="ti ti-settings"></i> تنظیمات</div>
    <div class="nav-it" data-pg="inbound"><i class="ti ti-plug"></i> ربات</div>
    <div class="nav-it" data-pg="logs"><i class="ti ti-notes"></i> لگ</div>
    <div class="nav-it" data-pg="clean-ips"><i class="ti ti-shield"></i> آی‌پی تمیز</div>
    <div class="nav-it" data-pg="bandwidth"><i class="ti ti-wifi"></i> ایپاند</div>
    <div class="nav-it" data-pg="users"><i class="ti ti-users"></i> کاربران</div>
    <div class="nav-it" data-pg="connections"><i class="ti ti-plug-connected"></i> اتصالات</div>
    <div class="nav-it" data-pg="backup"><i class="ti ti-database"></i> بکاپ</div>
  </div>
  <div class="sb-foot">
    <button class="logout-btn" onclick="logout()"><i class="ti ti-logout"></i> خروج</button>
  </div>
</aside>

<!-- ===== منوی پایین (موبایل) ===== -->
<div class="bottom-nav" id="bottomNav">
  <button class="nav-item active" data-pg="dashboard" onclick="navTo('dashboard')"><i class="ti ti-layout-dashboard"></i><span>خانه</span></button>
  <button class="nav-item" data-pg="settings" onclick="navTo('settings')"><i class="ti ti-settings"></i><span>تنظیمات</span></button>
  <button class="nav-item" data-pg="inbound" onclick="navTo('inbound')"><i class="ti ti-plug"></i><span>ربات</span></button>
  <button class="nav-item" data-pg="logs" onclick="navTo('logs')"><i class="ti ti-notes"></i><span>لگ</span></button>
  <button class="nav-item" data-pg="clean-ips" onclick="navTo('clean-ips')"><i class="ti ti-shield"></i><span>آی‌پی تمیز</span></button>
  <button class="nav-item" data-pg="bandwidth" onclick="navTo('bandwidth')"><i class="ti ti-wifi"></i><span>ایپاند</span></button>
</div>

<!-- ===== محتوای اصلی ===== -->
<main class="main">

<!-- ===== خانه ===== -->
<section class="pg on" id="pg-dashboard">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-layout-dashboard"></i> خانه</div><div class="tb-sub" id="last-update">بروزرسانی: لحظه‌ای</div></div>
    <div class="tb-right">
      <span class="badge bg-fire" id="online-badge"><span class="dot dg"></span> ۰ آنلاین</span>
      <button class="btn btn-p btn-sm" onclick="openModal('modal-user')"><i class="ti ti-plus"></i> کاربر</button>
    </div>
  </div>
  <div class="stats-grid">
    <div class="stat-card"><span class="icon">📊</span><div class="number" id="stat-traffic">۰</div><div class="label">ترافیک</div><div class="sub">MB</div></div>
    <div class="stat-card"><span class="icon">📨</span><div class="number" id="stat-requests">۰</div><div class="label">درخواست‌ها</div><div class="sub">تعداد</div></div>
    <div class="stat-card"><span class="icon">⏱️</span><div class="number" id="stat-uptime">۰۰:۰۰:۰۰</div><div class="label">آپتایم</div><div class="sub">زمان</div></div>
    <div class="stat-card"><span class="icon">💾</span><div class="number small" id="stat-disk">۰ GB</div><div class="label">فضای دیسک</div><div class="sub" id="stat-disk-used">استفاده</div></div>
    <div class="stat-card"><span class="icon">📶</span><div class="number small" id="stat-speed">۰ B/s</div><div class="label">سرعت</div><div class="sub">لحظه‌ای</div></div>
    <div class="stat-card"><span class="icon">👥</span><div class="number" id="stat-users">۰</div><div class="label">کاربران</div><div class="sub" id="stat-users-active">۰ فعال</div></div>
  </div>
  <div style="background:var(--card);border:1px solid var(--card-b);border-radius:var(--radius);padding:10px 12px;margin-top:4px">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
      <span style="font-size:11px;font-weight:700;color:var(--t1)">🆕 کاربران اخیر</span>
      <button class="btn btn-sm btn-o" onclick="loadDashboard()"><i class="ti ti-refresh"></i></button>
    </div>
    <div id="recent-users" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:4px"></div>
  </div>
</section>

<!-- ===== کاربران ===== -->
<section class="pg" id="pg-users">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-users"></i> کاربران</div><div class="tb-sub" id="users-count">۰ کاربر</div></div>
    <div class="tb-right"><button class="btn btn-p btn-sm" onclick="openModal('modal-user')"><i class="ti ti-plus"></i> جدید</button></div>
  </div>
  <div id="users-grid" class="user-grid"><div class="empty"><i class="ti ti-users"></i><p>هیچ کاربری وجود ندارد</p></div></div>
</section>

<!-- ===== اینباند ===== -->
<section class="pg" id="pg-inbound">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-plug"></i> اینباند</div><div class="tb-sub">تنظیمات ورودی</div></div></div>
  <div style="background:var(--card);border:1px solid var(--card-b);border-radius:var(--radius);padding:12px 14px;margin-bottom:10px">
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px">
      <div style="text-align:center"><div style="font-size:14px;font-weight:700;color:var(--t1)" id="inbound-port">۴۴۳</div><div style="font-size:8px;color:var(--t3)">پورت</div></div>
      <div style="text-align:center"><div style="font-size:14px;font-weight:700;color:var(--t1)" id="inbound-protocol">VLESS</div><div style="font-size:8px;color:var(--t3)">پروتکل</div></div>
      <div style="text-align:center"><div style="font-size:12px;font-weight:700;color:var(--t1)" id="inbound-host">—</div><div style="font-size:8px;color:var(--t3)">هاست</div></div>
      <div style="text-align:center"><div style="font-size:14px;font-weight:700;color:#34D399">✅ فعال</div><div style="font-size:8px;color:var(--t3)">وضعیت</div></div>
    </div>
    <div style="display:flex;gap:6px;margin-top:10px;flex-wrap:wrap">
      <button class="btn btn-p btn-sm" onclick="openModal('modal-user')"><i class="ti ti-user-plus"></i> کاربر</button>
      <button class="btn btn-o btn-sm" onclick="openModal('modal-inbound')"><i class="ti ti-settings"></i> تنظیمات</button>
    </div>
  </div>
  <div style="background:var(--card);border:1px solid var(--card-b);border-radius:var(--radius);padding:10px 12px">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
      <span style="font-size:11px;font-weight:700;color:var(--t1)">📋 کاربران اینباند</span>
    </div>
    <div id="inbound-users-grid" class="user-grid"></div>
  </div>
</section>

<!-- ===== اتصالات ===== -->
<section class="pg" id="pg-connections">
  <div class="topbar"><div><div class="tb-title">🔌 اتصالات</div><div class="tb-sub" id="conn-count">۰ اتصال</div></div>
    <div class="tb-right"><span class="badge bg-green"><span class="dot dg pulse"></span> فعال</span><button class="btn btn-sm btn-o" onclick="loadConnections()"><i class="ti ti-refresh"></i></button></div>
  </div>
  <div id="conns-grid" class="conn-grid"><div class="empty"><i class="ti ti-plug-off"></i><p>هیچ اتصالی وجود ندارد</p></div></div>
</section>

<!-- ===== آی‌پی تمیز ===== -->
<section class="pg" id="pg-clean-ips">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-shield"></i> آی‌پی تمیز</div><div class="tb-sub">مدیریت آی‌پی‌ها</div></div></div>
  <div class="settings-card">
    <div class="title"><i class="ti ti-shield"></i> لیست آی‌پی‌های تمیز</div>
    <div style="display:flex;gap:6px;margin-bottom:8px">
      <input class="fi" id="clean-ip-input" placeholder="آی‌پی جدید" style="flex:1;font-size:10px">
      <button class="btn btn-p btn-sm" onclick="addCleanIP()"><i class="ti ti-plus"></i> افزودن</button>
    </div>
    <div id="clean-ips-list" style="display:flex;flex-wrap:wrap;gap:4px"></div>
    <div style="font-size:8px;color:var(--t3);margin-top:6px;">💡 آی‌پی‌های ثبت شده در بخش ساخت کاربر قابل انتخاب هستند (حداکثر ۳ عدد)</div>
  </div>
</section>

<!-- ===== ایپاند ===== -->
<section class="pg" id="pg-bandwidth">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-wifi"></i> ایپاند</div><div class="tb-sub">مدیریت پهنای باند</div></div></div>
  <div class="settings-card">
    <div class="title"><i class="ti ti-wifi"></i> محدودیت پهنای باند</div>
    <div class="field"><label>محدودیت (MB/s)</label><input class="fi" id="bandwidth-limit" type="number" min="0" step="0.5" value="0" placeholder="0 = نامحدود"></div>
    <div class="field"><label>مصرف شده</label><div style="font-size:16px;font-weight:700;color:var(--t1)" id="bandwidth-used">۰ MB</div></div>
    <button class="btn btn-p" onclick="saveBandwidth()"><i class="ti ti-check"></i> ذخیره</button>
  </div>
</section>

<!-- ===== تنظیمات ===== -->
<section class="pg" id="pg-settings">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-settings"></i> تنظیمات</div><div class="tb-sub">مدیریت پنل</div></div></div>
  <div class="settings-card">
    <div class="title"><i class="ti ti-key"></i> تغییر رمز</div>
    <div class="field"><label>رمز فعلی</label><input class="fi" id="old-password" type="password" placeholder="رمز فعلی" dir="ltr"></div>
    <div class="field"><label>رمز جدید</label><input class="fi" id="new-password" type="password" placeholder="حداقل ۴ کاراکتر" dir="ltr"></div>
    <div class="field"><label>تکرار</label><input class="fi" id="confirm-password" type="password" placeholder="تکرار" dir="ltr"></div>
    <button class="btn btn-p" onclick="changePassword()"><i class="ti ti-key"></i> تغییر</button>
    <div id="password-result" style="margin-top:8px;display:none;font-size:11px;"></div>
  </div>
  <div class="settings-card">
    <div class="title"><i class="ti ti-plug"></i> پورت اینباند</div>
    <div class="field"><label>پورت</label><input class="fi" id="inbound-port-setting" type="number" min="1" max="65535" value="443"></div>
    <button class="btn btn-p" onclick="updateInbound()"><i class="ti ti-check"></i> ذخیره</button>
  </div>
</section>

<!-- ===== لاگ‌ها ===== -->
<section class="pg" id="pg-logs">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-notes"></i> لاگ‌ها</div><div class="tb-sub" id="logs-count">۰ لاگ</div></div>
    <div class="tb-right"><button class="btn btn-sm btn-o" onclick="loadLogs()"><i class="ti ti-refresh"></i></button></div>
  </div>
  <div style="background:var(--card);border:1px solid var(--card-b);border-radius:var(--radius);padding:8px 10px;max-height:400px;overflow-y:auto">
    <div id="logs-container" style="font-family:monospace;font-size:9px;color:var(--t2);direction:ltr;text-align:left;line-height:1.5"></div>
  </div>
</section>

<!-- ===== بکاپ ===== -->
<section class="pg" id="pg-backup">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-database"></i> بکاپ</div><div class="tb-sub">ذخیره و بازیابی</div></div></div>
  <div class="settings-card">
    <div class="title"><i class="ti ti-download"></i> بکاپ‌گیری</div>
    <div style="display:flex;gap:6px;flex-wrap:wrap">
      <button class="btn btn-p btn-sm" onclick="createBackup()" style="flex:2"><i class="ti ti-download"></i> دانلود</button>
      <button class="btn btn-o btn-sm" onclick="document.getElementById('restore-input').click()" style="flex:1"><i class="ti ti-upload"></i> بازیابی</button>
      <input type="file" id="restore-input" accept=".json" style="display:none" onchange="restoreBackup(event)">
    </div>
  </div>
</section>

</main>

<script>
// ===== توابع کمکی =====
function toast(msg, type='') {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = 'toast show' + (type ? ' ' + type : '');
  setTimeout(() => t.classList.remove('show'), 2500);
}

function fmtB(b) {
  if (!b || b === 0) return '0 B';
  if (b < 1024) return b + ' B';
  if (b < 1024**2) return (b/1024).toFixed(1) + ' KB';
  if (b < 1024**3) return (b/1024**2).toFixed(1) + ' MB';
  if (b < 1024**4) return (b/1024**3).toFixed(2) + ' GB';
  return (b/1024**4).toFixed(2) + ' TB';
}

function esc(s) {
  return String(s || '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

function openModal(id) {
  if (id === 'modal-user') {
    loadCleanIPsForModal();
  }
  document.getElementById(id).classList.add('open');
}
function closeModal(id) { document.getElementById(id).classList.remove('open'); }

// ===== احراز هویت =====
async function authF(url, opts={}) {
  const r = await fetch(url, opts);
  if (r.status === 401) { location.href = '/login'; throw new Error('unauthorized'); }
  return r;
}

async function logout() {
  try { await fetch('/api/logout', {method:'POST'}); } catch(e) {}
  location.href = '/login';
}

// ===== ناوبری =====
function navTo(name) {
  document.querySelectorAll('.nav-it').forEach(n => n.classList.toggle('on', n.dataset.pg === name));
  document.querySelectorAll('.pg').forEach(p => p.classList.toggle('on', p.id === 'pg-' + name));
  document.querySelectorAll('.bottom-nav .nav-item').forEach(n => n.classList.toggle('active', n.dataset.pg === name));
  closeSb();
  const loaders = {
    dashboard: loadDashboard,
    users: loadUsers,
    inbound: loadInbound,
    connections: loadConnections,
    logs: loadLogs,
    'clean-ips': loadCleanIPs,
    bandwidth: loadBandwidth,
    settings: () => {}
  };
  if (loaders[name]) loaders[name]();
}

document.querySelectorAll('.nav-it, .bottom-nav .nav-item').forEach(el => {
  el.addEventListener('click', () => navTo(el.dataset.pg));
});

const sb = document.getElementById('sb'), overlay = document.getElementById('overlay');
function openSb(){ sb.classList.add('open'); overlay.classList.add('show'); }
function closeSb(){ sb.classList.remove('open'); overlay.classList.remove('show'); }
document.getElementById('open-sb').addEventListener('click', openSb);
overlay.addEventListener('click', closeSb);

// ===== بارگذاری آی‌پی‌های تمیز در مودال =====
async function loadCleanIPsForModal() {
  try {
    const r = await authF('/api/clean-ips');
    const data = await r.json();
    const ips = data.ips || [];
    const container = document.getElementById('clean-ips-checkboxes');
    if (!ips.length) {
      container.innerHTML = '<div style="font-size:9px;color:var(--t3);padding:4px 0;">⚠️ هیچ آی‌پی تمیزی ثبت نشده. ابتدا از بخش آی‌پی تمیز اضافه کنید.</div>';
      return;
    }
    container.innerHTML = ips.map(ip => `
      <label class="ip-item">
        <input type="checkbox" class="clean-ip-checkbox" value="${esc(ip)}" style="accent-color:#FF6B35;width:13px;height:13px;cursor:pointer;">
        ${esc(ip)}
      </label>
    `).join('');
    document.querySelectorAll('.clean-ip-checkbox').forEach(cb => {
      cb.addEventListener('change', function() {
        const checked = document.querySelectorAll('.clean-ip-checkbox:checked');
        if (checked.length > 3) {
          this.checked = false;
          toast('❌ حداکثر ۳ آی‌پی می‌توانید انتخاب کنید', 'err');
        }
      });
    });
  } catch(e) { console.error(e); }
}

// ===== داشبورد =====
async function loadDashboard() {
  try {
    const r = await authF('/api/dashboard/stats');
    const data = await r.json();
    document.getElementById('stat-traffic').textContent = (data.traffic.total / (1024*1024)).toFixed(1);
    document.getElementById('stat-requests').textContent = data.requests || 0;
    document.getElementById('stat-uptime').textContent = data.uptime || '00:00:00';
    document.getElementById('stat-disk').textContent = data.disk.total_fmt || '0 GB';
    document.getElementById('stat-disk-used').textContent = 'استفاده: ' + (data.disk.used_fmt || '0');
    document.getElementById('stat-speed').textContent = data.speed.download_fmt || '0 B/s';
    document.getElementById('stat-users').textContent = data.links_count || 0;
    document.getElementById('stat-users-active').textContent = (data.active_links || 0) + ' فعال';
    document.getElementById('online-badge').innerHTML = '<span class="dot dg"></span> ' + (data.connections || 0) + ' آنلاین';
    document.getElementById('last-update').textContent = 'بروزرسانی: ' + new Date().toLocaleTimeString('fa-IR');
    
    const usersR = await authF('/api/links');
    const usersData = await usersR.json();
    const links = usersData.links || [];
    const recent = links.slice(0, 4);
    const grid = document.getElementById('recent-users');
    if (!recent.length) {
      grid.innerHTML = '<div class="empty" style="padding:10px"><i class="ti ti-users"></i><p style="font-size:9px">هیچ کاربری وجود ندارد</p></div>';
    } else {
      grid.innerHTML = recent.map(l => `
        <div style="background:rgba(255,255,255,0.02);border-radius:4px;padding:4px 6px;display:flex;justify-content:space-between;align-items:center">
          <div><div style="font-size:9px;font-weight:600;color:var(--t1)">${esc(l.label)}</div><div style="font-size:7px;color:var(--t3)">${l.active ? '🟢' : '🔴'}</div></div>
          <div style="font-size:8px;color:var(--t2)">${fmtB(l.used_bytes || 0)}</div>
        </div>
      `).join('');
    }
  } catch(e) { console.error(e); }
}

// ===== اینباند =====
async function loadInbound() {
  try {
    const r = await authF('/api/inbound');
    const data = await r.json();
    document.getElementById('inbound-port').textContent = data.port || 443;
    document.getElementById('inbound-protocol').textContent = (data.protocol || 'vless').toUpperCase();
    document.getElementById('inbound-host').textContent = data.host || '—';
    document.getElementById('inbound-port-setting').value = data.port || 443;
    loadUsers();
  } catch(e) { console.error(e); }
}

async function updateInbound() {
  const port = parseInt(document.getElementById('inbound-port-setting').value) || 443;
  try {
    const r = await authF('/api/inbound', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ port: port })
    });
    if (!r.ok) { toast('❌ خطا', 'err'); return; }
    toast('✅ ذخیره شد', 'ok');
    loadInbound();
  } catch(e) { toast('❌ خطا', 'err'); }
}

// ===== کاربران =====
async function loadUsers() {
  try {
    const r = await authF('/api/links');
    const { links=[] } = await r.json();
    const grid = document.getElementById('users-grid');
    const inboundGrid = document.getElementById('inbound-users-grid');
    document.getElementById('users-count').textContent = links.length + ' کاربر';
    if (!links.length) {
      const empty = '<div class="empty"><i class="ti ti-users"></i><p>هیچ کاربری وجود ندارد</p></div>';
      grid.innerHTML = empty;
      if (inboundGrid) inboundGrid.innerHTML = empty;
      return;
    }
    const html = links.map(l => {
      const pct = l.limit_bytes === 0 ? 0 : Math.min(100, (l.used_bytes / l.limit_bytes) * 100);
      const active = l.active && !l.expired;
      const statusClass = active ? 'on' : 'off';
      const statusText = active ? '🟢' : '🔴';
      const lastSeen = l.last_connected_at ? new Date(l.last_connected_at).toLocaleString('fa-IR') : '—';
      const cleanIps = l.clean_ips || [];
      const ipsText = cleanIps.length ? cleanIps.join(', ') : 'پیش‌فرض';
      return `<div class="user-card">
        <div class="head"><div class="name">🦅 ${esc(l.label)} ${l.has_password ? '<span class="lock-badge">🔒</span>' : ''}</div><span class="status ${statusClass}">${statusText}</span></div>
        <div class="uuid">🔑 ${esc(l.uuid)}</div>
        <div class="info"><span>📊 ${fmtB(l.used_bytes || 0)}</span><span>📦 ${l.limit_bytes === 0 ? '∞' : fmtB(l.limit_bytes)}</span><span>📱 ${l.max_devices || '∞'}</span><span>${l.expired ? '⛔' : '✅'}</span></div>
        <div style="font-size:8px;color:var(--t3);margin-bottom:2px;">🌐 ${ipsText}</div>
        <div class="last-seen"><i class="ti ti-clock"></i> ${lastSeen}</div>
        <div class="quota-info"><span>مصرف</span><span>${pct.toFixed(0)}%</span></div>
        <div class="quota-bar"><div class="quota-fill" style="width:${pct}%"></div></div>
        <div class="actions">
          <button class="btn btn-o btn-sm" onclick="showLinks('${l.uuid}')"><i class="ti ti-link"></i></button>
          <button class="btn btn-pur btn-sm" onclick="navigator.clipboard.writeText('${esc(l.sub_url)}').then(()=>toast('✅ کپی شد','ok'))"><i class="ti ti-copy"></i></button>
          <button class="btn btn-amber btn-sm" onclick="resetUsage('${l.uuid}')"><i class="ti ti-rotate"></i></button>
          <button class="btn btn-pur btn-sm btn-icon" onclick="openEditModal('${l.uuid}')"><i class="ti ti-edit"></i></button>
          <button class="btn btn-d btn-sm btn-icon" onclick="openDeleteModal('${l.uuid}')"><i class="ti ti-trash"></i></button>
        </div>
      </div>`;
    }).join('');
    grid.innerHTML = html;
    if (inboundGrid) inboundGrid.innerHTML = html;
  } catch(e) { console.error(e); }
}

// ===== نمایش لینک‌ها =====
async function showLinks(uuid) {
  try {
    const r = await authF('/api/links');
    const { links=[] } = await r.json();
    const link = links.find(l => l.uuid === uuid);
    if (!link) { toast('کاربر یافت نشد', 'err'); return; }
    const vlessLinks = link.vless_links || [link.vless_link];
    let msg = `🦅 <b>${esc(link.label)}</b>\n━━━━━━━━━━━━━━━━\n`;
    vlessLinks.forEach((l, i) => {
      msg += `🔗 لینک ${i+1}:\n<code>${l}</code>\n\n`;
    });
    msg += `📎 ساب‌لینک:\n<code>${link.sub_url}</code>`;
    // ارسال به صورت پیام
    toast('📋 لینک‌ها کپی شدند', 'ok');
    // کپی همه لینک‌ها در کلیپ‌بورد
    const allLinks = vlessLinks.join('\n');
    navigator.clipboard.writeText(allLinks).then(() => toast('✅ همه لینک‌ها کپی شدند', 'ok'));
  } catch(e) { toast('❌ خطا', 'err'); }
}

// ===== ساخت کاربر =====
async function saveUser() {
  const label = document.getElementById('user-label').value.trim() || 'کاربر';
  const quota = parseFloat(document.getElementById('user-quota').value) || 0;
  const exp = parseInt(document.getElementById('user-exp').value) || 30;
  const devices = parseInt(document.getElementById('user-devices').value) || 0;
  const password = document.getElementById('user-password').value.trim();
  
  const selectedIPs = [];
  document.querySelectorAll('.clean-ip-checkbox:checked').forEach(cb => {
    selectedIPs.push(cb.value);
  });
  if (!selectedIPs.length) {
    toast('❌ حداقل یک آی‌پی تمیز انتخاب کنید', 'err');
    return;
  }
  
  try {
    const r = await authF('/api/links', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        label, limit_value: quota, limit_unit: 'GB',
        expires_days: exp, max_devices: devices,
        password, fingerprint: 'chrome', protocol: 'vless-ws',
        port: 443, clean_ips: selectedIPs
      })
    });
    if (!r.ok) throw new Error();
    const data = await r.json();
    
    document.getElementById('user-label').value = '';
    document.getElementById('user-quota').value = '2';
    document.getElementById('user-exp').value = '30';
    document.getElementById('user-devices').value = '1';
    document.getElementById('user-password').value = '';
    document.querySelectorAll('.clean-ip-checkbox:checked').forEach(cb => cb.checked = false);
    
    closeModal('modal-user');
    
    let linksMsg = '';
    if (data.vless_links && data.vless_links.length) {
      data.vless_links.forEach((l, i) => {
        linksMsg += `🔗 لینک ${i+1}:\n<code>${l}</code>\n\n`;
      });
    }
    
    toast('✅ کاربر ساخته شد', 'ok');
    loadUsers(); loadDashboard();
  } catch(e) { toast('❌ خطا', 'err'); }
}

// ===== ویرایش =====
async function openEditModal(uuid) {
  try {
    const r = await authF('/api/links');
    const { links=[] } = await r.json();
    const link = links.find(l => l.uuid === uuid);
    if (!link) { toast('کاربر یافت نشد', 'err'); return; }
    document.getElementById('edit-uuid').value = uuid;
    document.getElementById('edit-label').value = link.label || '';
    document.getElementById('edit-password').value = '';
    document.getElementById('edit-quota').value = link.limit_bytes === 0 ? '' : (link.limit_bytes / (1024**3)).toFixed(1);
    document.getElementById('edit-exp').value = link.expires_at ? Math.ceil((new Date(link.expires_at) - new Date()) / (1000*60*60*24)) : '';
    document.getElementById('edit-devices').value = link.max_devices || 0;
    document.getElementById('edit-status').value = link.active ? 'true' : 'false';
    document.getElementById('edit-password-section').style.display = link.has_password ? 'block' : 'none';
    openModal('modal-edit');
  } catch(e) { toast('خطا', 'err'); }
}

async function saveEdit() {
  const uuid = document.getElementById('edit-uuid').value;
  const password = document.getElementById('edit-password').value.trim();
  const label = document.getElementById('edit-label').value.trim() || 'کاربر';
  const quota = parseFloat(document.getElementById('edit-quota').value) || 0;
  const exp = parseInt(document.getElementById('edit-exp').value) || 0;
  const devices = parseInt(document.getElementById('edit-devices').value) || 0;
  const active = document.getElementById('edit-status').value === 'true';
  try {
    const r = await authF('/api/links/' + uuid, {
      method: 'PATCH', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ label, limit_value: quota, limit_unit: 'GB', expires_days: exp, max_devices: devices, active, password })
    });
    if (!r.ok) { if (r.status === 403) { toast('❌ رمز اشتباه', 'err'); return; } throw new Error(); }
    closeModal('modal-edit');
    toast('✅ ویرایش شد', 'ok');
    loadUsers();
  } catch(e) { toast('❌ خطا', 'err'); }
}

// ===== حذف =====
function openDeleteModal(uuid) {
  document.getElementById('delete-uuid').value = uuid;
  document.getElementById('delete-password').value = '';
  openModal('modal-delete');
}

async function confirmDelete() {
  const uuid = document.getElementById('delete-uuid').value;
  const password = document.getElementById('delete-password').value.trim();
  try {
    const r = await authF('/api/links/' + uuid, {
      method: 'DELETE', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password })
    });
    if (!r.ok) { if (r.status === 403) { toast('❌ رمز اشتباه', 'err'); return; } throw new Error(); }
    closeModal('modal-delete');
    toast('✅ حذف شد', 'ok');
    loadUsers(); loadDashboard();
  } catch(e) { toast('❌ خطا', 'err'); }
}

async function resetUsage(uuid) {
  if (!confirm('ریست مصرف؟')) return;
  try {
    const r = await authF('/api/links/' + uuid, {
      method: 'PATCH', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reset_usage: true })
    });
    if (!r.ok) throw new Error();
    toast('✅ ریست شد', 'ok');
    loadUsers();
  } catch(e) { toast('❌ خطا', 'err'); }
}

// ===== اتصالات =====
async function loadConnections() {
  try {
    const r = await authF('/api/connections');
    const d = await r.json();
    const grid = document.getElementById('conns-grid');
    const count = d.count || 0;
    document.getElementById('conn-count').textContent = count + ' اتصال';
    if (!count) { grid.innerHTML = '<div class="empty"><i class="ti ti-plug-off"></i><p>هیچ اتصالی وجود ندارد</p></div>'; return; }
    grid.innerHTML = d.connections.map(c => {
      const secs = c.connected_at ? Math.max(0, Math.floor((Date.now() - new Date(c.connected_at).getTime()) / 1000)) : 0;
      const dur = secs < 60 ? secs + 'ث' : secs < 3600 ? Math.floor(secs/60) + 'د' : Math.floor(secs/3600) + 'س';
      return `<div class="conn-card"><div class="ip"><span class="conn-status-dot"></span> ${esc(c.ip)}</div><div class="label">${esc(c.label || 'نامشخص')}</div><div class="conn-info"><span>📥 ${esc(c.bytes_fmt || '0 B')}</span><span>⏱ ${dur}</span></div></div>`;
    }).join('');
  } catch(e) { console.error(e); }
}

// ===== لاگ‌ها =====
async function loadLogs() {
  try {
    const r = await authF('/api/activity');
    const data = await r.json();
    const logs = data.logs || [];
    document.getElementById('logs-count').textContent = logs.length + ' لاگ';
    const container = document.getElementById('logs-container');
    if (!logs.length) { container.innerHTML = '<div class="empty"><i class="ti ti-notes"></i><p>هیچ لاگی وجود ندارد</p></div>'; return; }
    container.innerHTML = logs.map(log => {
      const time = log.time ? new Date(log.time).toLocaleString('fa-IR') : '—';
      const color = log.level === 'err' ? '#F87171' : log.level === 'warn' ? '#FCD34D' : '#34D399';
      return `<div style="padding:3px 0;border-bottom:1px solid rgba(255,255,255,0.02);display:flex;gap:6px"><span style="color:${color};font-weight:700">[${(log.level || 'info').toUpperCase()}]</span><span style="color:var(--t3)">${time}</span><span>${esc(log.message)}</span></div>`;
    }).join('');
  } catch(e) { console.error(e); }
}

// ===== آی‌پی تمیز =====
async function loadCleanIPs() {
  try {
    const r = await authF('/api/clean-ips');
    const data = await r.json();
    const ips = data.ips || [];
    const list = document.getElementById('clean-ips-list');
    if (!ips.length) { list.innerHTML = '<div class="empty" style="padding:10px"><i class="ti ti-shield"></i><p style="font-size:9px">هیچ آی‌پی تمیزی وجود ندارد</p></div>'; return; }
    list.innerHTML = ips.map(ip => 
      `<span style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.04);border-radius:4px;padding:2px 8px;font-size:9px;display:flex;align-items:center;gap:4px">
        ${esc(ip)}
        <button onclick="removeCleanIP('${esc(ip)}')" style="background:none;border:none;color:#F87171;cursor:pointer;font-size:10px">✕</button>
      </span>`
    ).join('');
  } catch(e) { console.error(e); }
}

async function addCleanIP() {
  const input = document.getElementById('clean-ip-input');
  const ip = input.value.trim();
  if (!ip) { toast('❌ آی‌پی را وارد کنید', 'err'); return; }
  try {
    const r = await authF('/api/clean-ips', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ip })
    });
    if (!r.ok) throw new Error();
    input.value = '';
    toast('✅ آی‌پی اضافه شد', 'ok');
    loadCleanIPs();
  } catch(e) { toast('❌ خطا', 'err'); }
}

async function removeCleanIP(ip) {
  try {
    const r = await authF('/api/clean-ips/' + encodeURIComponent(ip), { method: 'DELETE' });
    if (!r.ok) throw new Error();
    toast('✅ آی‌پی حذف شد', 'ok');
    loadCleanIPs();
  } catch(e) { toast('❌ خطا', 'err'); }
}

// ===== ایپاند =====
async function loadBandwidth() {
  try {
    const r = await authF('/api/bandwidth');
    const data = await r.json();
    document.getElementById('bandwidth-limit').value = data.limit || 0;
    document.getElementById('bandwidth-used').textContent = data.used_fmt || '0 B';
  } catch(e) { console.error(e); }
}

async function saveBandwidth() {
  const limit = parseFloat(document.getElementById('bandwidth-limit').value) || 0;
  try {
    const r = await authF('/api/bandwidth', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ limit })
    });
    if (!r.ok) throw new Error();
    toast('✅ ذخیره شد', 'ok');
    loadBandwidth();
  } catch(e) { toast('❌ خطا', 'err'); }
}

// ===== تغییر رمز =====
async function changePassword() {
  const oldPw = document.getElementById('old-password').value;
  const newPw = document.getElementById('new-password').value;
  const confirmPw = document.getElementById('confirm-password').value;
  const result = document.getElementById('password-result');
  if (!oldPw || !newPw || !confirmPw) { result.style.display='block'; result.style.color='#F87171'; result.innerHTML='❌ همه فیلدها را پر کنید'; return; }
  if (newPw.length < 4) { result.style.display='block'; result.style.color='#F87171'; result.innerHTML='❌ حداقل ۴ کاراکتر'; return; }
  if (newPw !== confirmPw) { result.style.display='block'; result.style.color='#F87171'; result.innerHTML='❌ رمزها مطابقت ندارند'; return; }
  try {
    const r = await authF('/api/change-password', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ old_password: oldPw, new_password: newPw })
    });
    const data = await r.json();
    if (!r.ok) { result.style.display='block'; result.style.color='#F87171'; result.innerHTML='❌ ' + (data.detail || data.message || 'خطا'); return; }
    result.style.display='block'; result.style.color='#34D399'; result.innerHTML='✅ رمز تغییر کرد!';
    document.getElementById('old-password').value = '';
    document.getElementById('new-password').value = '';
    document.getElementById('confirm-password').value = '';
    toast('✅ رمز تغییر کرد', 'ok');
  } catch(e) { result.style.display='block'; result.style.color='#F87171'; result.innerHTML='❌ خطا'; }
}

// ===== بکاپ =====
async function createBackup() {
  try {
    const r = await authF('/api/backup');
    const data = await r.json();
    const blob = new Blob([JSON.stringify(data, null, 2)], {type:'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `eagle_backup_${new Date().toISOString().slice(0,10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
    toast('✅ بکاپ دانلود شد', 'ok');
  } catch(e) { toast('❌ خطا', 'err'); }
}

async function restoreBackup(event) {
  const file = event.target.files[0];
  if (!file) return;
  try {
    const text = await file.text();
    const data = JSON.parse(text);
    const r = await authF('/api/backup/restore', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!r.ok) { toast('❌ خطا', 'err'); return; }
    toast('✅ بکاپ بازیابی شد', 'ok');
    setTimeout(() => location.reload(), 1000);
  } catch(e) { toast('❌ خطا: ' + e.message, 'err'); }
  event.target.value = '';
}

// ===== بارگذاری اولیه =====
document.addEventListener('DOMContentLoaded', async () => {
  try {
    const r = await fetch('/api/me');
    const d = await r.json();
    if (!d.authenticated) location.href = '/login';
  } catch(e) { location.href = '/login'; }
  loadDashboard();
  loadInbound();
  loadUsers();
  loadConnections();
  loadLogs();
  loadCleanIPs();
  loadBandwidth();
  setInterval(() => {
    if (document.getElementById('pg-dashboard').classList.contains('on')) loadDashboard();
    if (document.getElementById('pg-connections').classList.contains('on')) loadConnections();
  }, 5000);
});
</script>
</body></html>"""

# ===== صفحه ساب‌لینک =====
def get_sub_page_html(uuid: str, link: dict) -> str:
    from datetime import datetime
    used = link.get('used_bytes', 0)
    limit = link.get('limit_bytes', 0)
    active = link.get('active', True)
    expired = link.get('expired', False)
    label = link.get('label', 'کاربر')
    fingerprint = link.get('fingerprint', 'chrome')
    max_devices = link.get('max_devices', 0)
    protocol = link.get('protocol', 'vless-ws')
    port = link.get('port', 443)
    active_connections = link.get('active_connections', 0)
    active_connections_list = link.get('active_connections_list', [])
    last_connected = link.get('last_connected_at')
    last_connected_text = "—"
    if last_connected:
        try:
            dt = datetime.fromisoformat(last_connected)
            last_connected_text = dt.strftime("%Y-%m-%d %H:%M")
        except:
            last_connected_text = last_connected[:16]
    percent = 0
    if limit > 0:
        percent = min(100, (used / limit) * 100)
    expires_at = link.get('expires_at')
    if expires_at:
        try:
            exp_date = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
            days_left = (exp_date - datetime.now().astimezone()).days
            if days_left < 0:
                days_left = 0
        except:
            days_left = 'نامشخص'
    else:
        days_left = 'نامحدود'
    is_allowed = active and not expired
    sub_url = link.get('sub_url', '')
    def fmt_bytes(b):
        if not b or b == 0:
            return '0 B'
        if b < 1024:
            return f'{b} B'
        if b < 1024**2:
            return f'{b/1024:.1f} KB'
        if b < 1024**3:
            return f'{b/1024**2:.2f} MB'
        return f'{b/1024**3:.2f} GB'
    used_fmt = fmt_bytes(used)
    limit_fmt = 'نامحدود' if limit == 0 else fmt_bytes(limit)
    from main import get_host, generate_vless_link
    host = get_host()
    remark = f"عقاب-{label}"
    new_vless_link = generate_vless_link(uuid, host, remark=remark, protocol=protocol, fingerprint=fingerprint, port=port)
    
    conns_html = ""
    if active_connections > 0:
        conns_html = f"""
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.04);border-radius:10px;padding:8px 10px;margin:8px 0">
            <div style="display:flex;align-items:center;gap:4px;margin-bottom:4px;font-size:9px;color:#8A4A3A">
                <span style="display:inline-block;width:5px;height:5px;border-radius:50%;background:#34D399;animation:pulse 1.5s infinite"></span>
                <span style="font-weight:700;color:#34D399;font-size:9px">{active_connections} دستگاه متصل</span>
            </div>
            <div style="display:flex;flex-wrap:wrap;gap:3px">"""
        for conn in active_connections_list[:10]:
            ip = conn.get('ip', 'نامشخص')
            conns_html += f"""<span style="font-family:monospace;font-size:8px;background:rgba(255,80,20,0.06);border:1px solid rgba(255,80,20,0.06);padding:1px 6px;border-radius:3px;color:#8A4A3A">🔵 {ip}</span>"""
        if len(active_connections_list) > 10:
            conns_html += f"""<span style="font-family:monospace;font-size:8px;background:rgba(255,80,20,0.04);padding:1px 6px;border-radius:3px;color:#5A3A2A">+{len(active_connections_list)-10}</span>"""
        conns_html += "</div></div>"
    else:
        conns_html = f"""<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.04);border-radius:10px;padding:6px 10px;margin:8px 0;text-align:center"><span style="font-size:9px;color:#5A3A2A">🔴 بدون اتصال فعال</span></div>"""
    
    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>🦅 {label}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>*{{margin:0;padding:0;box-sizing:border-box}}@keyframes fireBG{{0%{{background-position:0% 50%}}25%{{background-position:50% 0%}}50%{{background-position:100% 50%}}75%{{background-position:50% 100%}}100%{{background-position:0% 50%}}}}@keyframes flameFlicker{{0%{{opacity:0.6;transform:scale(1)}}50%{{opacity:1;transform:scale(1.02)}}100%{{opacity:0.6;transform:scale(1)}}}}@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}body{{font-family:'Vazirmatn',sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:16px;color:#F0EEFF;background:linear-gradient(135deg,#0a0a0f,#1a0a0a,#0a0a1a);background-size:400% 400%;animation:fireBG 8s ease infinite;}}
.fire-particles{{position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden;}}.fire-particle{{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(255,120,50,0.3),rgba(255,50,0,0));width:5px;height:5px;animation:floatFire 12s ease-in-out infinite;}}@keyframes floatFire{{0%{{transform:translateY(100vh) scale(0) rotate(0deg);opacity:0}}20%{{opacity:1}}80%{{opacity:1}}100%{{transform:translateY(-10vh) scale(1.5) rotate(720deg);opacity:0}}}}
.fire-glow{{position:fixed;border-radius:50%;filter:blur(150px);z-index:0;animation:flameFlicker 3s ease-in-out infinite;pointer-events:none;}}.glow1{{width:350px;height:350px;background:rgba(255,80,20,0.04);top:-120px;right:-60px}}.glow2{{width:250px;height:250px;background:rgba(255,150,50,0.03);bottom:-60px;left:-40px;animation-delay:2s}}
.card{{position:relative;z-index:10;background:rgba(15,15,30,0.8);backdrop-filter:blur(30px);border:1px solid rgba(255,255,255,0.04);border-radius:20px;padding:24px 22px 20px;max-width:420px;width:100%;box-shadow:0 0 60px rgba(0,0,0,0.4);animation:cardIn 0.6s ease;}}@keyframes cardIn{{from{{opacity:0;transform:translateY(20px) scale(0.97)}}to{{opacity:1;transform:translateY(0) scale(1)}}}}
.brand{{display:flex;align-items:center;gap:10px;margin-bottom:16px;padding-bottom:10px;border-bottom:1px solid rgba(255,255,255,0.03);}}.brand-icon{{width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,#FF6B35,#FF4500);display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;box-shadow:0 0 30px rgba(255,80,20,0.1);}}.brand-text .name{{font-size:13px;font-weight:800;background:linear-gradient(135deg,#FF8C00,#FF4500,#FF6B35);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}.brand-text .sub{{font-size:7px;color:#8A4A3A;margin-top:0px}}
.user-header{{display:flex;align-items:center;justify-content:space-between;margin-bottom:2px}}.user-name{{font-size:17px;font-weight:800;color:#F0EEFF;display:flex;align-items:center;gap:4px}}.user-name .fire{{font-size:15px}}
.status{{display:inline-flex;align-items:center;gap:3px;padding:2px 10px;border-radius:12px;font-size:9px;font-weight:700;}}.status.active{{background:rgba(255,80,20,0.12);color:#FF8C00;border:1px solid rgba(255,80,20,0.1);}}.status.inactive{{background:rgba(239,68,68,0.12);color:#F87171;border:1px solid rgba(239,68,68,0.1);}}
.uuid-box{{background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.03);border-radius:6px;padding:4px 8px;font-size:8px;font-family:monospace;color:#8A4A3A;word-break:break-all;margin:3px 0 8px;cursor:pointer}}.uuid-box:hover{{background:rgba(255,80,20,0.04)}}
.info-grid{{display:grid;gap:5px;margin:8px 0}}.info-item{{background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.02);border-radius:6px;padding:6px 10px;display:flex;justify-content:space-between;align-items:center}}.info-label{{font-size:9px;color:#8A4A3A;display:flex;align-items:center;gap:3px}}.info-label i{{font-size:10px;color:#FF6B35}}.info-value{{font-size:11px;font-weight:700;color:#F0EEFF}}.info-value.used{{color:#FF8C00}}.info-value.proto{{font-size:8px;background:rgba(255,80,20,0.05);padding:1px 6px;border-radius:4px;border:1px solid rgba(255,80,20,0.04);}}
.progress{{margin:8px 0 10px}}.progress-bar{{height:3px;border-radius:3px;background:rgba(255,255,255,0.03);overflow:hidden}}.progress-fill{{height:100%;border-radius:3px;background:linear-gradient(90deg,#FF6B35,#FF4500,#FF8C00);width:{percent:.1f}%;transition:width 1s ease}}.progress-text{{display:flex;justify-content:space-between;font-size:8px;color:#8A4A3A;margin-top:2px}}.progress-text .pct{{font-weight:700;color:#F0EEFF}}
.vless-section{{background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.03);border-radius:8px;padding:8px 10px;margin:8px 0}}.vless-label{{font-size:7px;color:#8A4A3A;font-weight:700;text-transform:uppercase;letter-spacing:.04em;display:flex;align-items:center;gap:4px;margin-bottom:4px}}.vless-label i{{color:#FF6B35;font-size:10px}}.vless-link{{font-family:monospace;font-size:8px;color:#FF8C00;word-break:break-all;line-height:1.5;background:rgba(0,0,0,0.2);padding:4px 6px;border-radius:4px;border:1px solid rgba(255,80,20,0.03);}}
.actions{{display:flex;gap:4px;margin-top:8px;flex-wrap:wrap}}.btn{{font-family:inherit;font-size:9px;font-weight:600;border-radius:6px;padding:5px 10px;cursor:pointer;display:inline-flex;align-items:center;gap:3px;border:none;transition:all .2s;white-space:nowrap;flex:1;justify-content:center}}.btn i{{font-size:11px}}
.btn-primary{{background:linear-gradient(135deg,#FF6B35,#FF4500);color:#fff;box-shadow:0 3px 15px rgba(255,80,20,0.15)}}.btn-primary:hover{{transform:translateY(-1px);box-shadow:0 6px 25px rgba(255,80,20,0.25)}}
.btn-secondary{{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.04);color:#8A4A3A}}.btn-secondary:hover{{background:rgba(255,255,255,0.06);color:#F0EEFF}}
.btn-success{{background:rgba(16,185,129,0.06);border:1px solid rgba(16,185,129,0.08);color:#34D399}}.btn-success:hover{{background:rgba(16,185,129,0.1)}}
.footer{{margin-top:12px;padding-top:10px;border-top:1px solid rgba(255,255,255,0.02);text-align:center;font-size:7px;color:#5A3A2A}}.footer .eagle{{color:#FF6B35;font-weight:700}}
.toast{{position:fixed;bottom:16px;left:50%;transform:translateX(-50%) translateY(40px);background:rgba(15,15,30,0.9);backdrop-filter:blur(20px);border:1px solid rgba(255,80,20,0.08);color:#F0EEFF;border-radius:8px;padding:6px 14px;font-size:10px;opacity:0;transition:all .3s;z-index:999;pointer-events:none;display:flex;align-items:center;gap:4px;box-shadow:0 8px 30px rgba(0,0,0,0.3)}}.toast.show{{opacity:1;transform:translateX(-50%) translateY(0)}}.toast.ok{{border-color:rgba(16,185,129,0.15);color:#34D399}}
@media(max-width:400px){{.card{{padding:16px 14px 14px}}.user-name{{font-size:15px}}.brand-icon{{width:30px;height:30px;font-size:14px}}.info-item{{padding:4px 8px}}.btn{{font-size:8px;padding:4px 8px}}}}
</style>
</head>
<body>
<div class="fire-particles"><div class="fire-particle" style="left:5%;animation-delay:0s;width:5px;height:5px"></div><div class="fire-particle" style="left:35%;animation-delay:3s;width:6px;height:6px"></div><div class="fire-particle" style="left:65%;animation-delay:5s;width:4px;height:4px"></div><div class="fire-particle" style="left:85%;animation-delay:7s;width:5px;height:5px"></div></div>
<div class="fire-glow glow1"></div><div class="fire-glow glow2"></div>
<div class="toast" id="toast"></div>
<div class="card">
    <div class="brand"><div class="brand-icon">🦅</div><div class="brand-text"><div class="name">پنل عقاب</div><div class="sub">اطلاعات اشتراک</div></div></div>
    <div class="user-header"><div class="user-name"><span class="fire">🦅</span> {label}</div><span class="status {'active' if is_allowed else 'inactive'}"><i class="ti {'ti-circle-check' if is_allowed else 'ti-circle-x'}"></i>{'فعال' if is_allowed else 'غیرفعال'}</span></div>
    <div class="uuid-box" onclick="copyUUID()">🔑 {uuid}</div>
    {conns_html}
    <div class="info-grid">
        <div class="info-item"><span class="info-label"><i class="ti ti-database"></i> مصرف</span><span class="info-value used">{used_fmt}</span></div>
        <div class="info-item"><span class="info-label"><i class="ti ti-package"></i> سهمیه</span><span class="info-value">{limit_fmt}</span></div>
        <div class="info-item"><span class="info-label"><i class="ti ti-calendar"></i> باقیمانده</span><span class="info-value">{days_left if days_left == 'نامحدود' else f'{days_left} روز'}</span></div>
        <div class="info-item"><span class="info-label"><i class="ti ti-devices"></i> دستگاه</span><span class="info-value">{max_devices if max_devices > 0 else '∞'}</span></div>
        <div class="info-item"><span class="info-label"><i class="ti ti-clock"></i> آخرین اتصال</span><span class="info-value" style="font-size:9px;">{last_connected_text}</span></div>
        <div class="info-item"><span class="info-label"><i class="ti ti-fingerprint"></i> FP</span><span class="info-value proto">{fingerprint}</span></div>
        <div class="info-item"><span class="info-label"><i class="ti ti-settings"></i> پروتکل</span><span class="info-value proto">{protocol}</span></div>
        <div class="info-item"><span class="info-label"><i class="ti ti-plug"></i> پورت</span><span class="info-value proto">{port}</span></div>
    </div>
    <div class="progress"><div class="progress-bar"><div class="progress-fill" style="width:{percent:.1f}%"></div></div><div class="progress-text"><span>میزان مصرف</span><span class="pct">{percent:.1f}%</span></div></div>
    <div class="vless-section"><div class="vless-label"><i class="ti ti-link"></i> لینک کانفیگ</div><div class="vless-link" id="vless-link">{new_vless_link}</div></div>
    <div class="actions"><button class="btn btn-primary" onclick="copyVless()"><i class="ti ti-copy"></i> کپی</button><button class="btn btn-success" onclick="copySub()"><i class="ti ti-link"></i> ساب</button><button class="btn btn-secondary" onclick="showQR()"><i class="ti ti-qrcode"></i> QR</button></div>
    <div class="footer"><span class="eagle">🦅</span> پنل عقاب</div>
</div>
<script>const vless=`{new_vless_link}`;const subUrl=`{sub_url}`;const uuid=`{uuid}`;function toast(msg,type=''){{const t=document.getElementById('toast');t.textContent=msg;t.className='toast show'+(type?' '+type:'');setTimeout(()=>t.classList.remove('show'),2000);}}function copyVless(){{navigator.clipboard.writeText(vless).then(()=>toast('✅ کپی شد','ok'));}}function copySub(){{navigator.clipboard.writeText(subUrl).then(()=>toast('✅ کپی شد','ok'));}}function copyUUID(){{navigator.clipboard.writeText(uuid).then(()=>toast('✅ کپی شد','ok'));}}function showQR(){{window.open('https://api.qrserver.com/v1/create-qr-code/?size=250x250&data='+encodeURIComponent(vless),'_blank');}}</script>
</body></html>"""
