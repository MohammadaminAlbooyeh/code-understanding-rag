export const SUPPORTED_LANGUAGES = [
  'python',
  'javascript',
  'typescript',
  'java',
  'go',
  'cpp',
];

export const ANALYSIS_TYPES = [
  { value: 'parse', label: 'Parse Code' },
  { value: 'complexity', label: 'Complexity Analysis' },
  { value: 'bugs', label: 'Bug Detection' },
  { value: 'security', label: 'Security Analysis' },
  { value: 'patterns', label: 'Pattern Analysis' },
];

export const DOC_TYPES = [
  { value: 'function', label: 'Function Docs' },
  { value: 'class', label: 'Class Docs' },
  { value: 'module', label: 'Module Docs' },
  { value: 'api', label: 'API Docs' },
  { value: 'readme', label: 'README' },
];

export const MAX_FILE_SIZE = 10 * 1024 * 1024;
