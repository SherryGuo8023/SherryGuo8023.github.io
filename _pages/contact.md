---
permalink: /contact/
title: "Contact"
author_profile: true
---

Leave me a message here. It goes straight to my inbox. An email address is optional; include one if you would like a reply.

<div id="contact-sent" hidden style="padding: 0.8em 1em; margin-bottom: 1.5em; border-left: 4px solid #52adc8; background: #f2f9fb;">
  Thanks, your message has been sent.
</div>

<form id="contact-form" action="https://api.web3forms.com/submit" method="POST" style="max-width: 40em;">
  <input type="hidden" name="access_key" value="9f416cc0-9fbb-496c-b33e-6d7fe7a76b90">
  <input type="hidden" name="subject" value="New message from sherryguo8023.github.io">
  <input type="hidden" name="from_name" value="Personal website">
  <input type="hidden" name="redirect" value="https://sherryguo8023.github.io/contact/?sent=1">
  <input type="checkbox" name="botcheck" tabindex="-1" autocomplete="off" style="display: none;">

  <p>
    <label for="contact-name">Name</label><br>
    <input id="contact-name" type="text" name="name" required style="width: 100%; padding: 0.5em;">
  </p>
  <p>
    <label for="contact-email">Email (optional)</label><br>
    <input id="contact-email" type="email" name="email" style="width: 100%; padding: 0.5em;">
  </p>
  <p>
    <label for="contact-message">Message</label><br>
    <textarea id="contact-message" name="message" rows="7" required style="width: 100%; padding: 0.5em;"></textarea>
  </p>
  <p>
    <button type="submit" class="btn btn--primary">Send</button>
  </p>
</form>

<script>
  if (new URLSearchParams(window.location.search).get('sent') === '1') {
    document.getElementById('contact-sent').hidden = false;
    document.getElementById('contact-form').hidden = true;
  }
</script>
