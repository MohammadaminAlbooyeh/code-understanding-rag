export function isValidCode(code) {
  return code && code.trim().length > 0;
}

export function isValidLanguage(language) {
  const supported = ['python', 'javascript', 'typescript', 'java', 'go', 'cpp'];
  return supported.includes(language.toLowerCase());
}

export function isValidFileSize(file, maxSize = 10 * 1024 * 1024) {
  return file.size <= maxSize;
}
