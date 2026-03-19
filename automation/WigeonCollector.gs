/**
 * 🦆 WIGEON Universal Report Collector
 * Google Apps Script — collects email attachments from any sender
 *
 * SETUP:
 *   1. Go to script.google.com → New Project
 *   2. Paste this entire script
 *   3. Run the "setup" function once (it will ask for permissions)
 *   4. Edit VENDOR_EMAIL below, then run "addFirstSender"
 *   5. Done! Reports are collected daily at 7 AM.
 *
 * To add more senders later, edit the email in addSender() and run it.
 */

// ═══════════════════════════════════════════════════════════════
// CONFIGURATION
// ═══════════════════════════════════════════════════════════════
const FOLDER_NAME = 'WIGEON_Reports';
const PROCESSED_LABEL = 'WIGEON_Processed';
const DAYS_TO_SEARCH = 7;
const MAX_COPIES_PER_REPORT = 2;

// ═══════════════════════════════════════════════════════════════
// SETUP — Run once
// ═══════════════════════════════════════════════════════════════

function setup() {
  const folder = getOrCreateFolder();
  Logger.log('✅ Folder ready: ' + folder.getUrl());

  getOrCreateLabel();
  Logger.log('✅ Label ready: ' + PROCESSED_LABEL);

  createDailyTrigger();
  Logger.log('✅ Daily trigger set for 7 AM');

  const props = PropertiesService.getScriptProperties();
  if (!props.getProperty('senders')) {
    props.setProperty('senders', '[]');
  }

  Logger.log('');
  Logger.log('🦆 WIGEON Setup Complete!');
  Logger.log('   Folder ID: ' + folder.getId());
  Logger.log('');
  Logger.log('Next: Edit the email in addFirstSender() and run it.');
}

// ═══════════════════════════════════════════════════════════════
// SENDER MANAGEMENT
// ═══════════════════════════════════════════════════════════════

/**
 * Add your first vendor email.
 * ✏️ Change the email below, then run this function.
 */
function addFirstSender() {
  _addSenderEmail('ENTER_VENDOR_EMAIL@example.com');
}

/**
 * Add another vendor email.
 * ✏️ Change the email below, then run this function.
 */
function addSender() {
  _addSenderEmail('ENTER_ANOTHER_EMAIL@example.com');
}

function _addSenderEmail(email) {
  const props = PropertiesService.getScriptProperties();
  let senders = JSON.parse(props.getProperty('senders') || '[]');

  if (!email || !email.includes('@') || email.startsWith('ENTER_')) {
    Logger.log('❌ Edit the email address in the function first!');
    Logger.log('   Replace ENTER_...@example.com with a real address.');
    return;
  }

  if (senders.includes(email.toLowerCase())) {
    Logger.log('⚠️  Already tracking: ' + email);
    _logSenders(senders);
    return;
  }

  senders.push(email.toLowerCase());
  props.setProperty('senders', JSON.stringify(senders));
  Logger.log('✅ Added: ' + email);
  _logSenders(senders);
}

function listSenders() {
  const senders = JSON.parse(
    PropertiesService.getScriptProperties().getProperty('senders') || '[]'
  );
  _logSenders(senders);
}

function removeSender() {
  const props = PropertiesService.getScriptProperties();
  let senders = JSON.parse(props.getProperty('senders') || '[]');

  if (senders.length === 0) {
    Logger.log('No senders configured.');
    return;
  }

  Logger.log('Current senders:');
  senders.forEach((s, i) => Logger.log('  ' + i + ': ' + s));
  Logger.log('');
  Logger.log('To remove, change indexToRemove below and re-run.');

  // ✏️ Set to 0, 1, 2… to remove that sender:
  const indexToRemove = -1;

  if (indexToRemove >= 0 && indexToRemove < senders.length) {
    const removed = senders.splice(indexToRemove, 1);
    props.setProperty('senders', JSON.stringify(senders));
    Logger.log('✅ Removed: ' + removed[0]);
  }
}

