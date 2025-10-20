(function(){
  // Enhanced React header + background manager without build tools.
  const e = React.createElement;
  const {useState, useEffect} = React;

  function PrefetchImage(src){
    useEffect(()=>{
      if(!src) return;
      const img = new Image(); img.src = src;
      return ()=>{ /* allow GC */ };
    }, [src]);
    return null;
  }

  function Header(props){
    const [menuOpen, setMenuOpen] = useState(false);

    // When menuOpen toggles, open/close the shared overlay element (#mobileNav) in base.html
    useEffect(()=>{
      const overlay = document.getElementById('mobileNav');
      const btn = document.querySelector('.hamburger') || document.querySelector('.menu-toggle');
      if(menuOpen){
        document.body.classList.add('menu-open');
        if(overlay){ overlay.classList.add('open'); overlay.setAttribute('aria-hidden','false'); }
        document.body.style.overflow = 'hidden';
        if(btn) btn.setAttribute('aria-expanded','true');
      } else {
        document.body.classList.remove('menu-open');
        if(overlay){ overlay.classList.remove('open'); overlay.setAttribute('aria-hidden','true'); }
        document.body.style.overflow = '';
        if(btn) btn.setAttribute('aria-expanded','false');
      }
      // ensure Escape closes the overlay
      function onKey(e){ if(e.key === 'Escape' && menuOpen){ setMenuOpen(false); } }
      document.addEventListener('keydown', onKey);
      return ()=> document.removeEventListener('keydown', onKey);
    }, [menuOpen]);

    // close menu when clicking a nav link inside our header
    function handleNavClick(ev){
      if(ev.target && ev.target.tagName === 'A'){
        setMenuOpen(false);
      }
    }

    // also close overlay if an external mobile overlay close button is clicked
    useEffect(()=>{
      const closeBtn = document.getElementById('mobileNavClose');
      function onClose(){ setMenuOpen(false); }
      if(closeBtn) closeBtn.addEventListener('click', onClose);
      return ()=>{ if(closeBtn) closeBtn.removeEventListener('click', onClose); };
    }, []);

    return e('header', {className: 'site-header'},
      e('div', {className: 'topbar'},
        e('div', {className: 'top-left'}, '1800-572-9877 \u00A0 hello@admitionwala.com'),
        e('div', {className: 'top-right'}, props.userAuthenticated ? e('span', null, e('a',{href:'/profile/'},'Profile'), ' \u00A0 | \u00A0 ', e('a',{href:'/logout/'},'Logout')) : e('a',{href:'/login/'},'Login'))
      ),
      e('div', {className: 'header-main'},
  e('div', {className: 'logo'}, e('a',{href:'/'}, e('img',{src: props.logo || STATIC_COLLEGE_LOGO, alt: 'AdmitionWala logo', style:{height:'48px'}}))),
        e('div', {className: 'header-right'},
          e('form', {action: '/colleges/', method: 'get', className: 'header-search'},
            e('input', {name:'q', type:'search', placeholder:'Search colleges, courses or cities', 'aria-label':'Search'}),
            e('button', {type:'submit'}, 'Explore')
          ),
          e('nav', {className: 'main-nav', 'aria-hidden': !menuOpen, style: {display: menuOpen ? 'block' : 'flex'}, onClick: handleNavClick},
            e('ul', {role:'menu'},
              e('li', null, e('a',{href:'/colleges/'},'Explore Colleges')),
              e('li', null, e('a',{href:'/exams/'},'Certified Courses')),
              e('li', null, e('a',{href:'/courses/'},'All Courses')),
              e('li', null, e('a',{href:'/careers/'},'Careers')),
              e('li', null, e('a',{href:'/about/'},'About Us')),
              e('li', null, e('a',{href:'/admition-counseling/'},'Counseling')),
              e('li', null, e('a',{href:'/apply/'},'Apply'))
            )
          ),
          e('button', {className:'hamburger', 'aria-label':'Open menu', 'aria-expanded': menuOpen ? 'true' : 'false', onClick: (ev)=>{ ev.preventDefault(); setMenuOpen(!menuOpen); }},
            e('svg',{viewBox:'0 0 24 18', width:24, height:18, xmlns:'http://www.w3.org/2000/svg', 'aria-hidden':true},
              e('g',{stroke:'currentColor', strokeWidth:2, strokeLinecap:'round'},
                e('path',{className:'bar-top', d:'M2 3h20'}),
                e('path',{className:'bar-mid', d:'M2 9h20'}),
                e('path',{className:'bar-bot', d:'M2 15h20'})
              )
            )
          )
        )
      )
    );
  }

  function App(){
    // STATIC values are injected by Django template via inline script
    const userAuthenticated = window.__DJANGO__ && window.__DJANGO__.user_authenticated;
    const pageBg = window.__DJANGO__ && window.__DJANGO__.page_background_url;
    const logo = window.__DJANGO__ && window.__DJANGO__.static_college_logo;

    // Prefetch background for smoother transitions
    useEffect(()=>{
      if(pageBg){
        const img = new Image(); img.src = pageBg;
        img.onload = ()=>{ document.documentElement.style.setProperty('--page-bg-url', `url('${pageBg}')`); };
        img.onerror = ()=>{ /* keep fallback */ };
      }
    }, [pageBg]);

    return e(React.Fragment, null,
      e(PrefetchImage, {src: pageBg}),
      e(Header, {userAuthenticated: userAuthenticated, logo: logo})
    );
  }

  // Render on DOMContentLoaded
  document.addEventListener('DOMContentLoaded', function(){
    // Inject STATIC_COLLEGE_LOGO constant (fallback)
    window.STATIC_COLLEGE_LOGO = (window.__DJANGO__ && window.__DJANGO__.static_college_logo) || '/static/college_logo.svg';
    const mount = document.getElementById('react-root');
    if(mount){
      ReactDOM.createRoot(mount).render(React.createElement(App));
    }
  });
})();
