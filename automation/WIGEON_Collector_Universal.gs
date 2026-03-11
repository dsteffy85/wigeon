/**
 * 🦆 WIGEON Universal Report Collector
 * 
 * ONE-TIME SETUP:
 * 1. Edit YOUR_VENDOR_EMAIL below
 * 2. Run "setup" once
 * 3. Done! Reports collected daily at 7 AM
 */

// ═══════════════════════════════════════════════════════════════
// ✏️ STEP 1: ENTER YOUR VENDOR'S EMAIL ADDRESS HERE:
// ═══════════════════════════════════════════════════════════════

const VENDOR_EMAIL = 'YOUR_VENDOR_EMAIL@example.com';

// ═══════════════════════════════════════════════════════════════
// ✏️ STEP 2: SELECT "setup" FROM DROPDOWN AND CLICK RUN ▶️
// ═══════════════════════════════════════════════════════════════


// ============ CONFIGURATION (Don't edit below) ============
const FOLDER_NAME = 'WIGEON_Reports';
const PROCESSED_LABEL = 'WIGEON_Processed';
const DAYS_TO_SEARCH = 7;


// ============ SETUP (Run Once) ============

/**
 * Run this ONCE to set up WIGEON
 */
function setup() {
  // Validate email first
  if (!VENDOR_EMAIL || !VENDOR_EMAIL.includes('@') || VENDOR_EMAIL === 'YOUR_VENDOR_EMAIL@example.com') {
    Logger.log('❌ ERROR: Please edit VENDOR_EMAIL at the top of the script first!');
    Logger.log('');
    Logger.log('   Look for this line near the top:');
    Logger.log('   const VENDOR_EMAIL = "YOUR_VENDOR_EMAIL@example.com";');
    Logger.log('');
    Logger.log('   Change it to your vendor\'s email, e.g.:');
    Logger.log('   const VENDOR_EMAIL = "reports@vendor.com";');
    Logger.log('');
    Logger.log('   Then run setup again.');
    return;
  }
  
  // Create folder
  const folder = getOrCreateFolder();
  Logger.log('✅ Folder ready: ' + folder.getUrl());
  
  // Create label
  getOrCreateLabel();
  Logger.log('✅ Label ready: ' + PROCESSED_LABEL);
  
  // Create daily trigger
  createDailyTrigger();
  Logger.log('✅ Daily trigger set for 7 AM');
  
  // Initialize sender list with the configured email
  const props = PropertiesService.getScriptProperties();
  let senders = JSON.parse(props.getProperty('senders') || '[]');
  
  if (!senders.includes(VENDOR_EMAIL.toLowerCase())) {
    senders.push(VENDOR_EMAIL.toLowerCase());
    props.setProperty('senders', JSON.stringify(senders));
    Logger.log('✅ Added sender: ' + VENDOR_EMAIL);
  } else {
    Logger.log('✅ Sender already configured: ' + VENDOR_EMAIL);
  }
  
  Logger.log('');
  Logger.log('═══════════════════════════════════════════════');
  Logger.log('🦆 WIGEON Setup Complete!');
  Logger.log('═══════════════════════════════════════════════');
  Logger.log('');
  Logger.log('📧 Tracking: ' + VENDOR_EMAIL);
  Logger.log('📁 Folder: ' + folder.getUrl());
  Logger.log('⏰ Schedule: Daily at 7 AM');
  Logger.log('');
  Logger.log('💡 To test now, select "collectNow" and click Run.');
  Logger.log('💡 To add more senders, use "addSender" function.');
}


/**
 * Add another email sender to track (for additional vendors)
 * 
 * ⚠️ EDIT THE EMAIL BELOW, THEN RUN THIS FUNCTION
 */
function addSender() {
  // ═══════════════════════════════════════════════════
  // ✏️ EDIT THIS EMAIL ADDRESS, THEN RUN THE FUNCTION:
  // ═══════════════════════════════════════════════════
  
  const newSender = 'ANOTHER_VENDOR@example.com';
  
  // ═══════════════════════════════════════════════════
  
  // Get current senders
  const props = PropertiesService.getScriptProperties();
  let senders = JSON.parse(props.getProperty('senders') || '[]');
  
  // Validate
  if (!newSender || !newSender.includes('@') || newSender === 'ANOTHER_VENDOR@example.com') {
    Logger.log('❌ Please edit the email address in the addSender() function first!');
    Logger.log('   Look for: const newSender = "..."');
    return;
  }
  
  // Check if already exists
  if (senders.includes(newSender.toLowerCase())) {
    Logger.log('⚠️ Sender already added: ' + newSender);
    Logger.log('');
    Logger.log('📧 Currently tracking ' + senders.length + ' sender(s):');
    senders.forEach(s => Logger.log('   • ' + s));
    return;
  }
  
  // Add sender
  senders.push(newSender.toLowerCase());
  props.setProperty('senders', JSON.stringify(senders));
  
  Logger.log('✅ Added sender: ' + newSender);
  Logger.log('');
  Logger.log('📧 Currently tracking ' + senders.length + ' sender(s):');
  senders.forEach(s => Logger.log('   • ' + s));
  Logger.log('');
  Logger.log('🦆 Reports will be collected daily at 7 AM!');
  Logger.log('');
  Logger.log('💡 To add another sender, edit the email and run addSender() again.');
}


