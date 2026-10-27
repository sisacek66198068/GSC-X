(() => {
  const form = document.querySelector('#audit-form');
  if (!form) return;
  if (location.hostname === 'command.gds-gsc-x.com' && location.protocol === 'http:') {
    location.replace('https://command.gds-gsc-x.com' + location.pathname + location.search + location.hash);
    return;
  }
  const cs = form.dataset.language === 'cs';
  const preview = document.querySelector('#audit-preview');
  const message = document.querySelector('#audit-message');
  const openEmail = document.querySelector('#audit-open-email');
  const status = document.querySelector('#audit-status');
  const sendStatus = document.querySelector('#audit-send-status');
  const send = document.querySelector('#audit-send');
  const newEnquiry = document.querySelector('#audit-new');
  let requestId = '', payloadSignature = '', sending = false;
  const label = cs ? 'Odeslat poptávku' : 'Send enquiry';
  const value = name => form.elements.namedItem(name).value.trim();
  function payload() {
    return {language:cs?'cs':'en', name:value('name'), company:value('company'), email:value('email'), domain:value('domain'), data:value('data'), problem:value('problem'), website:value('website')};
  }
  function prepare(data) {
    const lines = cs ? [
      'Dobrý den, mám zájem o technický audit GSC-X.', '',
      'Jméno: ' + data.name, 'Organizace: ' + (data.company || 'Neuvedeno'),
      'Kontaktní e-mail: ' + data.email, 'Oblast / systém: ' + data.domain,
      'Dostupnost dat: ' + data.data, '', 'Problém a očekávaný přínos:', data.problem, '',
      'Prosím o návrh rozsahu auditu, potřebných vstupů a dalšího postupu. Před předáním neveřejných dat domluvíme NDA.'
    ] : [
      'Hello, I would like to discuss a GSC-X technical audit.', '',
      'Name: ' + data.name, 'Organization: ' + (data.company || 'Not specified'),
      'Contact email: ' + data.email, 'Domain / system: ' + data.domain,
      'Data availability: ' + data.data, '', 'Problem and expected benefit:', data.problem, '',
      'Please suggest the audit scope, required inputs and next steps. We will agree an NDA before transferring non-public data.'
    ];
    message.value = lines.join('\n');
    const subject = cs ? 'Poptávka technického auditu GSC-X' : 'GSC-X technical audit enquiry';
    openEmail.href = 'mailto:stepanumartin@gds-gsc-x.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(message.value);
  }
  function showPreview() {
    if (!form.reportValidity()) return;
    prepare(payload()); preview.hidden = false;
    status.textContent = cs ? 'Toto je náhled zprávy. Pro přímé odeslání použijte tlačítko Odeslat poptávku.' : 'This is a message preview. Use Send enquiry to submit directly.';
    message.focus({preventScroll:true});
  }
  document.querySelector('#audit-review').addEventListener('click', showPreview);
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (sending || !form.reportValidity()) return;
    const data = payload(); prepare(data);
    const signature = JSON.stringify(data);
    if (signature !== payloadSignature) {
      payloadSignature = signature;
      requestId = typeof crypto.randomUUID === 'function' ? crypto.randomUUID() : Array.from(crypto.getRandomValues(new Uint8Array(16)), n=>n.toString(16).padStart(2,'0')).join('');
    }
    data.requestId = requestId;
    sending = true; send.disabled = true;
    send.textContent = cs ? 'Odesílám…' : 'Sending…';
    sendStatus.textContent = cs ? 'Odesílám poptávku, chvíli prosím vyčkejte.' : 'Sending your enquiry. Please wait.';
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 50000);
    try {
      const response = await fetch(location.hostname === 'command.gds-gsc-x.com' ? '/api/enquiry' : 'https://command.gds-gsc-x.com/api/enquiry', {method:'POST',headers:{'Content-Type':'application/json'},credentials:'omit',body:JSON.stringify(data),signal:controller.signal});
      let result = {};
      if ((response.headers.get('content-type')||'').includes('application/json')) result = await response.json();
      if (!response.ok || result.ok !== true) {
        const error = new Error(result.error || 'unavailable'); error.status = response.status; throw error;
      }
      send.textContent = cs ? 'Odesláno' : 'Sent';
      sendStatus.textContent = (cs ? 'Děkujeme. Poptávka byla předána k odeslání na stepanumartin@gds-gsc-x.com. Ozveme se na uvedený e-mail. Reference: ' : 'Thank you. Your enquiry was accepted for delivery to stepanumartin@gds-gsc-x.com. We will reply to your contact email. Reference: ') + result.reference;
      newEnquiry.hidden = false;
    } catch (error) {
      send.disabled = false; send.textContent = label;
      sendStatus.textContent = error.status === 429 ? (cs ? 'Byl dosažen limit odesílání. Zkuste to později nebo použijte e-mail níže.' : 'The sending limit has been reached. Try again later or use the email option below.') : (cs ? 'Odeslání se nepodařilo potvrdit. Údaje zůstaly vyplněné. Zkuste to znovu nebo použijte e-mail či kopírování zprávy níže.' : 'Sending could not be confirmed. Your details remain filled in. Try again or use the email or copy options below.');
      preview.hidden = false;
      status.textContent = cs ? 'Náhradní způsob: otevřete zprávu ve své poště nebo zkopírujte její text.' : 'Alternative: open the message in your email app or copy its text.';
    } finally {
      clearTimeout(timeout); sending = false;
    }
  });
  newEnquiry.addEventListener('click', () => {
    form.reset(); requestId=''; payloadSignature=''; send.disabled=false; send.textContent=label;
    sendStatus.textContent=''; preview.hidden=true; newEnquiry.hidden=true;
    form.elements.namedItem('name').focus();
  });
  document.querySelector('#audit-copy').addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(message.value);
      status.textContent = cs ? 'Text zkopírován. Vložte jej do e-mailu pro stepanumartin@gds-gsc-x.com.' : 'Message copied. Paste it into an email to stepanumartin@gds-gsc-x.com.';
    } catch {
      message.focus(); message.select();
      status.textContent = cs ? 'Text je označený. Zkopírujte jej pomocí Ctrl+C.' : 'Message selected. Copy it using Ctrl+C.';
    }
  });
})();
