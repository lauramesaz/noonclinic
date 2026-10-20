// noon Clinic · medición de Google Ads (clic a WhatsApp) para las landings (criolipólisis y promos), que no cargan noon.js.
// COPIA EXACTA del primer bloque de assets/noon.js. Si cambia allá, actualizar aquí.
// El consentimiento se guarda con la misma clave, así que la elección sirve en toda la web.
// Noon Clinic: medición de visitas y clics a WhatsApp (Google Ads), sin datos clínicos ni personales.
// Desde el 19-oct-2026 (decisión de Laura, igual que en Seravena) la medición está PRENDIDA por defecto y ya no sale ningún
// aviso que estorbe. En Europa sigue apagada hasta que la persona la permita (lo pone la cabecera: HEAD_MEDICION en build.py).
// Quien quiera desactivarla lo hace en "Preferencias de medición", la línea pequeña al final de cada página.
(function () {
  'use strict';
  var KEY = 'noon_measurement_consent_v1';
  var TAG = 'AW-18513507492';
  var EVENT = TAG + '/9R4bCKTkjZ0dEKTp9vtE';
  var consent = null, loaded = false, reported = false;
  var english = document.documentElement.lang === 'en';
  try { consent = localStorage.getItem(KEY); } catch (_) {}
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  function state(allowed) {
    return {ad_storage: allowed ? 'granted' : 'denied',
      ad_user_data: allowed ? 'granted' : 'denied',
      ad_personalization: 'denied', analytics_storage: allowed ? 'granted' : 'denied'};
  }
  if (!window.__noonConsentDefault) window.gtag('consent', 'default', state(consent !== 'no'));  // normalmente ya lo puso la cabecera (Tag Manager)
  window.gtag('set', 'allow_ad_personalization_signals', false);
  window.gtag('set', 'ads_data_redaction', true);
  function start() {
    if (loaded) return;
    loaded = true;
    // No transmitir procedimientos, textos de WhatsApp ni parámetros personales.
    var safeURL = new URL('/', location.origin);
    var query = new URLSearchParams(location.search);
    ['gclid', 'gbraid', 'wbraid'].forEach(function (key) {
      var value = query.get(key);
      if (value && /^[A-Za-z0-9_-]{1,512}$/.test(value)) safeURL.searchParams.set(key, value);
    });
    window.gtag('js', new Date());
    window.gtag('config', TAG, {allow_ad_personalization_signals: false,
      allow_google_signals: false, page_location: safeURL.href,
      page_title: 'Noon Clinic', page_referrer: ''});
    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + TAG;
    document.head.appendChild(script);
  }
  if (consent !== 'no') start();
  // Panel de preferencias: ya NO aparece solo; se abre desde la línea del pie de página.
  var panel = document.createElement('section');
  panel.setAttribute('role', 'region');
  panel.setAttribute('aria-label', english ? 'Measurement preferences' : 'Preferencias de medición');
  panel.style.cssText = 'position:fixed;bottom:84px;left:16px;right:16px;max-width:560px;padding:20px;background:#fff;color:#202020;border:1px solid #ccc;border-radius:12px;box-shadow:0 4px 24px #0002;z-index:10000;font:15px/1.5 system-ui,sans-serif';
  var text = document.createElement('p');
  text.style.cssText = 'margin:0 0 14px';
  text.textContent = english
    ? 'We measure visits and clicks to WhatsApp with Google Analytics, Google Ads and Microsoft Clarity, without personal data. You can turn it off at any time; it will not affect your access to the website or WhatsApp.'
    : 'Medimos visitas y clics a WhatsApp con Google Analytics, Google Ads y Microsoft Clarity, sin datos personales. Puedes desactivarlo cuando quieras; no afecta tu acceso a la web ni a WhatsApp.';
  panel.appendChild(text);
  function choose(value) {
    consent = value;
    try { localStorage.setItem(KEY, value); } catch (_) {}
    window.gtag('consent', 'update', state(value === 'yes'));
    if (value === 'yes') start();
    panel.hidden = true;
  }
  [['no', english ? 'Turn off' : 'Desactivar'], ['yes', english ? 'Allow' : 'Permitir']].forEach(function (item) {
    var button = document.createElement('button');
    button.type = 'button'; button.textContent = item[1];
    button.style.cssText = 'padding:10px 18px;margin:0 10px 0 0;border:1px solid #555;border-radius:6px;background:#fff;color:#222;font:inherit;cursor:pointer';
    button.addEventListener('click', function () { choose(item[0]); });
    panel.appendChild(button);
  });
  panel.hidden = true;
  document.body.appendChild(panel);
  var settings = document.createElement('button');
  settings.type = 'button';
  settings.textContent = english ? 'Measurement preferences' : 'Preferencias de medición';
  settings.style.cssText = 'display:block;margin:14px auto 0;padding:6px 8px;background:transparent;border:0;color:inherit;opacity:.7;font:inherit;font-size:13px;text-decoration:underline;text-underline-offset:3px;cursor:pointer';
  settings.addEventListener('click', function () { panel.hidden = false; panel.querySelector('button').focus(); });
  (document.querySelector('footer') || document.body).appendChild(settings);
  function track(event) {
    if (consent === 'no' || reported || (event.type === 'auxclick' && event.button !== 1)) return;
    var link = event.target && event.target.closest ? event.target.closest('a[href]') : null;
    if (!link) return;
    var url;
    try { url = new URL(link.href, location.href); } catch (_) { return; }
    var isNoon = (url.hostname === 'wa.me' && url.pathname.replace(/\/$/, '') === '/573022491937') ||
      (url.hostname === 'api.whatsapp.com' && url.searchParams.get('phone') === '573022491937');
    if (!isNoon) return;
    reported = true;
    window.gtag('event', 'conversion', {send_to: EVENT, value: 0, currency: 'COP'});
    // No bloquear ni modificar la navegación a WhatsApp.
  }
  document.addEventListener('click', track);
  document.addEventListener('auxclick', track);
})();
