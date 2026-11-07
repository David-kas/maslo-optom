(function () {
  'use strict';

  var DEMO = true;

  document.querySelectorAll('[data-request-form]').forEach(function (root) {
    var product = 'Жмых';
    var picks = root.querySelectorAll('[data-product-pick]');
    var volume = root.querySelector('[name="volume"]');
    var company = root.querySelector('[name="company"]');
    var contact = root.querySelector('[name="contact"]');
    var consent = root.querySelector('[name="consent"]');
    var errorEl = root.querySelector('[data-form-error]');
    var successEl = root.querySelector('[data-form-success]');
    var form = root.querySelector('form');
    var prefill = root.getAttribute('data-prefill-product');
    if (prefill) {
      product = prefill;
    }

    function setProduct(next) {
      product = next;
      picks.forEach(function (btn) {
        var on = btn.getAttribute('data-product-pick') === next;
        btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
    }

    picks.forEach(function (btn) {
      btn.addEventListener('click', function () {
        setProduct(btn.getAttribute('data-product-pick'));
      });
    });
    setProduct(product);

    if (!form) return;

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (errorEl) errorEl.hidden = true;
      var c = company && company.value.trim();
      var ct = contact && contact.value.trim();
      if (!c || !ct) {
        if (errorEl) {
          errorEl.textContent = 'Укажите компанию и телефон или email.';
          errorEl.hidden = false;
        }
        return;
      }
      if (consent && !consent.checked) {
        if (errorEl) {
          errorEl.textContent = 'Нужно согласие на обработку персональных данных.';
          errorEl.hidden = false;
        }
        return;
      }
      if (DEMO) {
        if (form) form.hidden = true;
        if (successEl) {
          var vol = volume && volume.value.trim();
          successEl.innerHTML =
            '<p role="status"><strong>Демонстрационный режим.</strong> Заявка не отправлена на сервер. ' +
            'Свяжитесь с менеджером по телефону или email. Черновик: ' +
            escapeHtml(c) + ', ' + escapeHtml(product.toLowerCase()) +
            (vol ? ', ' + escapeHtml(vol) + ' т' : '') + ', контакт ' + escapeHtml(ct) + '.</p>' +
            '<button type="button" class="btn-cta" data-form-reset>Новая заявка</button>';
          successEl.hidden = false;
          successEl.querySelector('[data-form-reset]').addEventListener('click', function () {
            if (form) {
              form.reset();
              form.hidden = false;
            }
            successEl.hidden = true;
            setProduct(prefill || 'Жмых');
          });
        }
        return;
      }
    });
  });

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
})();
