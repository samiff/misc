// ==UserScript==
// @name         LED Notifier
// @description  Listen for events and call the LED Notifier API.
// @version      1.0.0
// @namespace    https://github.com/samiff/misc/projects/led-notifier
// @author       Samiff
// @match        https://app.slack.com/client/*
// @match        https://mail.google.com/mail/*
// @connect      10.0.0.41
// @grant        GM_xmlhttpRequest
// @downloadURL  none
// ==/UserScript==

const options = {
  consoleLogRequests: true,
  interval: 1000 * 10,
  apiBaseUrl: "http://10.0.0.41/api",
};

function doRequest(url) {
  options.consoleLogRequests &&
    console.log(`LED Notifier - requesting URL: ${url}`);
  try {
    GM_xmlhttpRequest({
      method: "GET",
      url: url,
    });
  } catch (error) {
    console.log("LED Notifier - error making fetch request:", error);
  }
}

// Slack Listener
if (window.location.href.startsWith("https://app.slack.com/client")) {
  let slackStatus = 0; // Default of 0 for LED_1 off (no DMs), 1 for LED_1 on (has unread DMs).
  window.setInterval(() => {
    const el = document.querySelector(
      "#Pdms .p-channel_sidebar__link--unread"
    );
    if (el && slackStatus === 0) {
      slackStatus = 1;
      doRequest(`${options.apiBaseUrl}/?led_1=1&source=slack-work`);
    } else if (el === null && slackStatus === 1) {
      slackStatus = 0;
      doRequest(`${options.apiBaseUrl}/?led_1=0&source=slack-work`);
    }
  }, options.interval);
}

// Gmail Chat Listener
if (window.location.href.startsWith("https://mail.google.com/mail")) {
  let gmailStatus = 0; // Default of 0 for LED_2 off (no chats), 1 for LED_2 on (has unread chats).
  window.setInterval(() => {
    const el = document.querySelector("div[data-tooltip='Chat']");
    const hasChats =
      el && el.getAttribute("aria-label") !== "Chat, 0 unread messages";
    if (hasChats && gmailStatus === 0) {
      gmailStatus = 1;
      doRequest(`${options.apiBaseUrl}/?led_2=1&source=gmail-chat`);
    } else if (!hasChats && gmailStatus === 1) {
      gmailStatus = 0;
      doRequest(`${options.apiBaseUrl}/?led_2=0&source=gmail-chat`);
    }
  }, options.interval);
}
