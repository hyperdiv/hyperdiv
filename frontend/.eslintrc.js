module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
  },
  extends: [
    "eslint:recommended",
    "airbnb",
    "prettier",
    "plugin:jsx-a11y/strict",
  ],
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 12,
    sourceType: "module",
  },
  plugins: ["prettier", "jsx-a11y"],
  rules: {
    "no-underscore-dangle": ["error", { allowAfterThis: true }],
    // multiple classes per file are fine:
    "max-classes-per-file": ["off"],
    "import/no-extraneous-dependencies": ["off"],
    "import/extensions": ["off"],
    // Having to always destructure is annoying:
    "prefer-destructuring": ["off"],
    "no-return-assign": ["off"],
    // foo++ is ok:
    "no-plusplus": ["off"],
    // Can declare vars anywhere:
    "one-var": ["off"],
    // Mutually-recursive functions are normal:
    "no-use-before-define": ["error", { functions: false }],
    // Functions can mutate their inputs:
    "no-param-reassign": ["off"],
    // For-of syntax is fine:
    "no-restricted-syntax": ["off"],
    // Non-default exports are fine:
    "import/prefer-default-export": ["off"],
    // ("foo" + bar) is ok:
    "prefer-template": ["off"],
    // while (true) is ok
    "no-constant-condition": ["off"],
    // no-await-in-loop is too restrictive.
    "no-await-in-loop": ["off"],
    // continue statements in loops are fine
    "no-continue": ["off"],
    "no-shadow": ["off"],
  },
  settings: {},
  overrides: [],
};
