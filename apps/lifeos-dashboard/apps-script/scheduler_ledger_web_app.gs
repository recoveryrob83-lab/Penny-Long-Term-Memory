const LEDGER_SPREADSHEET_ID = '1o5Qkzntd5OmKX7Vxix-PbhbuyPigJvss1AkP7Kvb0Q4';
const DEFAULT_SHEET_NAME = 'Run Ledger';
const EXPECTED_VALUE_COUNT = 17;

function doGet() {
  return jsonResponse_({
    ok: true,
    service: 'LifeOS Scheduler Ledger',
    message: 'POST requests only update the ledger.',
  });
}

function doPost(event) {
  try {
    const payload = parsePayload_(event);
    authorize_(payload);

    if (String(payload.spreadsheet_id || '') !== LEDGER_SPREADSHEET_ID) {
      throw new Error('Spreadsheet ID mismatch.');
    }

    const spreadsheet = SpreadsheetApp.openById(LEDGER_SPREADSHEET_ID);
    const sheetName =
      PropertiesService.getScriptProperties().getProperty('LEDGER_SHEET_NAME') ||
      DEFAULT_SHEET_NAME;

    if (String(payload.sheet_name || '') !== sheetName) {
      throw new Error('Sheet name mismatch.');
    }

    const sheet = spreadsheet.getSheetByName(sheetName);
    if (!sheet) {
      throw new Error(`Sheet tab not found: ${sheetName}`);
    }

    const lock = LockService.getScriptLock();
    lock.waitLock(10000);
    try {
      const action = String(payload.action || '');
      if (action === 'ping') {
        return successResponse_(spreadsheet, sheetName, action, null);
      }
      if (action === 'upsert') {
        const rowNumber = upsertSchedule_(sheet, payload);
        SpreadsheetApp.flush();
        return successResponse_(spreadsheet, sheetName, action, rowNumber);
      }
      if (action === 'remove') {
        const rowNumber = removeSchedule_(sheet, payload);
        SpreadsheetApp.flush();
        return successResponse_(spreadsheet, sheetName, action, rowNumber);
      }
      throw new Error('Unsupported ledger action.');
    } finally {
      lock.releaseLock();
    }
  } catch (error) {
    return jsonResponse_({
      ok: false,
      error: error && error.message ? error.message : String(error),
    });
  }
}

function parsePayload_(event) {
  const contents = event && event.postData ? event.postData.contents : '';
  if (!contents) {
    throw new Error('Missing JSON request body.');
  }
  const payload = JSON.parse(contents);
  if (!payload || typeof payload !== 'object' || Array.isArray(payload)) {
    throw new Error('Request body must be a JSON object.');
  }
  return payload;
}

function authorize_(payload) {
  const expectedSecret =
    PropertiesService.getScriptProperties().getProperty('LEDGER_SECRET');
  if (!expectedSecret) {
    throw new Error('LEDGER_SECRET is not configured in Script Properties.');
  }
  const suppliedSecret = String(payload.secret || '');
  if (!constantTimeEqual_(suppliedSecret, expectedSecret)) {
    throw new Error('Unauthorized ledger request.');
  }
}

function constantTimeEqual_(left, right) {
  const leftText = String(left);
  const rightText = String(right);
  let difference = leftText.length ^ rightText.length;
  const length = Math.max(leftText.length, rightText.length);
  for (let index = 0; index < length; index += 1) {
    difference |=
      (leftText.charCodeAt(index) || 0) ^ (rightText.charCodeAt(index) || 0);
  }
  return difference === 0;
}

function upsertSchedule_(sheet, payload) {
  const scheduleId = requireScheduleId_(payload.schedule_id);
  const values = payload.values;
  if (!Array.isArray(values) || values.length !== EXPECTED_VALUE_COUNT) {
    throw new Error(`Upsert requires exactly ${EXPECTED_VALUE_COUNT} values.`);
  }

  compactBlankScheduleRows_(sheet);
  const rowNumber = findScheduleRow_(sheet, scheduleId, true);
  writeScheduleRow_(sheet, rowNumber, values);
  return rowNumber;
}

