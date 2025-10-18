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
    useEffect(()=>{ document.body.classList.toggle('menu-open', menuOpen); }, [menuOpen]);
    // close menu when route changes or when clicking a link
    function handleNavClick(ev){ if(ev.target && ev.target.tagName === 'A'){ setMenuOpen(false); } }
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
          e('button', {className:'hamburger', 'aria-label':'Open menu', 'aria-expanded': menuOpen ? 'true' : 'false', onClick: (ev)=>{ ev.preventDefault(); setMenuOpen(!menuOpen); }}, '☰')
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