/**
 * View all tracked senders
 */
function listSenders() {
  const props = PropertiesService.getScriptProperties();
  const senders = JSON.parse(props.getProperty('senders') || '[]');
  
  Logger.log('📧 Currently tracking ' + senders.length + ' sender(s):');
  if (senders.length === 0) {
    Logger.log('   (none - run "setup" first)');
  } else {
    senders.forEach(s => Logger.log('   • ' + s));
  }
}


/**
 * Remove a sender from tracking
 */
function removeSender() {
  const props = PropertiesService.getScriptProperties();
  let senders = JSON.parse(props.getProperty('senders') || '[]');
  
  if (senders.length === 0) {
    Logger.log('❌ No senders to remove');
    return;
  }
  
  Logger.log('Current senders:');
  senders.forEach((s, i) => Logger.log('   ' + i + ': ' + s));
  Logger.log('');
  Logger.log('To remove a sender, edit the "indexToRemove" variable below and run again.');
  
  // ═══════════════════════════════════════════════════
  // ✏️ EDIT THIS NUMBER TO REMOVE A SENDER (0, 1, 2...):
  // ═══════════════════════════════════════════════════
  const indexToRemove = -1;
  // ═══════════════════════════════════════════════════
  
  if (indexToRemove >= 0 && indexToRemove < senders.length) {
    const removed = senders.splice(indexToRemove, 1);
    props.setProperty('senders', JSON.stringify(senders));
    Logger.log('✅ Removed: ' + removed[0]);
  }
}


// ============ COLLECTION (Runs Automatically) ============

/**
 * Main collection function - runs daily at 7 AM
 */
function collectReports() {
  const props = PropertiesService.getScriptProperties();
  const senders = JSON.parse(props.getProperty('senders') || '[]');
  
  if (senders.length === 0) {
    Logger.log('⚠️ No senders configured. Run "setup" first.');
    return;
  }
  
  const folder = getOrCreateFolder();
  const label = getOrCreateLabel();
  
  // Build search query for all senders
  const senderQuery = senders.map(s => 'from:' + s).join(' OR ');
  const searchQuery = '(' + senderQuery + ') has:attachment newer_than:' + DAYS_TO_SEARCH + 'd -label:' + PROCESSED_LABEL;
  
  Logger.log('🔍 Searching: ' + searchQuery);
  
  const threads = GmailApp.search(searchQuery);
  Logger.log('📧 Found ' + threads.length + ' email thread(s)');
  
  let savedCount = 0;
  
  threads.forEach(thread => {
    const messages = thread.getMessages();
    messages.forEach(message => {
      const attachments = message.getAttachments();
      const date = Utilities.formatDate(message.getDate(), 'America/Los_Angeles', 'yyyy-MM-dd');
      const sender = message.getFrom().match(/<(.+)>/)?.[1] || message.getFrom();
      
      attachments.forEach(attachment => {
        const name = attachment.getName();
        
        // Only save Excel, CSV, XML, ZIP files
        if (name.match(/\.(xlsx?|csv|xml|zip)$/i)) {
          const fileName = date + '_' + name.replace(/[^a-zA-Z0-9._-]/g, '_');
          
          // Check if already exists
          const existing = folder.getFilesByName(fileName);
          if (!existing.hasNext()) {
            folder.createFile(attachment.copyBlob().setName(fileName));
            Logger.log('✅ Saved: ' + fileName);
            savedCount++;
          }
        }
      });
    });
    
    // Mark as processed
    thread.addLabel(label);
  });
  
  Logger.log('');
  Logger.log('🦆 WIGEON Collection Complete!');
  Logger.log('   Saved ' + savedCount + ' new file(s)');
  Logger.log('   Folder: ' + folder.getUrl());
}


/**
 * Manual run - collect reports now
 */
function collectNow() {
  collectReports();
}


// ============ HELPERS ============

function getOrCreateFolder() {
  const folders = DriveApp.getFoldersByName(FOLDER_NAME);
  if (folders.hasNext()) {
    return folders.next();
  }
  return DriveApp.createFolder(FOLDER_NAME);
}

function getOrCreateLabel() {
  let label = GmailApp.getUserLabelByName(PROCESSED_LABEL);
  if (!label) {
    label = GmailApp.createLabel(PROCESSED_LABEL);
  }
  return label;
}

function createDailyTrigger() {
  // Remove existing triggers
  ScriptApp.getProjectTriggers().forEach(trigger => {
    if (trigger.getHandlerFunction() === 'collectReports') {
      ScriptApp.deleteTrigger(trigger);
    }
  });
  
  // Create new daily trigger at 7 AM
  ScriptApp.newTrigger('collectReports')
    .timeBased()
    .atHour(7)
    .everyDays(1)
    .create();
}
