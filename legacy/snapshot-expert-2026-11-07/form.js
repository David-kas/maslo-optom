(function () {
  'use strict';

  var API = '/api/callback';

  function digitsPhone(s) {
    return String(s || '').replace(/\D/g, '');
  }

  function validRuPhone(d) {
    if (d.length === 11 && (d[0] === '7' || d[0] === '8')) return true;
    if (d.length === 10 && d[0] === '9') return true;
    return false;
  }

  function formatPhoneHint(input) {
    input.addEventListener('input', function () {
      var d = digitsPhone(input.value);
      if (d.length > 11) d = d.slice(0, 11);
      if (!d) { input.value = ''; return; }
      if (d[0] === '8') d = '7' + d.slice(1);
      if (d[0] !== '7' && d.length <= 10) d = '7' + d;
      var out = '+7';
      if (d.length > 1) out += ' (' + d.slice(1, 4);
      if (d.length >= 4) out += ') ' + d.slice(4, 7);
      if (d.length >= 7) out += '-' + d.slice(7, 9);
      if (d.length >= 9) out += '-' + d.slice(9, 11);
      input.value = out;
    });
  }

  function setStatus(root, kind, text) {
    var el = root.querySelector('[data-form-status]');
    if (!el) return;
    el.hidden = !text;
    el.dataset.kind = kind || 'info';
    el.textContent = text || '';
  }

  document.querySelectorAll('[data-callback-form]').forEach(function (root) {
    var form = root.querySelector('form');
    var nameInput = root.querySelector('[name="name"]');
    var phoneInput = root.querySelector('[name="phone"]');
    var consent = root.querySelector('[name="consent"]');
    if (phoneInput) formatPhoneHint(phoneInput);

    if (!form) return;

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      setStatus(root, 'info', '');

      var name = nameInput && nameInput.value.trim();
      var phone = phoneInput && digitsPhone(phoneInput.value);
      var hp = root.querySelector('[name="website"]');

      if (hp && hp.value) return;

      if (!name || name.length < 2) {
        setStatus(root, 'error', 'Укажите, как к вам обращаться (имя).');
        nameInput && nameInput.focus();
        return;
      }
      if (!validRuPhone(phone)) {
        setStatus(root, 'error', 'Укажите корректный российский номер телефона, например +7 (909) 339-81-67.');
        phoneInput && phoneInput.focus();
        return;
      }
      if (consent && !consent.checked) {
        setStatus(root, 'error', 'Нужно согласие на обработку персональных данных.');
        return;
      }

      var btn = form.querySelector('[type="submit"]');
      if (btn) btn.disabled = true;

      fetch(API, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ name: name, phone: phone, consent: true }),
      })
        .then(function (res) {
          return res.json().then(function (data) {
            return { res: res, data: data };
          });
        })
        .then(function (pack) {
          if (pack.res.ok && pack.data && pack.data.ok) {
            setStatus(root, 'ok', 'Заявка принята. Мы перезвоним по указанному номеру.');
            form.reset();
            return;
          }
          if (pack.res.status === 503 && pack.data && pack.data.code === 'NOT_CONFIGURED') {
            setStatus(
              root,
              'error',
              'Отправка пока не настроена на сервере. Позвоните по телефону в шапке или напишите на email в контактах.'
            );
            return;
          }
          var msg = (pack.data && pack.data.message) || 'Не удалось отправить заявку. Попробуйте позже или позвоните нам.';
          setStatus(root, 'error', msg);
        })
        .catch(function () {
          setStatus(
            root,
            'error',
            'Сервер недоступен (откройте сайт через локальный сервер: py -3 server/app.py). Или позвоните по телефону.'
          );
        })
        .finally(function () {
          if (btn) btn.disabled = false;
        });
    });
  });
})();
