# pages.py - پنل عقاب (نسخه کامل با آیپی تمیز + تغییر رمز + ربات تلگرام)

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
:root{
    --bg:#0b0d1a;
    --bg2:#111329;
    --bg3:#181b3a;
    --card:#141632;
    --card-border:#2a2d5a;
    --primary:#4f8cff;
    --primary-dark:#3a6fd6;
    --secondary:#b388ff;
    --accent:#ff6b35;
    --text:#f0f0ff;
    --text-dim:#7a7aaa;
    --text-muted:#4a4a7a;
}
body{
    font-family:'Vazirmatn',sans-serif;
    background:var(--bg);
    min-height:100vh;
    display:flex;
    align-items:center;
    justify-content:center;
    padding:20px;
    background:radial-gradient(ellipse at 20% 50%, #141632 0%, #0b0d1a 100%);
}
.card{
    background:var(--card);
    border:1px solid var(--card-border);
    border-radius:24px;
    padding:44px 40px 36px;
    max-width:420px;
    width:100%;
    box-shadow:0 25px 60px rgba(0,0,0,0.6);
}
.brand{
    display:flex;
    align-items:center;
    gap:14px;
    margin-bottom:30px;
}
.brand-icon{
    width:52px;height:52px;
    border-radius:14px;
    background:linear-gradient(135deg,var(--primary),var(--secondary));
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:26px;
    box-shadow:0 8px 30px rgba(79,140,255,0.25);
}
.brand-name{
    font-size:20px;font-weight:800;
    background:linear-gradient(135deg,var(--primary),var(--secondary));
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.brand-sub{
    font-size:11px;color:var(--text-dim);margin-top:2px;
}
h1{
    font-size:20px;font-weight:700;color:var(--text);margin-bottom:4px;
}
.sub{
    font-size:12px;color:var(--text-dim);margin-bottom:22px;line-height:1.7;
}
.hint{
    background:rgba(79,140,255,0.06);
    border:1px solid rgba(79,140,255,0.1);
    border-radius:12px;
    padding:10px 16px;
    margin-bottom:20px;
    display:flex;
    align-items:center;
    justify-content:space-between;
}
.hint-label{
    font-size:11px;color:var(--text-dim);
}
.hint-val{
    font-family:monospace;font-size:13px;font-weight:700;
    color:var(--primary);
    background:rgba(79,140,255,0.1);
    padding:3px 14px;
    border-radius:8px;
    cursor:pointer;
    transition:.2s;
}
.hint-val:hover{
    background:rgba(79,140,255,0.2);
}
.field{
    margin-bottom:18px;
}
.field label{
    display:block;
    font-size:10.5px;font-weight:600;
    color:var(--text-dim);
    margin-bottom:6px;
    text-transform:uppercase;
    letter-spacing:.06em;
}
.inp-wrap{
    position:relative;
}
input[type=password]{
    width:100%;
    padding:13px 48px 13px 16px;
    border-radius:12px;
    border:1px solid var(--card-border);
    background:rgba(0,0,0,0.25);
    color:var(--text);
    font-family:inherit;
    font-size:14px;
    outline:none;
    transition:.3s;
}
input[type=password]:focus{
    border-color:var(--primary);
    box-shadow:0 0 0 4px rgba(79,140,255,0.08);
    background:rgba(0,0,0,0.35);
}
.ic{
    position:absolute;
    left:14px;
    top:50%;
    transform:translateY(-50%);
    color:var(--text-dim);
    font-size:18px;
}
input:focus + .ic{
    color:var(--primary);
}
.err{
    display:none;
    background:rgba(239,68,68,0.08);
    border:1px solid rgba(239,68,68,0.15);
    border-radius:10px;
    padding:10px 14px;
    margin-bottom:14px;
    font-size:12px;
    color:#f87171;
    align-items:center;
    gap:8px;
}
.err.show{display:flex}
.btn{
    width:100%;
    padding:14px;
    border-radius:12px;
    border:none;
    cursor:pointer;
    background:linear-gradient(135deg,var(--primary),var(--secondary));
    color:#fff;
    font-family:inherit;
    font-size:14px;
    font-weight:700;
    display:flex;
    align-items:center;
    justify-content:center;
    gap:10px;
    box-shadow:0 4px 30px rgba(79,140,255,0.25);
    transition:all .3s;
}
.btn:hover{
    transform:translateY(-2px);
    box-shadow:0 8px 40px rgba(79,140,255,0.35);
}
.btn:disabled{
    opacity:.5;cursor:not-allowed;transform:none;
}
.footer{
    margin-top:22px;
    padding-top:18px;
    border-top:1px solid rgba(255,255,255,0.04);
    display:flex;
    align-items:center;
    justify-content:center;
    gap:8px;
    font-size:10.5px;
    color:var(--text-dim);
}
.footer button{
    background:none;
    border:none;
    color:var(--primary);
    cursor:pointer;
    font-weight:600;
    font-family:inherit;
    font-size:10.5px;
    display:flex;
    align-items:center;
    gap:4px;
    transition:.3s;
}
.footer button:hover{
    color:var(--secondary);
}
@keyframes spin{to{transform:rotate(360deg)}}
</style>
</head>
<body>
<div class="card">
    <div class="brand">
        <div class="brand-icon">🦅</div>
        <div>
            <div class="brand-name">پنل عقاب</div>
            <div class="brand-sub">مدیریت کاربران</div>
        </div>
    </div>
    <h1>ورود به پنل عقاب</h1>
    <p class="sub">رمز عبور را برای دسترسی به داشبورد وارد کنید</p>
    <div class="err" id="err"><i class="ti ti-alert-circle"></i><span id="err-text"></span></div>
    <div class="hint">
        <span class="hint-label">رمز پیش‌فرض</span>
        <span class="hint-val" onclick="document.getElementById('pw').value='123456';document.getElementById('pw').focus()">123456</span>
    </div>
    <form id="form">
        <div class="field">
            <label>رمز عبور</label>
            <div class="inp-wrap">
                <input type="password" id="pw" placeholder="رمز عبور را وارد کنید" autofocus required>
                <i class="ti ti-lock ic"></i>
            </div>
        </div>
        <button class="btn" type="submit" id="btn"><i class="ti ti-login-2"></i> ورود به پنل</button>
    </form>
    <div class="footer">
        🦅 پنل عقاب · v10.0 · <button onclick="toggleTheme()"><i class="ti ti-palette"></i> تغییر تم</button>
    </div>
</div>
<script>
let currentTheme = localStorage.getItem('eagle-theme') || 'dark';
function applyTheme(theme){document.documentElement.setAttribute('data-theme',theme);localStorage.setItem('eagle-theme',theme);}
function toggleTheme(){currentTheme=currentTheme==='dark'?'white':'dark';applyTheme(currentTheme);}
applyTheme(currentTheme);
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

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🦅 پنل عقاب · مدیریت کاربران</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}

:root{
    --bg:#0b0d1a;
    --bg2:#111329;
    --bg3:#181b3a;
    --card:#141632;
    --card-hover:#1a1d42;
    --card-border:#2a2d5a;
    --card-border-hover:#3a3d7a;
    --primary:#4f8cff;
    --primary-dark:#3a6fd6;
    --secondary:#b388ff;
    --accent:#ff6b35;
    --green:#10b981;
    --green-bg:rgba(16,185,129,0.08);
    --red:#ef4444;
    --red-bg:rgba(239,68,68,0.08);
    --amber:#f59e0b;
    --amber-bg:rgba(245,158,11,0.08);
    --text:#f0f0ff;
    --text-dim:#7a7aaa;
    --text-muted:#4a4a7a;
    --sidebar-w:220px;
    --radius:16px;
    --shadow:0 8px 32px rgba(0,0,0,0.4),0 0 60px rgba(79,140,255,0.02);
}

[data-theme="white"]{
    --bg:#f0f0f8;
    --bg2:#e8e8f2;
    --bg3:#ddddea;
    --card:#ffffff;
    --card-hover:#f5f5ff;
    --card-border:#d0d0e0;
    --card-border-hover:#b0b0d0;
    --text:#1a1a2e;
    --text-dim:#5a5a7a;
    --text-muted:#8a8aaa;
    --shadow:0 8px 32px rgba(0,0,0,0.06);
}

html,body{height:100%}
body{
    font-family:'Vazirmatn',sans-serif;
    background:var(--bg);
    color:var(--text);
    min-height:100vh;
    display:flex;
    font-size:14px;
    transition:background .3s,color .3s;
    background:radial-gradient(ellipse at 80% 20%, #141632 0%, #0b0d1a 100%);
}
[data-theme="white"] body{
    background:radial-gradient(ellipse at 80% 20%, #e8e8f2 0%, #f0f0f8 100%);
}

.sidebar{
    width:var(--sidebar-w);
    min-height:100vh;
    background:var(--card);
    backdrop-filter:blur(20px);
    -webkit-backdrop-filter:blur(20px);
    border-left:1px solid var(--card-border);
    display:flex;
    flex-direction:column;
    flex-shrink:0;
    position:fixed;
    right:0;top:0;bottom:0;
    z-index:200;
    transition:transform .3s cubic-bezier(.4,0,.2,1),background .3s;
    box-shadow:var(--shadow);
}
.logo{
    display:flex;
    align-items:center;
    gap:12px;
    padding:20px 16px 16px;
    border-bottom:1px solid var(--card-border);
}
.logo-icon{
    width:40px;height:40px;
    border-radius:12px;
    background:linear-gradient(135deg,var(--primary),var(--secondary));
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:20px;
    flex-shrink:0;
    box-shadow:0 4px 20px rgba(79,140,255,0.2);
}
.logo-name{
    font-size:14px;
    font-weight:800;
    background:linear-gradient(135deg,var(--primary),var(--secondary));
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.logo-sub{
    font-size:8.5px;
    color:var(--text-dim);
    margin-top:1px;
}
.nav-wrap{
    flex:1;
    overflow-y:auto;
    padding:12px 10px;
}
.nav-it{
    display:flex;
    align-items:center;
    gap:10px;
    padding:10px 14px;
    color:var(--text-dim);
    font-size:12.5px;
    cursor:pointer;
    border-radius:10px;
    transition:all .2s;
    margin:2px 0;
}
.nav-it i{
    font-size:16px;
    width:20px;
    text-align:center;
    flex-shrink:0;
}
.nav-it:hover{
    background:rgba(79,140,255,0.06);
    color:var(--text);
}
.nav-it.on{
    background:linear-gradient(135deg,rgba(79,140,255,0.12),rgba(179,136,255,0.06));
    color:var(--primary);
    font-weight:600;
    border:1px solid rgba(79,140,255,0.1);
}
.nav-badge{
    margin-right:auto;
    background:linear-gradient(135deg,var(--primary),var(--secondary));
    color:#fff;
    font-size:8px;
    padding:1px 8px;
    border-radius:12px;
    font-weight:700;
}
.sb-foot{
    padding:12px 12px;
    border-top:1px solid var(--card-border);
}
.theme-btn{
    display:flex;
    align-items:center;
    justify-content:center;
    gap:6px;
    background:rgba(79,140,255,0.06);
    color:var(--text-dim);
    border-radius:10px;
    padding:8px;
    font-size:10.5px;
    font-weight:500;
    font-family:inherit;
    border:1px solid var(--card-border);
    cursor:pointer;
    width:100%;
    transition:.2s;
    margin-bottom:6px;
}
.theme-btn:hover{
    background:rgba(79,140,255,0.12);
    color:var(--text);
}
.logout-btn{
    display:flex;
    align-items:center;
    justify-content:center;
    gap:6px;
    background:var(--red-bg);
    color:#f87171;
    border-radius:10px;
    padding:8px;
    font-size:11px;
    font-weight:500;
    font-family:inherit;
    border:1px solid rgba(239,68,68,0.12);
    cursor:pointer;
    width:100%;
    transition:.2s;
}
.logout-btn:hover{
    background:rgba(239,68,68,0.15);
}

.mob-top{
    display:none;
    position:fixed;
    top:0;right:0;left:0;
    height:56px;
    background:var(--card);
    backdrop-filter:blur(20px);
    -webkit-backdrop-filter:blur(20px);
    border-bottom:1px solid var(--card-border);
    z-index:150;
    align-items:center;
    justify-content:space-between;
    padding:0 14px;
}
.mob-top .ml{display:flex;align-items:center;gap:10px}
.mob-logo{
    width:32px;height:32px;
    border-radius:10px;
    background:linear-gradient(135deg,var(--primary),var(--secondary));
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:16px;
}
.mob-title{
    color:var(--text);
    font-size:13px;font-weight:700;
}
.mob-right{display:flex;gap:6px}
.menu-btn,.theme-mob{
    background:rgba(79,140,255,0.06);
    border:1px solid var(--card-border);
    color:var(--text-dim);
    width:36px;height:36px;
    border-radius:9px;
    font-size:17px;
    display:flex;
    align-items:center;
    justify-content:center;
    cursor:pointer;
    transition:.2s;
}
.menu-btn:hover,.theme-mob:hover{
    background:rgba(79,140,255,0.12);
    color:var(--text);
}
.overlay{
    display:none;
    position:fixed;
    inset:0;
    background:rgba(0,0,0,.5);
    z-index:190;
    backdrop-filter:blur(4px);
}
.overlay.show{display:block}

.main{
    margin-right:var(--sidebar-w);
    flex:1;
    padding:24px 28px 40px;
    min-width:0;
    transition:margin .3s;
}
.pg{
    display:none;
    animation:pageIn .3s ease;
}
.pg.on{display:block}
@keyframes pageIn{
    from{opacity:0;transform:translateY(8px)}
    to{opacity:1;transform:translateY(0)}
}

.topbar{
    display:flex;
    align-items:center;
    justify-content:space-between;
    margin-bottom:22px;
    flex-wrap:wrap;
    gap:10px;
}
.tb-title{
    font-size:18px;
    font-weight:700;
    color:var(--text);
    display:flex;
    align-items:center;
    gap:8px;
}
.tb-title i{
    color:var(--primary);
    font-size:20px;
}
.tb-sub{
    font-size:11px;
    color:var(--text-dim);
    margin-top:2px;
}
.tb-right{
    display:flex;
    align-items:center;
    gap:8px;
    flex-wrap:wrap;
}
.badge{
    font-size:10px;
    padding:4px 12px;
    border-radius:20px;
    font-weight:600;
    display:inline-flex;
    align-items:center;
    gap:5px;
    white-space:nowrap;
}
.bg-primary{
    background:rgba(79,140,255,0.1);
    color:var(--primary);
}
.bg-green{
    background:var(--green-bg);
    color:var(--green);
}
.bg-red{
    background:var(--red-bg);
    color:#f87171;
}
.bg-fire{
    background:rgba(255,107,53,0.1);
    color:var(--accent);
}
.dot{
    width:6px;height:6px;border-radius:50%;
    flex-shrink:0;display:inline-block;
}
.dg{background:var(--green)}
.dr{background:var(--red)}
.da{background:var(--amber)}
.db{background:var(--primary)}
.pulse{animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}

.stats-grid{
    display:grid;
    grid-template-columns:repeat(6,1fr);
    gap:14px;
    margin-bottom:22px;
}
.stat-card{
    background:var(--card);
    border:1px solid var(--card-border);
    border-radius:var(--radius);
    padding:18px 14px;
    text-align:center;
    transition:all .3s;
    position:relative;
    min-height:100px;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
}
.stat-card:hover{
    border-color:var(--card-border-hover);
    transform:translateY(-3px);
    background:var(--card-hover);
    box-shadow:var(--shadow);
}
.stat-card .icon{
    font-size:22px;
    margin-bottom:4px;
    display:block;
    opacity:.6;
}
.stat-card .number{
    font-size:26px;
    font-weight:800;
    color:var(--text);
    line-height:1.2;
}
.stat-card .label{
    font-size:10.5px;
    color:var(--text-dim);
    margin-top:2px;
    font-weight:500;
}
.stat-card .sub{
    font-size:9px;
    color:var(--text-muted);
    margin-top:1px;
}
.stat-card .bar{
    position:absolute;
    bottom:0;right:0;left:0;
    height:3px;
    background:linear-gradient(90deg,var(--primary),var(--secondary));
    opacity:0;
    border-radius:0 0 var(--radius) var(--radius);
    transition:.3s;
}
.stat-card:hover .bar{opacity:1}

.user-grid{
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(400px,1fr));
    gap:14px;
}
.user-card{
    background:var(--card);
    border:1px solid var(--card-border);
    border-radius:var(--radius);
    padding:16px 18px;
    transition:all .3s;
}
.user-card:hover{
    border-color:var(--card-border-hover);
    transform:translateY(-2px);
    background:var(--card-hover);
}
.user-card .head{
    display:flex;
    align-items:center;
    justify-content:space-between;
    margin-bottom:4px;
}
.user-card .name{
    font-size:13px;
    font-weight:700;
    color:var(--text);
    display:flex;
    align-items:center;
    gap:6px;
}
.user-card .status{
    font-size:9.5px;
    font-weight:600;
    padding:3px 12px;
    border-radius:12px;
}
.user-card .status.on{
    background:var(--green-bg);
    color:var(--green);
}
.user-card .status.off{
    background:var(--red-bg);
    color:#f87171;
}
.user-card .uuid{
    font-family:monospace;
    font-size:9px;
    color:var(--text-dim);
    margin-bottom:6px;
    word-break:break-all;
}
.user-card .info{
    display:flex;
    justify-content:space-between;
    font-size:10.5px;
    color:var(--text-dim);
    gap:6px;
    flex-wrap:wrap;
    margin-bottom:4px;
}
.user-card .quota-info{
    display:flex;
    justify-content:space-between;
    font-size:10.5px;
    color:var(--text-dim);
    margin-bottom:3px;
}
.user-card .quota-bar{
    height:5px;
    border-radius:4px;
    background:rgba(79,140,255,0.08);
    overflow:hidden;
    margin-bottom:8px;
}
.user-card .quota-fill{
    height:100%;
    border-radius:4px;
    background:linear-gradient(90deg,var(--primary),var(--secondary));
    transition:width .6s ease;
}
.user-card .actions{
    display:flex;
    gap:4px;
    flex-wrap:wrap;
    margin-top:6px;
}
.user-card .actions .btn{flex:1;justify-content:center;min-width:fit-content;font-size:9.5px;}
.user-card .lock-badge{
    display:inline-flex;
    align-items:center;
    gap:3px;
    font-size:8.5px;
    color:var(--amber);
    background:var(--amber-bg);
    padding:2px 8px;
    border-radius:10px;
}

.user-card .clean-ips-box{
    margin-top:8px;
    border-top:1px solid var(--card-border);
    padding-top:8px;
}
.user-card .clean-ips-box .cip-title{
    font-size:9.5px;
    color:var(--text-dim);
    display:flex;
    align-items:center;
    gap:4px;
    margin-bottom:4px;
    font-weight:600;
}
.user-card .clean-ips-box .cip-title i{
    font-size:13px;
    color:var(--primary);
}
.user-card .clean-ips-box .cip-list{
    display:flex;
    flex-wrap:wrap;
    gap:3px;
}
.user-card .clean-ips-box .cip-item{
    font-family:monospace;
    font-size:9px;
    background:rgba(79,140,255,0.06);
    border:1px solid rgba(79,140,255,0.06);
    padding:2px 8px;
    border-radius:6px;
    color:var(--text-dim);
    display:flex;
    align-items:center;
    gap:4px;
}
.user-card .clean-ips-box .cip-item .del-cip{
    cursor:pointer;
    color:var(--red);
    font-size:10px;
    opacity:.5;
    transition:.2s;
}
.user-card .clean-ips-box .cip-item .del-cip:hover{
    opacity:1;
}
.user-card .clean-ips-box .cip-input-group{
    display:flex;
    gap:4px;
    margin-top:4px;
}
.user-card .clean-ips-box .cip-input-group input{
    flex:1;
    padding:4px 8px;
    border-radius:6px;
    border:1px solid var(--card-border);
    background:rgba(0,0,0,0.15);
    color:var(--text);
    font-family:monospace;
    font-size:9px;
    outline:none;
    transition:.2s;
    min-width:80px;
}
.user-card .clean-ips-box .cip-input-group input:focus{
    border-color:var(--primary);
}
.user-card .clean-ips-box .cip-input-group .btn{
    font-size:8.5px;
    padding:3px 10px;
}
.user-card .clean-ips-box .cip-empty{
    font-size:9px;
    color:var(--text-muted);
}
.user-card .warning-box{
    background:rgba(239,68,68,0.04);
    border:1px solid rgba(239,68,68,0.08);
    border-radius:6px;
    padding:4px 8px;
    margin-top:4px;
    font-size:7.5px;
    color:#f87171;
    font-family:monospace;
    white-space:pre-wrap;
    max-height:50px;
    overflow-y:auto;
    direction:ltr;
    text-align:left;
    line-height:1.4;
}
.empty{
    text-align:center;
    padding:50px 20px;
    color:var(--text-dim);
}
.empty i{
    font-size:38px;
    opacity:.3;
    display:block;
    margin-bottom:12px;
}

.btn{
    font-family:inherit;
    font-size:11px;
    font-weight:600;
    border-radius:10px;
    padding:7px 14px;
    cursor:pointer;
    display:inline-flex;
    align-items:center;
    gap:5px;
    border:none;
    transition:all .2s;
    white-space:nowrap;
}
.btn i{font-size:12px}
.btn-p{
    background:linear-gradient(135deg,var(--primary),var(--secondary));
    color:#fff;
    box-shadow:0 4px 20px rgba(79,140,255,0.2);
}
.btn-p:hover{
    transform:translateY(-2px);
    box-shadow:0 8px 30px rgba(79,140,255,0.35);
}
.btn-o{
    background:var(--card);
    border:1px solid var(--card-border);
    color:var(--text-dim);
}
.btn-o:hover{
    background:rgba(79,140,255,0.06);
    border-color:rgba(79,140,255,0.2);
}
.btn-d{
    background:var(--red-bg);
    color:#f87171;
    border:1px solid rgba(239,68,68,0.12);
}
.btn-d:hover{
    background:rgba(239,68,68,0.15);
}
.btn-pur{
    background:rgba(179,136,255,0.08);
    color:var(--secondary);
    border:1px solid rgba(179,136,255,0.12);
}
.btn-pur:hover{
    background:rgba(179,136,255,0.15);
}
.btn-amber{
    background:var(--amber-bg);
    color:var(--amber);
    border:1px solid rgba(245,158,11,0.12);
}
.btn-amber:hover{
    background:rgba(245,158,11,0.15);
}
.btn-sm{padding:4px 10px;font-size:9.5px;border-radius:8px}
.btn-icon{width:28px;height:28px;padding:0;justify-content:center;border-radius:8px}

.toast{
    position:fixed;
    bottom:24px;
    left:50%;
    transform:translateX(-50%) translateY(50px);
    background:var(--card);
    backdrop-filter:blur(20px);
    -webkit-backdrop-filter:blur(20px);
    border:1px solid var(--card-border);
    color:var(--text);
    border-radius:12px;
    padding:10px 20px;
    font-size:12px;
    opacity:0;
    transition:all .3s;
    z-index:999;
    pointer-events:none;
    box-shadow:var(--shadow);
    white-space:nowrap;
    display:flex;
    align-items:center;
    gap:8px;
}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.toast.ok{border-color:rgba(16,185,129,.2);color:var(--green)}
.toast.err{border-color:rgba(239,68,68,.2);color:#f87171}

.modal-bg{
    display:none;
    position:fixed;
    inset:0;
    background:rgba(0,0,0,.6);
    z-index:500;
    align-items:center;
    justify-content:center;
    backdrop-filter:blur(6px);
}
.modal-bg.open{display:flex}
.modal{
    background:var(--card);
    backdrop-filter:blur(20px);
    -webkit-backdrop-filter:blur(20px);
    border:1px solid var(--card-border);
    border-radius:20px;
    padding:28px 26px;
    max-width:540px;
    width:calc(100% - 32px);
    max-height:90vh;
    overflow-y:auto;
    animation:pageIn .3s ease;
    box-shadow:var(--shadow);
}
.modal-close{
    position:absolute;top:12px;left:12px;
    background:rgba(79,140,255,0.06);
    border:1px solid var(--card-border);
    color:var(--text-dim);
    width:30px;height:30px;
    border-radius:9px;
    font-size:16px;
    display:flex;
    align-items:center;
    justify-content:center;
    cursor:pointer;
    border:none;
    transition:.2s;
}
.modal-close:hover{
    background:var(--red-bg);
    color:#f87171;
    transform:rotate(90deg);
}
.modal-title{
    font-size:15px;
    font-weight:700;
    color:var(--text);
    margin-bottom:18px;
    display:flex;
    align-items:center;
    gap:8px;
}
.modal-title i{
    color:var(--primary);
    font-size:17px;
}
.fg{
    display:flex;
    flex-direction:column;
    gap:4px;
    margin-bottom:10px;
}
.fg label{
    font-size:10px;
    color:var(--text-dim);
    font-weight:600;
    text-transform:uppercase;
    letter-spacing:.05em;
    display:flex;
    align-items:center;
    gap:4px;
}
.fi{
    width:100%;
    padding:9px 12px;
    border-radius:10px;
    border:1px solid var(--card-border);
    background:rgba(0,0,0,0.15);
    color:var(--text);
    font-family:inherit;
    font-size:12px;
    outline:none;
    transition:.2s;
}
.fi:focus{
    border-color:var(--primary);
    box-shadow:0 0 0 3px rgba(79,140,255,0.06);
    background:rgba(0,0,0,0.25);
}
.fi::placeholder{color:var(--text-muted)}
select.fi{appearance:none;cursor:pointer}

.conn-grid{
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(260px,1fr));
    gap:12px;
}
.conn-card{
    background:var(--card);
    border:1px solid var(--card-border);
    border-radius:14px;
    padding:13px 15px;
    transition:.2s;
}
.conn-card:hover{
    border-color:var(--card-border-hover);
}
.conn-card .ip{
    font-family:monospace;
    font-size:12px;
    font-weight:700;
    color:var(--text);
    display:flex;
    align-items:center;
    gap:6px;
}
.conn-card .label{
    font-size:10px;
    color:var(--text-dim);
    margin-top:2px;
}
.conn-card .conn-info{
    display:flex;
    justify-content:space-between;
    margin-top:6px;
    font-size:10px;
    color:var(--text-dim);
    gap:6px;
    flex-wrap:wrap;
}
.conn-status-dot{
    display:inline-block;
    width:6px;height:6px;
    border-radius:50%;
    background:var(--green);
    animation:pulse 1.5s infinite;
    margin-left:3px;
}

.settings-card{
    background:var(--card);
    border:1px solid var(--card-border);
    border-radius:var(--radius);
    padding:22px;
    max-width:560px;
}
.settings-card .title{
    font-size:15px;font-weight:700;
    color:var(--text);
    margin-bottom:14px;
    display:flex;align-items:center;gap:8px;
}
.settings-card .title i{color:var(--primary)}
.settings-card .field{margin-bottom:12px}
.settings-card .field label{
    font-size:10.5px;
    color:var(--text-dim);
    display:block;
    margin-bottom:3px;
    font-weight:600;
}
.settings-card .field input{
    width:100%;padding:9px 12px;
    border-radius:10px;
    border:1px solid var(--card-border);
    background:rgba(0,0,0,0.15);
    color:var(--text);
    font-family:inherit;
    font-size:12px;
    outline:none;
    transition:.2s;
}
.settings-card .field input:focus{
    border-color:var(--primary);
    box-shadow:0 0 0 3px rgba(79,140,255,0.06);
}
.settings-card .field input::placeholder{color:var(--text-muted)}
.settings-card .btn{width:100%;justify-content:center;margin-top:2px}
.settings-card .toggle-row{
    display:flex;align-items:center;justify-content:space-between;
    padding:10px 0;
    border-bottom:1px solid var(--card-border);
}
.settings-card .toggle-row .toggle-label{
    font-size:12.5px;
    color:var(--text-dim);
    display:flex;align-items:center;gap:8px;
}
.settings-card .toggle-row .toggle-label i{font-size:17px}
.switch{
    position:relative;width:44px;height:24px;
    background:var(--text-muted);
    border-radius:12px;
    cursor:pointer;transition:.3s;
    flex-shrink:0;
}
.switch.on{
    background:linear-gradient(135deg,var(--primary),var(--secondary));
}
.switch .slider{
    position:absolute;
    top:2px;right:2px;
    width:20px;height:20px;
    background:#fff;
    border-radius:50%;
    transition:.3s;
    box-shadow:0 2px 8px rgba(0,0,0,0.2);
}
.switch.on .slider{right:22px}

.telegram-status{
    margin-top:12px;padding:10px;
    border-radius:10px;
    background:rgba(79,140,255,0.04);
    border:1px solid var(--card-border);
    font-size:11px;
    color:var(--text-dim);
}

@media(max-width:1200px){.stats-grid{grid-template-columns:repeat(3,1fr)}}
@media(max-width:900px){.stats-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:768px){
    .sidebar{transform:translateX(100%)}
    .sidebar.open{transform:translateX(0)}
    .main{margin-right:0;padding-top:70px}
    .mob-top{display:flex}
    .user-grid{grid-template-columns:1fr}
    .stats-grid{grid-template-columns:1fr 1fr}
}
@media(max-width:500px){.stats-grid{grid-template-columns:1fr}.main{padding:64px 12px 30px}}
</style>
</head>
<body>

<div class="toast" id="toast"></div>

<!-- Modals -->
<div class="modal-bg" id="modal-user">
    <div class="modal">
        <button class="modal-close" onclick="closeModal('modal-user')"><i class="ti ti-x"></i></button>
        <div class="modal-title"><i class="ti ti-user-plus"></i> 🦅 ساخت کانفیگ جدید</div>
        <div class="fg"><label><i class="ti ti-tag"></i> نام کاربری</label><input class="fi" id="user-label" placeholder="مثلاً: کاربر علی"></div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px">
            <div class="fg"><label><i class="ti ti-database"></i> حجم</label><input class="fi" id="user-quota" type="number" min="0.5" step="0.5" value="2"></div>
            <div class="fg"><label><i class="ti ti-ruler"></i> واحد</label><select class="fi" id="user-unit"><option value="GB">GB</option><option value="MB">MB</option></select></div>
            <div class="fg"><label><i class="ti ti-calendar"></i> انقضا (روز)</label><input class="fi" id="user-exp" type="number" min="0" value="30" placeholder="0=نامحدود"></div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
            <div class="fg"><label><i class="ti ti-fingerprint"></i> فینگرپرینت</label><select class="fi" id="user-fingerprint"><option value="chrome">Chrome</option><option value="firefox">Firefox</option><option value="safari">Safari</option><option value="edge">Edge</option><option value="random">Random</option><option value="none">None</option></select></div>
            <div class="fg"><label><i class="ti ti-devices"></i> محدودیت دستگاه</label><input class="fi" id="user-devices" type="number" min="0" max="10" value="1" placeholder="0=نامحدود"></div>
        </div>
        <div class="fg"><label><i class="ti ti-settings"></i> پروتکل</label><select class="fi" id="user-protocol"><option value="vless-ws">VLESS (WebSocket)</option><option value="xhttp-stream-up">XHTTP (Stream)</option></select></div>
        <div class="fg"><label><i class="ti ti-plug"></i> پورت (پیش‌فرض: 443)</label><input class="fi" id="user-port" type="number" min="1" max="65535" value="443" placeholder="443"></div>
        <div class="fg"><label><i class="ti ti-lock"></i> رمز کانفیگ (اختیاری)</label><input class="fi" id="user-password" type="password" placeholder="برای حذف/ویرایش نیاز است" dir="ltr"></div>
        <div style="display:flex;gap:8px;margin-top:14px">
            <button class="btn btn-p" onclick="saveUser()" style="flex:2"><i class="ti ti-check"></i> ساخت کانفیگ</button>
            <button class="btn btn-o" onclick="closeModal('modal-user')" style="flex:1">انصراف</button>
        </div>
    </div>
</div>

<div class="modal-bg" id="modal-edit">
    <div class="modal">
        <button class="modal-close" onclick="closeModal('modal-edit')"><i class="ti ti-x"></i></button>
        <div class="modal-title"><i class="ti ti-edit"></i> 🦅 ویرایش کانفیگ</div>
        <input type="hidden" id="edit-uuid">
        <div class="fg" id="edit-password-section"><label><i class="ti ti-lock"></i> 🔑 رمز کانفیگ (برای ویرایش لازم است)</label><input class="fi" id="edit-password" type="password" placeholder="رمز کانفیگ را وارد کنید" dir="ltr"></div>
        <div class="fg"><label><i class="ti ti-tag"></i> نام کاربری</label><input class="fi" id="edit-label" placeholder="نام کاربری"></div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px">
            <div class="fg"><label><i class="ti ti-database"></i> حجم (0=نامحدود)</label><input class="fi" id="edit-quota" type="number" min="0" step="0.5"></div>
            <div class="fg"><label><i class="ti ti-ruler"></i> واحد</label><select class="fi" id="edit-unit"><option value="GB">GB</option><option value="MB">MB</option></select></div>
            <div class="fg"><label><i class="ti ti-calendar"></i> انقضا (روز)</label><input class="fi" id="edit-exp" type="number" min="0" placeholder="0=نامحدود"></div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
            <div class="fg"><label><i class="ti ti-fingerprint"></i> فینگرپرینت</label><select class="fi" id="edit-fingerprint"><option value="chrome">Chrome</option><option value="firefox">Firefox</option><option value="safari">Safari</option><option value="edge">Edge</option><option value="random">Random</option><option value="none">None</option></select></div>
            <div class="fg"><label><i class="ti ti-devices"></i> محدودیت دستگاه</label><input class="fi" id="edit-devices" type="number" min="0" max="10" placeholder="0=نامحدود"></div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
            <div class="fg"><label><i class="ti ti-settings"></i> پروتکل</label><select class="fi" id="edit-protocol"><option value="vless-ws">VLESS (WebSocket)</option><option value="xhttp-stream-up">XHTTP (Stream)</option></select></div>
            <div class="fg"><label><i class="ti ti-toggle-left"></i> وضعیت</label><select class="fi" id="edit-status"><option value="true">✅ فعال</option><option value="false">❌ غیرفعال</option></select></div>
        </div>
        <div class="fg"><label><i class="ti ti-plug"></i> پورت</label><input class="fi" id="edit-port" type="number" min="1" max="65535" placeholder="443"></div>
        <div style="display:flex;gap:8px;margin-top:14px">
            <button class="btn btn-p" onclick="saveEdit()" style="flex:2"><i class="ti ti-check"></i> ذخیره تغییرات</button>
            <button class="btn btn-o" onclick="closeModal('modal-edit')" style="flex:1">انصراف</button>
        </div>
    </div>
</div>

<div class="modal-bg" id="modal-delete">
    <div class="modal" style="max-width:400px">
        <button class="modal-close" onclick="closeModal('modal-delete')"><i class="ti ti-x"></i></button>
        <div class="modal-title"><i class="ti ti-trash"></i> 🦅 حذف کانفیگ</div>
        <input type="hidden" id="delete-uuid">
        <p style="font-size:12.5px;color:var(--text-dim);margin-bottom:14px">برای حذف این کانفیگ، رمز آن را وارد کنید.</p>
        <div class="fg"><label><i class="ti ti-lock"></i> رمز کانفیگ</label><input class="fi" id="delete-password" type="password" placeholder="رمز کانفیگ را وارد کنید" dir="ltr"></div>
        <div style="display:flex;gap:8px;margin-top:14px">
            <button class="btn btn-d" onclick="confirmDelete()" style="flex:2"><i class="ti ti-trash"></i> حذف</button>
            <button class="btn btn-o" onclick="closeModal('modal-delete')" style="flex:1">انصراف</button>
        </div>
    </div>
</div>

<!-- Mobile Header -->
<div class="mob-top">
    <div class="ml"><div class="mob-logo">🦅</div><span class="mob-title">پنل عقاب</span></div>
    <div class="mob-right"><button class="theme-mob" id="theme-mob-btn" onclick="toggleTheme()"><i class="ti ti-palette" id="theme-mob-icon"></i></button><button class="menu-btn" id="open-sb"><i class="ti ti-menu-2"></i></button></div>
</div>
<div class="overlay" id="overlay"></div>

<!-- Sidebar -->
<aside class="sidebar" id="sb">
    <div class="logo"><div class="logo-icon">🦅</div><div><div class="logo-name">پنل عقاب</div><div class="logo-sub">مدیریت کاربران</div></div></div>
    <div class="nav-wrap">
        <div class="nav-it on" data-pg="users"><i class="ti ti-layout-dashboard"></i> داشبورد</div>
        <div class="nav-it" data-pg="connections"><i class="ti ti-plug-connected"></i> اتصالات زنده</div>
        <div class="nav-it" data-pg="support"><i class="ti ti-headset"></i> پشتیبانی</div>
        <div class="nav-it" data-pg="settings"><i class="ti ti-settings"></i> تنظیمات</div>
        <div class="nav-it" data-pg="backup"><i class="ti ti-database"></i> بکاپ</div>
    </div>
    <div class="sb-foot">
        <button class="theme-btn" onclick="toggleTheme()"><i class="ti ti-palette" id="theme-icon"></i> <span id="theme-label">تغییر تم</span></button>
        <button class="logout-btn" onclick="logout()"><i class="ti ti-logout"></i> خروج</button>
    </div>
</aside>

<!-- Main -->
<main class="main">
<section class="pg on" id="pg-users">
    <div class="topbar">
        <div>
            <div class="tb-title"><i class="ti ti-layout-dashboard"></i> داشبورد عقاب</div>
            <div class="tb-sub" id="last-update">آخرین بروزرسانی: لحظه‌ای</div>
        </div>
        <div class="tb-right">
            <span class="badge bg-fire" id="online-badge"><span class="dot dg"></span> ۰ آنلاین</span>
            <button class="btn btn-p" onclick="openModal('modal-user')"><i class="ti ti-plus"></i> کانفیگ جدید</button>
        </div>
    </div>

    <div class="stats-grid">
        <div class="stat-card"><span class="icon">🔥</span><div class="number" id="online-count">۰</div><div class="label">آنلاین</div><div class="bar"></div></div>
        <div class="stat-card"><span class="icon">👥</span><div class="number" id="total-users">۰</div><div class="label">کل کاربران</div><div class="bar"></div></div>
        <div class="stat-card"><span class="icon">📊</span><div class="number" id="total-usage">۰</div><div class="label">مصرف کل (MB)</div><div class="bar"></div></div>
        <div class="stat-card"><span class="icon">📱</span><div class="number" id="active-devices">۰</div><div class="label">دستگاه‌های فعال</div><div class="bar"></div></div>
        <div class="stat-card"><span class="icon">⛔</span><div class="number" id="inactive-count">۰</div><div class="label">غیرفعال</div><div class="bar"></div></div>
        <div class="stat-card"><span class="icon">🏆</span><div class="number" id="top-user-label" style="font-size:14px">-</div><div class="label">پر مصرف‌ترین</div><div class="bar"></div></div>
    </div>

    <div id="users-grid" class="user-grid"><div class="empty"><i class="ti ti-users"></i><p>هیچ کاربری ساخته نشده</p></div></div>
</section>

<section class="pg" id="pg-connections">
    <div class="topbar"><div><div class="tb-title">🔌 اتصالات زنده</div><div class="tb-sub" id="conn-count">۰ اتصال</div></div><div class="tb-right"><span class="badge bg-green" id="conn-live-badge"><span class="dot dg pulse"></span> فعال</span><button class="btn btn-sm btn-o" onclick="loadConnections()"><i class="ti ti-refresh"></i> بروزرسانی</button></div></div>
    <div id="conns-grid" class="conn-grid"><div class="empty"><i class="ti ti-plug-off"></i><p>هیچ اتصال فعالی وجود ندارد</p></div></div>
</section>

<section class="pg" id="pg-support">
    <div class="topbar"><div><div class="tb-title"><i class="ti ti-headset"></i> پشتیبانی</div><div class="tb-sub">راهنمایی و پشتیبانی سریع</div></div></div>
    <div style="background:var(--card);border:1px solid var(--card-border);border-radius:var(--radius);padding:22px;max-width:600px">
        <div style="font-size:15px;font-weight:700;color:var(--text);margin-bottom:14px;display:flex;align-items:center;gap:8px"><i class="ti ti-messages" style="color:var(--primary)"></i> ارتباط با پشتیبانی</div>
        <p style="font-size:12.5px;color:var(--text-dim);line-height:1.8;margin-bottom:14px">برای دریافت راهنمایی، پشتیبانی و پاسخ به سوالات خود، به گروه تلگرامی ما بپیوندید.</p>
        <div style="display:flex;gap:8px;flex-wrap:wrap">
            <button class="btn btn-p" onclick="window.open('https://t.me/+QyEVU0FquFczYjQ0','_blank')" style="flex:2"><i class="ti ti-brand-telegram"></i> عضویت در گروه</button>
            <button class="btn btn-o" onclick="navigator.clipboard.writeText('https://t.me/+QyEVU0FquFczYjQ0').then(()=>toast('لینک گروه کپی شد ✓','ok'))"><i class="ti ti-copy"></i> کپی</button>
        </div>
        <div style="margin-top:14px;padding-top:14px;border-top:1px solid var(--card-border);display:flex;align-items:center;gap:10px;flex-wrap:wrap">
            <span class="badge bg-green"><span class="dot dg"></span> آنلاین</span>
            <span style="font-size:10.5px;color:var(--text-dim)">گروه پشتیبانی عقاب</span>
        </div>
    </div>
</section>

<section class="pg" id="pg-settings">
    <div class="topbar">
        <div>
            <div class="tb-title"><i class="ti ti-settings"></i> تنظیمات پنل</div>
            <div class="tb-sub">تنظیمات ظاهری، امنیتی و ربات تلگرام</div>
        </div>
    </div>
    
    <!-- تنظیمات ظاهری -->
    <div class="settings-card" style="margin-bottom:16px">
        <div class="title"><i class="ti ti-color-swatch"></i> تنظیمات ظاهری</div>
        <div class="toggle-row">
            <div class="toggle-label"><i class="ti ti-palette" style="color:var(--primary)"></i> تم آتشین (دارک/لایت)</div>
            <div class="switch" id="theme-switch" onclick="toggleTheme()"><div class="slider"></div></div>
        </div>
        <div style="margin-top:10px;font-size:9.5px;color:var(--text-muted)">💡 تغییر بین تم تیره و روشن</div>
    </div>

    <!-- تغییر رمز عبور -->
    <div class="settings-card" style="margin-bottom:16px">
        <div class="title"><i class="ti ti-lock"></i> تغییر رمز عبور پنل</div>
        <p style="font-size:11.5px;color:var(--text-dim);margin-bottom:14px;line-height:1.6">رمز عبور ورود به پنل مدیریت را تغییر دهید.</p>
        
        <div class="field">
            <label>رمز فعلی</label>
            <input id="current-password" type="password" placeholder="رمز فعلی را وارد کنید" dir="ltr">
        </div>
        <div class="field">
            <label>رمز جدید</label>
            <input id="new-password" type="password" placeholder="رمز جدید (حداقل ۴ کاراکتر)" dir="ltr">
        </div>
        <div class="field">
            <label>تکرار رمز جدید</label>
            <input id="confirm-password" type="password" placeholder="رمز جدید را دوباره وارد کنید" dir="ltr">
        </div>
        <button class="btn btn-p" onclick="changePassword()" style="margin-top:6px">
            <i class="ti ti-key"></i> تغییر رمز عبور
        </button>
        <div id="password-result" style="margin-top:10px;font-size:11px;display:none"></div>
    </div>

    <!-- تنظیمات ربات تلگرام -->
    <div class="settings-card">
        <div class="title"><i class="ti ti-brand-telegram"></i> تنظیمات ربات تلگرام</div>
        <p style="font-size:11.5px;color:var(--text-dim);margin-bottom:14px;line-height:1.6">
            با تنظیم ربات تلگرام، می‌تونید پنل رو از طریق تلگرام مدیریت کنید.
            <br>📌 <b>نحوه تنظیم:</b>
            <br>۱. یک ربات با @BotFather بسازید و توکن بگیرید
            <br>۲. به ربات پیام /start بدید تا Chat ID رو بگیرید
            <br>۳. اطلاعات زیر رو وارد کنید و "ذخیره و فعال‌سازی" رو بزنید
        </p>
        
        <div class="field">
            <label><i class="ti ti-key"></i> توکن ربات (Bot Token)</label>
            <input id="bot-token" type="text" placeholder="مثلاً: 123456:ABC-DEF..." dir="ltr">
        </div>
        <div class="field">
            <label><i class="ti ti-id"></i> Chat ID</label>
            <input id="chat-id" type="text" placeholder="مثلاً: 123456789" dir="ltr">
        </div>
        
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px">
            <button class="btn btn-p" onclick="saveTelegramSettings()" style="flex:2">
                <i class="ti ti-save"></i> ذخیره و فعال‌سازی
            </button>
            <button class="btn btn-o" onclick="testTelegram()" style="flex:1">
                <i class="ti ti-send"></i> تست
            </button>
            <button class="btn btn-o" onclick="setWebhook()" style="flex:1">
                <i class="ti ti-link"></i> تنظیم Webhook
            </button>
        </div>
        
        <div id="telegram-status" class="telegram-status"></div>
    </div>
</section>

<section class="pg" id="pg-backup">
    <div class="topbar"><div><div class="tb-title"><i class="ti ti-database"></i> مدیریت بکاپ</div><div class="tb-sub">ذخیره و بازیابی اطلاعات</div></div></div>
    <div class="settings-card">
        <div class="title"><i class="ti ti-download"></i> بکاپ‌گیری</div>
        <p style="font-size:12px;color:var(--text-dim);margin-bottom:14px;line-height:1.8">از اطلاعات کاربران، کانفیگ‌ها و تنظیمات بکاپ بگیرید.</p>
        <div style="display:flex;gap:8px;flex-wrap:wrap">
            <button class="btn btn-p" onclick="createBackup()" style="flex:2"><i class="ti ti-download"></i> دانلود بکاپ</button>
            <button class="btn btn-o" onclick="document.getElementById('restore-input').click()" style="flex:1"><i class="ti ti-upload"></i> بازیابی</button>
            <input type="file" id="restore-input" accept=".json" style="display:none" onchange="restoreBackup(event)">
        </div>
        <div style="margin-top:10px;font-size:9.5px;color:var(--text-muted)">📁 فایل بکاپ با فرمت JSON</div>
    </div>
</section>
</main>

<script>
// Theme
let currentTheme = localStorage.getItem('eagle-theme') || 'dark';
function applyTheme(theme){
    currentTheme = theme;
    localStorage.setItem('eagle-theme', theme);
    document.documentElement.setAttribute('data-theme', theme);
    const icon = document.getElementById('theme-icon');
    const mobIcon = document.getElementById('theme-mob-icon');
    const label = document.getElementById('theme-label');
    const sw = document.getElementById('theme-switch');
    if(icon){icon.className = 'ti ' + (theme === 'dark' ? 'ti-moon' : 'ti-sun');}
    if(mobIcon){mobIcon.className = 'ti ' + (theme === 'dark' ? 'ti-moon' : 'ti-sun');}
    if(label){label.textContent = theme === 'dark' ? 'تم تیره' : 'تم روشن';}
    if(sw){sw.classList.toggle('on', theme === 'light');}
}
function toggleTheme(){
    const next = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(next);
}
applyTheme(currentTheme);

// Toast
function toast(msg, type=''){
    const t=document.getElementById('toast');
    t.textContent=msg;
    t.className='toast show' + (type ? ' ' + type : '');
    setTimeout(()=>t.classList.remove('show'), 2500);
}
function fmtB(b){
    if(!b || b===0) return '0 B';
    if(b<1024) return b + ' B';
    if(b<1024**2) return (b/1024).toFixed(1) + ' KB';
    if(b<1024**3) return (b/1024**2).toFixed(2) + ' MB';
    return (b/1024**3).toFixed(2) + ' GB';
}
function esc(s){return String(s||'').replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function openModal(id){document.getElementById(id).classList.add('open');}
function closeModal(id){document.getElementById(id).classList.remove('open');}

// Auth
async function authF(url, opts={}){
    const r=await fetch(url, opts);
    if(r.status===401){location.href='/login';throw new Error('unauthorized');}
    return r;
}
async function logout(){
    try{await fetch('/api/logout',{method:'POST'});}catch(e){}
    location.href='/login';
}

// Navigation
function navTo(name){
    document.querySelectorAll('.nav-it').forEach(n=>n.classList.toggle('on', n.dataset.pg===name));
    document.querySelectorAll('.pg').forEach(p=>p.classList.toggle('on', p.id==='pg-'+name));
    closeSb();
    if(name==='users') loadUsers();
    if(name==='connections') loadConnections();
}
document.querySelectorAll('.nav-it').forEach(el=>{
    el.addEventListener('click', ()=>navTo(el.dataset.pg));
});

const sb=document.getElementById('sb'), overlay=document.getElementById('overlay');
function openSb(){sb.classList.add('open'); overlay.classList.add('show');}
function closeSb(){sb.classList.remove('open'); overlay.classList.remove('show');}
document.getElementById('open-sb').addEventListener('click', openSb);
overlay.addEventListener('click', closeSb);

// ===== توابع آیپی تمیز =====
async function addCleanIP(uuid){
    const input = document.getElementById('cip-input-' + uuid);
    const ip = input.value.trim();
    if(!ip){
        toast('لطفاً یک آیپی وارد کنید', 'err');
        return;
    }
    try{
        const r = await authF('/api/links/' + uuid + '/clean-ips', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({ips: [ip]})
        });
        const data = await r.json();
        if(r.ok){
            toast('✅ آیپی تمیز اضافه شد', 'ok');
            input.value = '';
            loadUsers();
        } else {
            toast('خطا: ' + (data.detail || 'نامشخص'), 'err');
        }
    } catch(e){
        toast('خطا در ارتباط با سرور', 'err');
    }
}

async function removeCleanIP(uuid, ip, port){
    try{
        const r = await authF('/api/links/' + uuid + '/clean-ips', {
            method: 'DELETE',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({ip: ip, port: port})
        });
        if(r.ok){
            toast('✅ آیپی تمیز حذف شد', 'ok');
            loadUsers();
        }
    } catch(e){
        toast('خطا', 'err');
    }
}

// ===== تغییر رمز عبور =====
async function changePassword(){
    const current = document.getElementById('current-password').value.trim();
    const newPass = document.getElementById('new-password').value.trim();
    const confirm = document.getElementById('confirm-password').value.trim();
    const result = document.getElementById('password-result');
    
    if(!current){
        result.style.display='block';
        result.style.color='#f87171';
        result.textContent='❌ لطفاً رمز فعلی را وارد کنید';
        return;
    }
    if(newPass.length < 4){
        result.style.display='block';
        result.style.color='#f87171';
        result.textContent='❌ رمز جدید باید حداقل ۴ کاراکتر باشد';
        return;
    }
    if(newPass !== confirm){
        result.style.display='block';
        result.style.color='#f87171';
        result.textContent='❌ رمز جدید و تکرار آن مطابقت ندارند';
        return;
    }
    
    try{
        const r = await authF('/api/change-password', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({current_password: current, new_password: newPass, confirm_password: confirm})
        });
        const data = await r.json();
        if(r.ok){
            result.style.display='block';
            result.style.color='#10b981';
            result.textContent='✅ ' + data.message;
            document.getElementById('current-password').value = '';
            document.getElementById('new-password').value = '';
            document.getElementById('confirm-password').value = '';
            toast('🔑 رمز عبور با موفقیت تغییر کرد', 'ok');
            setTimeout(() => {
                toast('⚠️ برای امنیت، به صفحه ورود هدایت میشوید', '');
                setTimeout(() => logout(), 2000);
            }, 3000);
        } else {
            result.style.display='block';
            result.style.color='#f87171';
            result.textContent='❌ ' + (data.detail || 'خطا');
        }
    } catch(e){
        result.style.display='block';
        result.style.color='#f87171';
        result.textContent='❌ خطا در ارتباط با سرور';
    }
}

// ===== تنظیمات ربات تلگرام =====
async function loadTelegramSettings() {
    try {
        const r = await authF('/api/telegram/settings');
        const data = await r.json();
        document.getElementById('bot-token').value = data.bot_token || '';
        document.getElementById('chat-id').value = data.chat_id || '';
        
        const statusDiv = document.getElementById('telegram-status');
        if (data.enabled) {
            statusDiv.innerHTML = `✅ <b>ربات فعال است</b><br>📎 Webhook: <code style="font-size:9px">${data.webhook_url || 'تنظیم نشده'}</code>`;
            statusDiv.style.borderColor = 'rgba(16,185,129,0.2)';
        } else {
            statusDiv.innerHTML = `⛔ <b>ربات غیرفعال است</b><br>برای فعال‌سازی، اطلاعات را وارد کنید.`;
            statusDiv.style.borderColor = 'var(--card-border)';
        }
    } catch(e) {
        console.error(e);
    }
}

async function saveTelegramSettings() {
    const bot_token = document.getElementById('bot-token').value.trim();
    const chat_id = document.getElementById('chat-id').value.trim();
    
    if (!bot_token || !chat_id) {
        toast('لطفاً توکن و Chat ID را وارد کنید', 'err');
        return;
    }
    
    try {
        const r = await authF('/api/telegram/settings', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({
                bot_token: bot_token,
                chat_id: chat_id,
                enabled: true
            })
        });
        
        if (r.ok) {
            toast('✅ تنظیمات ربات ذخیره شد', 'ok');
            loadTelegramSettings();
            setTimeout(() => setWebhook(), 1000);
        }
    } catch(e) {
        toast('❌ خطا: ' + e.message, 'err');
    }
}

async function testTelegram() {
    try {
        const r = await authF('/api/telegram/settings');
        const data = await r.json();
        
        if (!data.enabled || !data.bot_token || !data.chat_id) {
            toast('❌ ابتدا ربات را فعال کنید', 'err');
            return;
        }
        
        const token = data.bot_token;
        const chat_id = data.chat_id;
        const url = `https://api.telegram.org/bot${token}/sendMessage`;
        
        const resp = await fetch(url, {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({
                chat_id: chat_id,
                text: '🦅 پیام تست از پنل عقاب!\n✅ اتصال برقرار است.'
            })
        });
        
        if (resp.ok) {
            toast('✅ پیام تست ارسال شد!', 'ok');
        } else {
            const data = await resp.json();
            toast('❌ خطا: ' + (data.description || 'نامشخص'), 'err');
        }
    } catch(e) {
        toast('❌ خطا: ' + e.message, 'err');
    }
}

async function setWebhook() {
    try {
        const r = await authF('/api/telegram/set-webhook', {
            method: 'POST'
        });
        const data = await r.json();
        if (r.ok) {
            toast('✅ Webhook تنظیم شد: ' + data.webhook_url, 'ok');
            loadTelegramSettings();
        } else {
            toast('❌ خطا: ' + data.detail, 'err');
        }
    } catch(e) {
        toast('❌ خطا: ' + e.message, 'err');
    }
}

// ===== Load Users =====
async function loadUsers(){
    try{
        const r=await authF('/api/links');
        const {links=[]}=await r.json();
        const grid=document.getElementById('users-grid');
        const total=links.length;
        const online=links.filter(l=>l.active && !l.expired).length;
        const inactive=links.filter(l=>!l.active || l.expired).length;
        const totalBytes=links.reduce((sum,l)=>sum+(l.used_bytes||0),0);
        const devices=links.reduce((sum,l)=>sum+(l.max_devices||0),0);
        document.getElementById('total-users').textContent=total;
        document.getElementById('online-count').textContent=online;
        document.getElementById('inactive-count').textContent=inactive;
        document.getElementById('total-usage').textContent=(totalBytes/(1024*1024)).toFixed(1);
        document.getElementById('active-devices').textContent=devices;
        document.getElementById('last-update').textContent='آخرین بروزرسانی: ' + new Date().toLocaleTimeString('fa-IR');
        document.getElementById('online-badge').innerHTML='<span class="dot dg"></span> '+online+' آنلاین';
        try{
            const sr=await authF('/stats');
            const statsData=await sr.json();
            if(statsData.top_user){
                document.getElementById('top-user-label').textContent='🦅 ' + statsData.top_user.label;
            }else{
                document.getElementById('top-user-label').textContent='—';
            }
        }catch(e){}
        if(!links.length){
            grid.innerHTML='<div class="empty"><i class="ti ti-users"></i><p>هیچ کاربری ساخته نشده</p></div>';
            return;
        }
        const host=window.location.host;
        grid.innerHTML=links.map(l=>{
            const pct=l.limit_bytes===0?0:Math.min(100,(l.used_bytes/l.limit_bytes)*100);
            const bc=pct>90?'#ef4444':pct>70?'#f59e0b':'#4f8cff';
            const active=l.active && !l.expired;
            const subLink='https://'+host+'/sub/'+l.uuid;
            const todayBytes=l.today_bytes||0;
            const todayFmt=fmtB(todayBytes);
            const lastSeen=l.last_connected_at?new Date(l.last_connected_at).toLocaleString('fa-IR'):'—';
            const statusText=active?'🟢 آنلاین':'🔴 آفلاین';
            const statusClass=active?'on':'off';
            
            const cleanIps = l.clean_ips || [];
            const cleanIpsHtml = cleanIps.length > 0 ? 
                cleanIps.map(ci => `<span class="cip-item">📍 ${ci.ip}:${ci.port} <span class="del-cip" onclick="removeCleanIP('${l.uuid}','${ci.ip}',${ci.port})">✕</span></span>`).join('') :
                `<span class="cip-empty">هیچ آیپی تمیزی ثبت نشده</span>`;
            
            return `<div class="user-card">
                <div class="head">
                    <div class="name">🦅 ${esc(l.label)} ${l.has_password?'<span class="lock-badge"><i class="ti ti-lock"></i> رمزدار</span>':''}</div>
                    <span class="status ${statusClass}">${statusText}</span>
                </div>
                <div class="uuid">🔑 ${esc(l.uuid)}</div>
                <div class="info">
                    <span>📊 امروز: ${todayFmt}</span>
                    <span>📅 آخرین: ${lastSeen}</span>
                    <span>📱 ${l.max_devices===0?'∞':l.max_devices+' دستگاه'}</span>
                </div>
                <div class="quota-info">
                    <span>📊 مصرف: ${fmtB(l.used_bytes)}</span>
                    <span>📦 کل: ${l.limit_bytes===0?'∞':fmtB(l.limit_bytes)}</span>
                </div>
                <div class="quota-bar">
                    <div class="quota-fill" style="width:${pct}%; background:${bc}"></div>
                </div>
                
                <div class="clean-ips-box">
                    <div class="cip-title"><i class="ti ti-cloud"></i> آیپی‌های تمیز (${cleanIps.length})</div>
                    <div class="cip-list">${cleanIpsHtml}</div>
                    <div class="cip-input-group">
                        <input id="cip-input-${l.uuid}" placeholder="مثلاً 1.2.3.4 یا 1.2.3.4:443" dir="ltr">
                        <button class="btn btn-sm btn-pur" onclick="addCleanIP('${l.uuid}')"><i class="ti ti-plus"></i> افزودن</button>
                    </div>
                </div>
                
                <div class="actions">
                    <button class="btn btn-sm btn-o" onclick="navigator.clipboard.writeText('${esc(l.vless_link)}').then(()=>toast('لینک کپی شد','ok'))"><i class="ti ti-copy"></i> لینک</button>
                    <button class="btn btn-sm btn-pur" onclick="navigator.clipboard.writeText('${esc(subLink)}').then(()=>toast('ساب‌لینک کپی شد','ok'))"><i class="ti ti-link"></i> ساب</button>
                    <button class="btn btn-sm btn-amber" onclick="resetUsage('${l.uuid}')"><i class="ti ti-rotate"></i> ریست</button>
                    <button class="btn btn-sm btn-pur btn-icon" onclick="openEditModal('${l.uuid}')" title="ویرایش"><i class="ti ti-edit"></i></button>
                    <button class="btn btn-sm btn-d" onclick="openDeleteModal('${l.uuid}')"><i class="ti ti-trash"></i></button>
                </div>
            </div>`;
        }).join('');
    }catch(e){console.error(e);}
}

// Edit/Delete/Reset functions
async function openEditModal(uuid){
    try{
        const r=await authF('/api/links');
        const {links=[]}=await r.json();
        const link=links.find(l=>l.uuid===uuid);
        if(!link){toast('کاربر یافت نشد','err');return;}
        document.getElementById('edit-uuid').value=uuid;
        document.getElementById('edit-label').value=link.label||'';
        document.getElementById('edit-password').value='';
        if(link.limit_bytes===0){
            document.getElementById('edit-quota').value='';
        }else{
            document.getElementById('edit-quota').value=(link.limit_bytes/(1024**3)).toFixed(1);
        }
        document.getElementById('edit-unit').value='GB';
        if(link.expires_at){
            const days=Math.ceil((new Date(link.expires_at)-new Date())/(1000*60*60*24));
            document.getElementById('edit-exp').value=days>0?days:0;
        }else{
            document.getElementById('edit-exp').value='';
        }
        document.getElementById('edit-fingerprint').value=link.fingerprint||'chrome';
        document.getElementById('edit-devices').value=link.max_devices||0;
        document.getElementById('edit-protocol').value=link.protocol||'vless-ws';
        document.getElementById('edit-status').value=link.active?'true':'false';
        document.getElementById('edit-port').value=link.port||443;
        document.getElementById('edit-password-section').style.display=link.has_password?'block':'none';
        openModal('modal-edit');
    }catch(e){toast('خطا در بارگذاری','err');}
}
async function saveEdit(){
    const uuid=document.getElementById('edit-uuid').value;
    const password=document.getElementById('edit-password').value.trim();
    const label=document.getElementById('edit-label').value.trim()||'کاربر';
    const quota=parseFloat(document.getElementById('edit-quota').value)||0;
    const unit=document.getElementById('edit-unit').value||'GB';
    const exp=parseInt(document.getElementById('edit-exp').value)||0;
    const fingerprint=document.getElementById('edit-fingerprint').value||'chrome';
    const devices=parseInt(document.getElementById('edit-devices').value)||0;
    const protocol=document.getElementById('edit-protocol').value||'vless-ws';
    const active=document.getElementById('edit-status').value==='true';
    const port=parseInt(document.getElementById('edit-port').value)||443;
    try{
        const r=await authF('/api/links/'+uuid,{
            method:'PATCH',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({label,limit_value:quota,limit_unit:unit,expires_days:exp,fingerprint,max_devices:devices,protocol,active,password,port})
        });
        if(!r.ok){
            const err=await r.json().catch(()=>({}));
            if(r.status===403){toast('❌ رمز کانفیگ اشتباه است!','err');return;}
            throw new Error(err.detail||'خطا');
        }
        closeModal('modal-edit');
        toast('🦅 کانفیگ ویرایش شد ✓','ok');
        loadUsers();
    }catch(e){toast('خطا در ویرایش: '+e.message,'err');}
}
function openDeleteModal(uuid){document.getElementById('delete-uuid').value=uuid;document.getElementById('delete-password').value='';openModal('modal-delete');}
async function confirmDelete(){
    const uuid=document.getElementById('delete-uuid').value;
    const password=document.getElementById('delete-password').value.trim();
    try{
        const r=await authF('/api/links/'+uuid,{
            method:'DELETE',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({password})
        });
        if(!r.ok){
            const err=await r.json().catch(()=>({}));
            if(r.status===403){toast('❌ رمز کانفیگ اشتباه است!','err');return;}
            throw new Error(err.detail||'خطا');
        }
        closeModal('modal-delete');
        toast('🦅 کاربر حذف شد','ok');
        loadUsers();
    }catch(e){toast('خطا در حذف: '+e.message,'err');}
}
async function saveUser(){
    const label=document.getElementById('user-label').value.trim()||'کاربر';
    const quota=parseFloat(document.getElementById('user-quota').value)||2;
    const unit=document.getElementById('user-unit').value||'GB';
    const exp=parseInt(document.getElementById('user-exp').value)||0;
    const fingerprint=document.getElementById('user-fingerprint').value||'chrome';
    const devices=parseInt(document.getElementById('user-devices').value)||0;
    const protocol=document.getElementById('user-protocol').value||'vless-ws';
    const password=document.getElementById('user-password').value.trim();
    const port=parseInt(document.getElementById('user-port').value)||443;
    try{
        const r=await authF('/api/links',{
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({label,limit_value:quota,limit_unit:unit,expires_days:exp,fingerprint,max_devices:devices,protocol,password,port})
        });
        if(!r.ok)throw new Error();
        document.getElementById('user-label').value='';
        document.getElementById('user-quota').value='2';
        document.getElementById('user-unit').value='GB';
        document.getElementById('user-exp').value='30';
        document.getElementById('user-fingerprint').value='chrome';
        document.getElementById('user-devices').value='1';
        document.getElementById('user-protocol').value='vless-ws';
        document.getElementById('user-password').value='';
        document.getElementById('user-port').value='443';
        closeModal('modal-user');
        toast('🦅 کانفیگ ساخته شد ✓','ok');
        loadUsers();
    }catch(e){toast('خطا در ساخت','err');}
}
async function resetUsage(uuid){
    if(!confirm('مصرف این کاربر ریست شود؟'))return;
    try{
        const r=await authF('/api/links/'+uuid,{
            method:'PATCH',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({reset_usage:true})
        });
        if(!r.ok)throw new Error();
        toast('مصرف ریست شد ✓','ok');
        loadUsers();
    }catch(e){toast('خطا','err');}
}
async function loadConnections(){
    try{
        const r=await authF('/api/connections');
        const d=await r.json();
        const grid=document.getElementById('conns-grid');
        const count=d.count||0;
        document.getElementById('conn-count').textContent=count+' اتصال';
        if(!count){
            grid.innerHTML='<div class="empty"><i class="ti ti-plug-off"></i><p>هیچ اتصال فعالی وجود ندارد</p></div>';
            return;
        }
        grid.innerHTML=d.connections.map(c=>{
            const secs=c.connected_at?Math.max(0,Math.floor((Date.now()-new Date(c.connected_at).getTime())/1000)):0;
            const dur=secs<60?secs+' ث':secs<3600?Math.floor(secs/60)+' د':Math.floor(secs/3600)+' س';
            return `<div class="conn-card">
                <div class="ip"><span class="conn-status-dot"></span> ${esc(c.ip)}</div>
                <div class="label">${esc(c.label||'نامشخص')}</div>
                <div class="conn-info"><span>📥 ${esc(c.bytes_fmt||'0 B')}</span><span>⏱ ${dur}</span></div>
            </div>`;
        }).join('');
    }catch(e){console.error(e);}
}
async function createBackup(){
    try{
        const r=await authF('/api/backup');
        const data=await r.json();
        const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
        const url=URL.createObjectURL(blob);
        const a=document.createElement('a');
        a.href=url;
        a.download='eagle_backup_'+new Date().toISOString().slice(0,10)+'.json';
        a.click();
        URL.revokeObjectURL(url);
        toast('✅ بکاپ دانلود شد','ok');
    }catch(e){toast('خطا در بکاپ‌گیری','err');}
}
async function restoreBackup(event){
    const file=event.target.files[0];
    if(!file)return;
    try{
        const text=await file.text();
        const data=JSON.parse(text);
        const r=await authF('/api/backup/restore',{
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify(data)
        });
        if(!r.ok){const err=await r.json().catch(()=>({}));toast(err.detail||'خطا در بازیابی','err');return;}
        toast('✅ بکاپ بازیابی شد','ok');
        setTimeout(()=>location.reload(),1500);
    }catch(e){toast('خطا: '+e.message,'err');}
    event.target.value='';
}

// Init
document.addEventListener('DOMContentLoaded', async ()=>{
    try{
        const r=await fetch('/api/me');
        const d=await r.json();
        if(!d.authenticated)location.href='/login';
    }catch(e){location.href='/login';}
    loadTelegramSettings();
    loadUsers();
    loadConnections();
    setInterval(()=>{
        if(document.getElementById('pg-users').classList.contains('on'))loadUsers();
        if(document.getElementById('pg-connections').classList.contains('on'))loadConnections();
    },5000);
});
</script>
</body></html>"""


# ===== صفحه ساب‌لینک (با آیپی تمیز) =====
def get_sub_page_html(uuid: str, link: dict) -> str:
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
    clean_ips = link.get('clean_ips', [])

    percent = 0
    if limit > 0:
        percent = min(100, (used / limit) * 100)

    expires_at = link.get('expires_at')
    if expires_at:
        try:
            from datetime import datetime
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
        if not b or b == 0: return '0 B'
        if b < 1024: return f'{b} B'
        if b < 1024**2: return f'{b/1024:.1f} KB'
        if b < 1024**3: return f'{b/1024**2:.2f} MB'
        return f'{b/1024**3:.2f} GB'

    used_fmt = fmt_bytes(used)
    limit_fmt = 'نامحدود' if limit == 0 else fmt_bytes(limit)

    conns_html = ""
    if active_connections > 0:
        conns_html = f"""
        <div style="background:rgba(79,140,255,0.04);border:1px solid rgba(79,140,255,0.06);border-radius:12px;padding:10px 14px;margin:12px 0">
            <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;font-size:10.5px;color:var(--text-dim)">
                <span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:#10b981;animation:pulse 1.5s infinite"></span>
                <span style="font-weight:700;color:#10b981">{active_connections} دستگاه متصل</span>
            </div>
            <div style="display:flex;flex-wrap:wrap;gap:4px">
        """
        for conn in active_connections_list[:10]:
            ip = conn.get('ip', 'نامشخص')
            conns_html += f"""
                <span style="font-family:monospace;font-size:9px;background:rgba(79,140,255,0.04);border:1px solid rgba(79,140,255,0.04);padding:2px 8px;border-radius:6px;color:var(--text-dim)">🔵 {ip}</span>
            """
        if len(active_connections_list) > 10:
            conns_html += f"""
                <span style="font-family:monospace;font-size:9px;background:rgba(79,140,255,0.02);padding:2px 8px;border-radius:6px;color:var(--text-muted)">+{len(active_connections_list)-10} بیشتر</span>
            """
        conns_html += """
            </div>
        </div>
        """
    else:
        conns_html = f"""
        <div style="background:rgba(79,140,255,0.02);border:1px solid rgba(79,140,255,0.04);border-radius:12px;padding:8px 14px;margin:12px 0;text-align:center">
            <span style="font-size:10.5px;color:var(--text-dim)">🔴 بدون اتصال فعال</span>
        </div>
        """

    clean_ips_html = ""
    if clean_ips:
        clean_ips_html = f"""
        <div style="background:rgba(79,140,255,0.03);border:1px solid rgba(79,140,255,0.06);border-radius:10px;padding:10px 14px;margin:12px 0">
            <div style="font-size:9.5px;color:var(--text-dim);display:flex;align-items:center;gap:4px;margin-bottom:4px;font-weight:600">
                <i class="ti ti-cloud" style="color:var(--primary)"></i> آیپی‌های تمیز ({len(clean_ips)})
            </div>
            <div style="display:flex;flex-wrap:wrap;gap:4px">
        """
        for ci in clean_ips:
            clean_ips_html += f"""
                <span style="font-family:monospace;font-size:9px;background:rgba(79,140,255,0.06);border:1px solid rgba(79,140,255,0.06);padding:2px 8px;border-radius:6px;color:var(--text-dim)">📍 {ci['ip']}:{ci.get('port', 443)}</span>
            """
        clean_ips_html += """
            </div>
        </div>
        """

    from main import get_host, generate_vless_link
    host = get_host()
    remark = f"عقاب-{label}"
    
    main_vless_link = generate_vless_link(uuid, host, remark=remark, protocol=protocol, fingerprint=fingerprint, port=port)
    
    clean_vless_links = []
    for ci in clean_ips:
        if ci.get('active', True):
            clean_vless_links.append(generate_vless_link(uuid, host, remark=remark + "-clean", protocol=protocol, fingerprint=fingerprint, port=ci.get('port', port), clean_ip=ci['ip']))

    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🦅 {label} · پنل عقاب</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{
    --bg:#0b0d1a;
    --card:#141632;
    --card-border:#2a2d5a;
    --primary:#4f8cff;
    --secondary:#b388ff;
    --text:#f0f0ff;
    --text-dim:#7a7aaa;
    --text-muted:#4a4a7a;
}}
body{{
    font-family:'Vazirmatn',sans-serif;
    min-height:100vh;
    display:flex;
    align-items:center;
    justify-content:center;
    padding:20px;
    background:radial-gradient(ellipse at 20% 50%, #141632 0%, #0b0d1a 100%);
    color:var(--text);
}}
.card{{
    background:var(--card);
    border:1px solid var(--card-border);
    border-radius:24px;
    padding:36px 34px 30px;
    max-width:520px;
    width:100%;
    box-shadow:0 25px 60px rgba(0,0,0,0.6);
}}
.brand{{
    display:flex;align-items:center;gap:14px;
    margin-bottom:24px;
    padding-bottom:16px;
    border-bottom:1px solid var(--card-border);
}}
.brand-icon{{
    width:48px;height:48px;
    border-radius:14px;
    background:linear-gradient(135deg,var(--primary),var(--secondary));
    display:flex;align-items:center;justify-content:center;
    font-size:24px;
    flex-shrink:0;
    box-shadow:0 4px 20px rgba(79,140,255,0.2);
}}
.brand-text .name{{
    font-size:17px;font-weight:800;
    background:linear-gradient(135deg,var(--primary),var(--secondary));
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}}
.brand-text .sub{{font-size:10px;color:var(--text-dim);margin-top:1px}}
.user-header{{
    display:flex;align-items:center;justify-content:space-between;margin-bottom:4px;
}}
.user-name{{
    font-size:22px;font-weight:800;color:var(--text);
    display:flex;align-items:center;gap:8px;
}}
.status{{
    display:inline-flex;align-items:center;gap:5px;
    padding:4px 12px;border-radius:16px;
    font-size:11px;font-weight:700;
}}
.status.active{{
    background:rgba(79,140,255,0.12);color:var(--primary);
    border:1px solid rgba(79,140,255,0.1);
}}
.status.inactive{{
    background:rgba(239,68,68,0.1);color:#f87171;
    border:1px solid rgba(239,68,68,0.08);
}}
.uuid-box{{
    background:rgba(0,0,0,0.2);
    border:1px solid var(--card-border);
    border-radius:10px;
    padding:7px 12px;
    font-size:9.5px;
    font-family:monospace;
    color:var(--text-dim);
    word-break:break-all;
    margin:6px 0 14px;
    cursor:pointer;
    transition:.15s;
}}
.uuid-box:hover{{
    background:rgba(79,140,255,0.04);
    border-color:rgba(79,140,255,0.15);
}}
.info-grid{{display:grid;gap:8px;margin:14px 0}}
.info-item{{
    background:rgba(0,0,0,0.15);
    border:1px solid var(--card-border);
    border-radius:10px;
    padding:10px 14px;
    display:flex;justify-content:space-between;align-items:center;
}}
.info-label{{font-size:10.5px;color:var(--text-dim);display:flex;align-items:center;gap:6px}}
.info-label i{{font-size:14px;color:var(--primary)}}
.info-value{{font-size:13px;font-weight:700;color:var(--text)}}
.info-value.proto{{
    font-size:10.5px;
    background:rgba(79,140,255,0.06);
    padding:3px 10px;
    border-radius:6px;
    border:1px solid rgba(79,140,255,0.06);
}}
.progress{{margin:16px 0}}
.progress-bar{{
    height:6px;border-radius:4px;
    background:rgba(79,140,255,0.08);overflow:hidden;
}}
.progress-fill{{
    height:100%;border-radius:4px;
    background:linear-gradient(90deg,var(--primary),var(--secondary));
    width:{percent:.1f}%;transition:width 1s ease;
}}
.progress-text{{display:flex;justify-content:space-between;font-size:10.5px;color:var(--text-dim);margin-top:4px}}
.progress-text .pct{{font-weight:700;color:var(--text)}}
.vless-section{{
    background:rgba(0,0,0,0.2);
    border:1px solid var(--card-border);
    border-radius:10px;
    padding:12px 14px;
    margin:14px 0;
}}
.vless-label{{
    font-size:9.5px;color:var(--text-dim);font-weight:700;
    text-transform:uppercase;letter-spacing:.06em;
    display:flex;align-items:center;gap:6px;margin-bottom:6px;
}}
.vless-label i{{color:var(--primary);font-size:12px}}
.vless-link{{
    font-family:monospace;font-size:9.5px;color:var(--primary);
    word-break:break-all;line-height:1.8;
    background:rgba(0,0,0,0.2);padding:8px 10px;
    border-radius:6px;border:1px solid var(--card-border);
}}
.actions{{display:flex;gap:6px;margin-top:12px;flex-wrap:wrap}}
.btn{{
    font-family:inherit;font-size:11px;font-weight:600;
    border-radius:10px;padding:8px 14px;
    cursor:pointer;display:inline-flex;align-items:center;gap:5px;
    border:none;transition:all .2s;white-space:nowrap;flex:1;justify-content:center;
}}
.btn i{{font-size:13px}}
.btn-primary{{
    background:linear-gradient(135deg,var(--primary),var(--secondary));
    color:#fff;box-shadow:0 4px 20px rgba(79,140,255,0.2);
}}
.btn-primary:hover{{transform:translateY(-2px);box-shadow:0 8px 30px rgba(79,140,255,0.35)}}
.btn-secondary{{
    background:rgba(0,0,0,0.2);border:1px solid var(--card-border);
    color:var(--text-dim);
}}
.btn-secondary:hover{{background:rgba(79,140,255,0.06);color:var(--text)}}
.btn-success{{
    background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.1);
    color:#10b981;
}}
.btn-success:hover{{background:rgba(16,185,129,0.12)}}
.footer{{
    margin-top:18px;padding-top:14px;
    border-top:1px solid var(--card-border);
    text-align:center;font-size:9.5px;color:var(--text-muted);
}}
.footer .eagle{{color:var(--primary);font-weight:700}}
.toast{{
    position:fixed;bottom:30px;left:50%;
    transform:translateX(-50%) translateY(60px);
    background:var(--card);backdrop-filter:blur(20px);
    border:1px solid var(--card-border);
    color:var(--text);border-radius:12px;
    padding:10px 20px;font-size:12px;
    opacity:0;transition:all .3s;z-index:999;pointer-events:none;
    display:flex;align-items:center;gap:8px;
}}
.toast.show{{opacity:1;transform:translateX(-50%) translateY(0)}}
.toast.ok{{border-color:rgba(16,185,129,0.2);color:#10b981}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
@keyframes pageIn{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:translateY(0)}}}}
.card{{animation:pageIn .3s ease}}
@media(max-width:500px){{
    .card{{padding:24px 18px 20px}}
    .user-name{{font-size:18px}}
    .brand-icon{{width:40px;height:40px;font-size:20px}}
}}
</style>
</head>
<body>
<div class="toast" id="toast"></div>
<div class="card">
    <div class="brand">
        <div class="brand-icon">🦅</div>
        <div class="brand-text"><div class="name">پنل عقاب</div><div class="sub">اطلاعات اشتراک</div></div>
    </div>
    <div class="user-header">
        <div class="user-name"><span>🦅</span> {label}</div>
        <span class="status {'active' if is_allowed else 'inactive'}">
            <i class="ti {'ti-circle-check' if is_allowed else 'ti-circle-x'}"></i>
            {'فعال' if is_allowed else 'غیرفعال'}
        </span>
    </div>
    <div class="uuid-box" onclick="copyUUID()" title="کلیک برای کپی UUID">🔑 {uuid}</div>

    {conns_html}
    
    {clean_ips_html}

    <div class="info-grid">
        <div class="info-item"><span class="info-label"><i class="ti ti-database"></i> مصرف</span><span class="info-value">{used_fmt}</span></div>
        <div class="info-item"><span class="info-label"><i class="ti ti-package"></i> سهمیه</span><span class="info-value">{limit_fmt}</span></div>
        <div class="info-item"><span class="info-label"><i class="ti ti-calendar"></i> زمان باقیمانده</span><span class="info-value">{days_left if days_left == 'نامحدود' else f'{days_left} روز'}</span></div>
        <div class="info-item"><span class="info-label"><i class="ti ti-devices"></i> دستگاه‌ها</span><span class="info-value">{max_devices if max_devices > 0 else '∞'}</span></div>
        <div class="info-item"><span class="info-label"><i class="ti ti-fingerprint"></i> فینگرپرینت</span><span class="info-value proto">{fingerprint}</span></div>
        <div class="info-item"><span class="info-label"><i class="ti ti-settings"></i> پروتکل</span><span class="info-value proto">{protocol}</span></div>
        <div class="info-item"><span class="info-label"><i class="ti ti-plug"></i> پورت</span><span class="info-value proto">{port}</span></div>
    </div>

    <div class="progress">
        <div class="progress-bar"><div class="progress-fill" style="width:{percent:.1f}%"></div></div>
        <div class="progress-text"><span>میزان مصرف</span><span class="pct">{percent:.1f}%</span></div>
    </div>

    <div class="vless-section">
        <div class="vless-label"><i class="ti ti-link"></i> لینک کانفیگ (VLESS)</div>
        <div class="vless-link" id="vless-link">{main_vless_link}</div>
        {f'''
        <div style="margin-top:8px;font-size:9px;color:var(--text-dim);border-top:1px solid var(--card-border);padding-top:8px">
            <div style="display:flex;align-items:center;gap:4px;margin-bottom:4px">
                <i class="ti ti-cloud" style="color:var(--primary)"></i> لینک‌های با آیپی تمیز:
            </div>
            <div style="display:flex;flex-direction:column;gap:3px">
                {''.join(f'<div style="font-family:monospace;font-size:8.5px;color:#10b981;word-break:break-all;background:rgba(0,0,0,0.1);padding:4px 8px;border-radius:4px">{link}</div>' for link in clean_vless_links)}
            </div>
        </div>
        ''' if clean_vless_links else ''}
    </div>

    <div class="actions">
        <button class="btn btn-primary" onclick="copyVless()"><i class="ti ti-copy"></i> کپی لینک</button>
        <button class="btn btn-success" onclick="copySub()"><i class="ti ti-link"></i> کپی ساب</button>
        <button class="btn btn-secondary" onclick="showQR()"><i class="ti ti-qrcode"></i> QR</button>
    </div>

    <div class="footer"><span class="eagle">🦅</span> پنل عقاب</div>
</div>
<script>
const vless = `{main_vless_link}`;
const subUrl = `{sub_url}`;
const uuid = `{uuid}`;
function toast(msg, type=''){{
    const t=document.getElementById('toast');
    t.textContent=msg;t.className='toast show'+(type?' '+type:'');
    setTimeout(()=>t.classList.remove('show'),2500);
}}
function copyVless(){{navigator.clipboard.writeText(vless).then(()=>toast('✅ لینک کانفیگ کپی شد','ok'));}}
function copySub(){{navigator.clipboard.writeText(subUrl).then(()=>toast('✅ ساب‌لینک کپی شد','ok'));}}
function copyUUID(){{navigator.clipboard.writeText(uuid).then(()=>toast('✅ UUID کپی شد','ok'));}}
function showQR(){{window.open('https://api.qrserver.com/v1/create-qr-code/?size=300x300&data='+encodeURIComponent(vless),'_blank');}}
</script>
</body></html>"""