function _logSenders(senders) {
  Logger.log('📧 Tracking ' + senders.length + ' sender(s):');
  if (senders.length === 0) {
    Logger.log('   (none)');
  } else {
    senders.forEach(s => Logger.log('   • ' + s));
  }
}

// ═══════════════════════════════════════════════════════════════
// COLLECTION — Runs daily at 7 AM
// ═══════════════════════════════════════════════════════════════

function collectReports() {
  const props = PropertiesService.getScriptProperties();
  const senders = JSON.parse(props.getProperty('senders') || '[]');

  if (senders.length === 0) {
    Logger.log('⚠️  No senders. Run setup + addFirstSender first.');
    return;
  }

  const folder = getOrCreateFolder();
  const label = getOrCreateLabel();

  const senderQuery = senders.map(s => 'from:' + s).join(' OR ');
  const query = '(' + senderQuery + ') has:attachment newer_than:'
    + DAYS_TO_SEARCH + 'd -label:' + PROCESSED_LABEL;

  Logger.log('🔍 ' + query);

  const threads = GmailApp.search(query);
  Logger.log('📧 ' + threads.length + ' thread(s)');

  let saved = 0;

  threads.forEach(thread => {
    thread.getMessages().forEach(msg => {
      const date = Utilities.formatDate(
        msg.getDate(), 'America/Los_Angeles', 'yyyy-MM-dd'
      );

      msg.getAttachments().forEach(att => {
        const name = att.getName();
        if (name.match(/\.(xlsx?|csv|xml|zip)$/i)) {
          const safeName = date + '_' + name.replace(/[^a-zA-Z0-9._-]/g, '_');
          if (!folder.getFilesByName(safeName).hasNext()) {
            folder.createFile(att.copyBlob().setName(safeName));
            Logger.log('✅ ' + safeName);
            saved++;
          }
        }
      });
    });
    thread.addLabel(label);
  });

  const deleted = cleanupOldFiles(folder);

  Logger.log('');
  Logger.log('🦆 Done — saved ' + saved + ', cleaned ' + deleted);
  Logger.log('   ' + folder.getUrl());
}

function collectNow() {
  collectReports();
}

// ═══════════════════════════════════════════════════════════════
// RETENTION — keep only N most recent per report type
// ═══════════════════════════════════════════════════════════════

function cleanupOldFiles(folder) {
  if (!folder) folder = getOrCreateFolder();

  const files = folder.getFiles();
  const byType = {};

  while (files.hasNext()) {
    const file = files.next();
    const name = file.getName();
    if (name.startsWith('_')) continue;

    const reportType = name.replace(/^\d{4}-\d{2}-\d{2}_/, '');
    if (!byType[reportType]) byType[reportType] = [];
    byType[reportType].push({
      file: file,
      name: name,
      date: name.substring(0, 10),
    });
  }

  let deleted = 0;
  for (const type in byType) {
    const list = byType[type].sort((a, b) => b.date.localeCompare(a.date));
    for (let i = MAX_COPIES_PER_REPORT; i < list.length; i++) {
      Logger.log('🗑️ ' + list[i].name);
      list[i].file.setTrashed(true);
      deleted++;
    }
  }
  return deleted;
}

function cleanupNow() {
  const deleted = cleanupOldFiles(getOrCreateFolder());
  Logger.log('Cleaned ' + deleted + ' file(s).');
}

// ═══════════════════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════════════════

function getOrCreateFolder() {
  const it = DriveApp.getFoldersByName(FOLDER_NAME);
  return it.hasNext() ? it.next() : DriveApp.createFolder(FOLDER_NAME);
}

function getOrCreateLabel() {
  let label = GmailApp.getUserLabelByName(PROCESSED_LABEL);
  return label || GmailApp.createLabel(PROCESSED_LABEL);
}

function createDailyTrigger() {
  ScriptApp.getProjectTriggers().forEach(t => {
    if (t.getHandlerFunction() === 'collectReports') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('collectReports')
    .timeBased()
    .atHour(7)
    .everyDays(1)
    .create();
}
