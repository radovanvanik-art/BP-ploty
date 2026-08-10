// Shared across all pages: lightbox, scroll reveal, hamburger menu, mobile CTA bar, back-to-top.
// Each page must set `window.galleryData = [...]` before including this script if it uses the lightbox.

(function(){
  const galleryData = window.galleryData || [];
  let lightboxIndex = 0;
  function showLightboxImage(i){
    if(!galleryData.length) return;
    lightboxIndex = (i + galleryData.length) % galleryData.length;
    const item = galleryData[lightboxIndex];
    document.getElementById('lightboxImg').src = item.full;
    document.getElementById('lightboxImg').alt = item.alt;
  }
  window.openLightbox = function(i){
    showLightboxImage(i);
    document.getElementById('lightbox').classList.add('show');
  };
  window.closeLightbox = function(){
    document.getElementById('lightbox').classList.remove('show');
  };
  window.navLightbox = function(dir){
    showLightboxImage(lightboxIndex + dir);
  };
  const lightbox = document.getElementById('lightbox');
  if(lightbox){
    lightbox.addEventListener('click', function(e){
      if(e.target === this) closeLightbox();
    });
    document.addEventListener('keydown', function(e){
      if(!lightbox.classList.contains('show')) return;
      if(e.key === 'Escape') closeLightbox();
      if(e.key === 'ArrowLeft') navLightbox(-1);
      if(e.key === 'ArrowRight') navLightbox(1);
    });
  }

  // Scroll reveal
  const revealEls = document.querySelectorAll('.reveal');
  const io = new IntersectionObserver((entries)=>{
    entries.forEach(entry=>{
      if(entry.isIntersecting){
        entry.target.classList.add('in');
        io.unobserve(entry.target);
      }
    });
  }, {threshold:0.12});
  revealEls.forEach(el=>io.observe(el));

  // Hamburger / mobile menu
  const hamburgerBtn = document.getElementById('hamburgerBtn');
  const mobileMenu = document.getElementById('mobileMenu');
  if(hamburgerBtn && mobileMenu){
    function toggleMenu(open){
      const isOpen = open !== undefined ? open : !mobileMenu.classList.contains('open');
      mobileMenu.classList.toggle('open', isOpen);
      hamburgerBtn.classList.toggle('open', isOpen);
      hamburgerBtn.setAttribute('aria-expanded', isOpen);
      document.body.style.overflow = isOpen ? 'hidden' : '';
    }
    hamburgerBtn.addEventListener('click', ()=>toggleMenu());
    mobileMenu.querySelectorAll('a').forEach(a=>{
      a.addEventListener('click', ()=>toggleMenu(false));
    });
  }

  // Sticky mobile CTA bar — hide right before the footer so it never overlaps it
  const mobileCtaBar = document.getElementById('mobileCtaBar');
  const footerEl = document.querySelector('footer');
  if(mobileCtaBar && footerEl){
    const barIo = new IntersectionObserver((entries)=>{
      entries.forEach(entry=>{
        mobileCtaBar.classList.toggle('hide', entry.isIntersecting);
      });
    }, {threshold:0.05});
    barIo.observe(footerEl);
  }

  // Back to top
  const toTopBtn = document.getElementById('toTopBtn');
  if(toTopBtn){
    let viewportH = window.innerHeight;
    window.addEventListener('resize', ()=>{ viewportH = window.innerHeight; }, {passive:true});
    let toTopTicking = false;
    window.addEventListener('scroll', ()=>{
      if(toTopTicking) return;
      toTopTicking = true;
      requestAnimationFrame(()=>{
        toTopBtn.classList.toggle('show', window.scrollY > viewportH * 0.9);
        toTopTicking = false;
      });
    }, {passive:true});
    toTopBtn.addEventListener('click', ()=>{
      window.scrollTo({top:0, behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'});
    });
  }
})();
