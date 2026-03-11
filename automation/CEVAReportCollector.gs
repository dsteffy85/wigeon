/**
 * WIGEON - CEVA Report Collector
 * Google Apps Script for 100% Automated Email Attachment Processing
 * 
 * This script:
 * 1. Searches Gmail for CEVA reports from ops_reporting@example.com
 * 2. Downloads attachments (Excel files)
 * 3. Saves them to a Google Drive folder
 * 4. Marks emails as processed (adds label)
 * 
 * Setup Instructions:
 * 1. Go to https://script.google.com
 * 2. Create a new project named "WIGEON CEVA Collector"
 * 3. Paste this entire script
 * 4. Run setupScript() once to create folder and label
 * 5. Set up a trigger to run collectCEVAReports() hourly or daily
 * 
 * @author WIGEON Automation
 * @version 1.0
 * @date 2026-03-10
 */

// ============================================
// CONFIGURATION
// ============================================

const CONFIG = {
  // Gmail search criteria
  SENDER_EMAIL: 'ops_reporting@example.com',
  SEARCH_KEYWORDS: 'CEVA',
  
  // Google Drive folder name (will be created in root)
  DRIVE_FOLDER_NAME: 'WIGEON_CEVA_Reports',
  
  // Gmail label for processed emails
  PROCESSED_LABEL: 'WIGEON_Processed',
  
  // File types to download
  ALLOWED_EXTENSIONS: ['.xlsx', '.xls', '.csv', '.zip'],
  
  // Maximum emails to process per run (to avoid timeout)
  MAX_EMAILS_PER_RUN: 20,
  
  // Days to look back for reports
  DAYS_TO_SEARCH: 7
};

// ============================================
// MAIN FUNCTIONS
// ============================================

/**
 * Main function - Run this on a schedule (hourly or daily)
 * Collects CEVA report attachments and saves to Google Drive
 */
function collectCEVAReports() {
  console.log('🦆 WIGEON CEVA Report Collector - Starting...');
  
  try {
    // Get or create the destination folder
    const folder = getOrCreateFolder(CONFIG.DRIVE_FOLDER_NAME);
    console.log(`📁 Using folder: ${folder.getName()} (${folder.getId()})`);
    
    // Get or create the processed label
    const label = getOrCreateLabel(CONFIG.PROCESSED_LABEL);
    console.log(`🏷️ Using label: ${label.getName()}`);
    
    // Build search query
    const searchQuery = buildSearchQuery();
    console.log(`🔍 Search query: ${searchQuery}`);
    
    // Search for emails
    const threads = GmailApp.search(searchQuery, 0, CONFIG.MAX_EMAILS_PER_RUN);
    console.log(`📧 Found ${threads.length} email threads`);
    
    if (threads.length === 0) {
      console.log('✅ No new CEVA reports to process');
      return {
        success: true,
        message: 'No new reports found',
        filesProcessed: 0
      };
    }
    
    // Process each thread
    let totalFiles = 0;
    const processedFiles = [];
    
    for (const thread of threads) {
      const messages = thread.getMessages();
      
      for (const message of messages) {
        const attachments = message.getAttachments();
        const subject = message.getSubject();
        const date = message.getDate();
        
        for (const attachment of attachments) {
          const fileName = attachment.getName();
          
          // Check if it's an allowed file type
          if (isAllowedFileType(fileName)) {
            // Create unique filename with date prefix
            const datePrefix = Utilities.formatDate(date, 'America/Los_Angeles', 'yyyy-MM-dd');
            const uniqueFileName = `${datePrefix}_${fileName}`;
            
            // Check if file already exists
            if (!fileExists(folder, uniqueFileName)) {
              // Save to Google Drive
              const file = folder.createFile(attachment.copyBlob().setName(uniqueFileName));
              console.log(`✅ Saved: ${uniqueFileName}`);
              
              processedFiles.push({
                fileName: uniqueFileName,
                fileId: file.getId(),
                subject: subject,
                date: datePrefix,
                size: attachment.getSize()
              });
              
              totalFiles++;
            } else {
              console.log(`⏭️ Skipped (exists): ${uniqueFileName}`);
            }
          }
        }
      }
      
      // Add processed label to thread
      thread.addLabel(label);
    }
    
    // Log summary
    console.log(`\n🎉 WIGEON Collection Complete!`);
    console.log(`📊 Files saved: ${totalFiles}`);
    console.log(`📁 Folder: https://drive.google.com/drive/folders/${folder.getId()}`);
    
    // Create manifest file
    if (processedFiles.length > 0) {
      createManifest(folder, processedFiles);
    }
    
    return {
      success: true,
      message: `Processed ${totalFiles} files`,
      filesProcessed: totalFiles,
      files: processedFiles,
      folderId: folder.getId(),
      folderUrl: `https://drive.google.com/drive/folders/${folder.getId()}`
    };
    
  } catch (error) {
    console.error(`❌ Error: ${error.message}`);
    return {
      success: false,
      message: error.message,
      filesProcessed: 0
    };
  }
}

/**
 * Setup function - Run once to initialize folder and label
 */