function removeSchedule_(sheet, payload) {
  const scheduleId = requireScheduleId_(payload.schedule_id);
  compactBlankScheduleRows_(sheet);
  const rowNumber = findScheduleRow_(sheet, scheduleId, false);
  if (rowNumber !== null) {
    sheet.deleteRow(rowNumber);
  }
  return rowNumber;
}

function compactBlankScheduleRows_(sheet) {
  const lastRow = sheet.getLastRow();
  if (lastRow <= 1) {
    return;
  }

  const identifiers = sheet.getRange(2, 1, lastRow - 1, 1).getDisplayValues();
  const blankRows = [];
  for (let index = 0; index < identifiers.length; index += 1) {
    if (!String(identifiers[index][0] || '').trim()) {
      blankRows.push(index + 2);
    }
  }

  for (let index = blankRows.length - 1; index >= 0; index -= 1) {
    sheet.deleteRow(blankRows[index]);
  }
}

function requireScheduleId_(value) {
  const scheduleId = Number(value);
  if (!Number.isInteger(scheduleId) || scheduleId <= 0) {
    throw new Error('schedule_id must be a positive integer.');
  }
  return scheduleId;
}

function findScheduleRow_(sheet, scheduleId, allowBlankRow) {
  const lastRow = Math.max(1, sheet.getLastRow());
  if (lastRow === 1) {
    return allowBlankRow ? 2 : null;
  }

  const identifiers = sheet.getRange(2, 1, lastRow - 1, 1).getDisplayValues();
  let firstBlankRow = null;
  for (let index = 0; index < identifiers.length; index += 1) {
    const rowNumber = index + 2;
    const value = String(identifiers[index][0] || '').trim();
    if (value === String(scheduleId)) {
      return rowNumber;
    }
    if (!value && firstBlankRow === null) {
      firstBlankRow = rowNumber;
    }
  }

  if (!allowBlankRow) {
    return null;
  }
  return firstBlankRow === null ? lastRow + 1 : firstBlankRow;
}

function writeScheduleRow_(sheet, rowNumber, values) {
  sheet.getRange(rowNumber, 1).setValue(Number(values[0]));
  setPlainTextValues_(sheet.getRange(rowNumber, 2, 1, 7), values.slice(1, 8));
  sheet.getRange(rowNumber, 9).setValue(Boolean(values[8]));
  setPlainTextValues_(sheet.getRange(rowNumber, 10, 1, 3), values.slice(9, 12));
  sheet.getRange(rowNumber, 13, 1, 2).setValues([[values[12], values[13]]]);
  setPlainTextValues_(sheet.getRange(rowNumber, 15, 1, 2), values.slice(14, 16));
  sheet.getRange(rowNumber, 17).setValue(values[16]);
  sheet.getRange(rowNumber, 18).setFormula(healthFormula_(rowNumber));
}

function setPlainTextValues_(range, values) {
  range.setNumberFormat('@');
  range.setValues([values.map((value) => String(value == null ? '' : value))]);
}

function healthFormula_(rowNumber) {
  return (
    `=IF(J${rowNumber}<>"Active",J${rowNumber},` +
    `IF(M${rowNumber}="","No future run",` +
    `IF(M${rowNumber}+TIME(0,5,0)<NOW(),"OVERDUE","On schedule")))`
  );
}

function successResponse_(spreadsheet, sheetName, action, rowNumber) {
  return jsonResponse_({
    ok: true,
    action: action,
    row: rowNumber,
    spreadsheet_id: spreadsheet.getId(),
    sheet_name: sheetName,
  });
}

function jsonResponse_(payload) {
  return ContentService.createTextOutput(JSON.stringify(payload)).setMimeType(
    ContentService.MimeType.JSON,
  );
}
