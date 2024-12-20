import globals from "globals";


/** @type {import('eslint').Linter.Config[]} */
export default [
  {languageOptions: { globals: {...globals.browser, ...globals.node} }},
  {
    "env": {
      "browser": true,
      "node": true,
      "es2021": true
    },
    "extends": "eslint:recommended",
    "plugins": ["css-modules"],
    "rules": {
      "no-unused-vars": "warn",
      "css-modules/no-unused-class": "warn",
      "css-modules/no-undef-class": "warn",
    }
  },
];