function setupScript() {
  console.log('🦆 WIGEON Setup - Initializing...');
  
  // Create folder
  const folder = getOrCreateFolder(CONFIG.DRIVE_FOLDER_NAME);
  console.log(`✅ Folder created/found: ${folder.getName()}`);
  console.log(`   URL: https://drive.google.com/drive/folders/${folder.getId()}`);
  
  // Create label
  const label = getOrCreateLabel(CONFIG.PROCESSED_LABEL);
  console.log(`✅ Label created/found: ${label.getName()}`);
  
  // Test Gmail access
  const testQuery = `from:${CONFIG.SENDER_EMAIL} newer_than:1d`;
  const testThreads = GmailApp.search(testQuery, 0, 1);
  console.log(`✅ Gmail access working (found ${testThreads.length} test threads)`);
  
  console.log('\n🎉 Setup complete! You can now:');
  console.log('1. Run collectCEVAReports() manually to test');
  console.log('2. Set up a time-driven trigger for automatic collection');
  
  return {
    folderId: folder.getId(),
    folderUrl: `https://drive.google.com/drive/folders/${folder.getId()}`,
    labelName: label.getName()
  };
}

/**
 * Create a time-driven trigger to run hourly
 */
function createHourlyTrigger() {
  // Delete existing triggers first
  const triggers = ScriptApp.getProjectTriggers();
  for (const trigger of triggers) {
    if (trigger.getHandlerFunction() === 'collectCEVAReports') {
      ScriptApp.deleteTrigger(trigger);
    }
  }
  
  // Create new hourly trigger
  ScriptApp.newTrigger('collectCEVAReports')
    .timeBased()
    .everyHours(1)
    .create();
  
  console.log('✅ Hourly trigger created for collectCEVAReports()');
}

/**
 * Create a time-driven trigger to run daily at 7 AM
 */
function createDailyTrigger() {
  // Delete existing triggers first
  const triggers = ScriptApp.getProjectTriggers();
  for (const trigger of triggers) {
    if (trigger.getHandlerFunction() === 'collectCEVAReports') {
      ScriptApp.deleteTrigger(trigger);
    }
  }
  
  // Create new daily trigger at 7 AM
  ScriptApp.newTrigger('collectCEVAReports')
    .timeBased()
    .atHour(7)
    .everyDays(1)
    .create();
  
  console.log('✅ Daily trigger created for collectCEVAReports() at 7 AM');
}

// ============================================
// HELPER FUNCTIONS
// ============================================

/**
 * Build Gmail search query
 */
function buildSearchQuery() {
  const parts = [
    `from:${CONFIG.SENDER_EMAIL}`,
    CONFIG.SEARCH_KEYWORDS,
    `newer_than:${CONFIG.DAYS_TO_SEARCH}d`,
    'has:attachment',
    `-label:${CONFIG.PROCESSED_LABEL}`
  ];
  return parts.join(' ');
}

/**
 * Get or create a Google Drive folder
 */
function getOrCreateFolder(folderName) {
  const folders = DriveApp.getFoldersByName(folderName);
  
  if (folders.hasNext()) {
    return folders.next();
  }
  
  return DriveApp.createFolder(folderName);
}

/**
 * Get or create a Gmail label
 */
function getOrCreateLabel(labelName) {
  let label = GmailApp.getUserLabelByName(labelName);
  
  if (!label) {
    label = GmailApp.createLabel(labelName);
  }
  
  return label;
}

/**
 * Check if file type is allowed
 */
function isAllowedFileType(fileName) {
  const lowerName = fileName.toLowerCase();
  return CONFIG.ALLOWED_EXTENSIONS.some(ext => lowerName.endsWith(ext));
}

/**
 * Check if file already exists in folder
 */
function fileExists(folder, fileName) {
  const files = folder.getFilesByName(fileName);
  return files.hasNext();
}

/**
 * Create a manifest file with processing details
 */
function createManifest(folder, files) {
  const timestamp = Utilities.formatDate(new Date(), 'America/Los_Angeles', 'yyyy-MM-dd_HH-mm-ss');
  const manifestName = `_manifest_${timestamp}.json`;
  
  const manifest = {
    timestamp: timestamp,
    totalFiles: files.length,
    files: files
  };
  
  folder.createFile(manifestName, JSON.stringify(manifest, null, 2), 'application/json');
  console.log(`📋 Manifest created: ${manifestName}`);
}

/**
 * Get folder ID for WIGEON integration
 */
function getFolderId() {
  const folder = getOrCreateFolder(CONFIG.DRIVE_FOLDER_NAME);
  return folder.getId();
}

/**
 * List all files in the CEVA reports folder
 */
function listFiles() {
  const folder = getOrCreateFolder(CONFIG.DRIVE_FOLDER_NAME);
  const files = folder.getFiles();
  
  const fileList = [];
  while (files.hasNext()) {
    const file = files.next();
    fileList.push({
      name: file.getName(),
      id: file.getId(),
      size: file.getSize(),
      created: file.getDateCreated(),
      url: file.getUrl()
    });
  }
  
  console.log(`📁 Files in ${CONFIG.DRIVE_FOLDER_NAME}:`);
  fileList.forEach(f => console.log(`  - ${f.name} (${f.size} bytes)`));
  
  return fileList;
}

/**
 * Clear processed label from all emails (for reprocessing)
 */
function clearProcessedLabel() {
  const label = GmailApp.getUserLabelByName(CONFIG.PROCESSED_LABEL);
  if (label) {
    const threads = label.getThreads();
    for (const thread of threads) {
      thread.removeLabel(label);
    }
    console.log(`✅ Removed ${CONFIG.PROCESSED_LABEL} label from ${threads.length} threads`);
  }
}
