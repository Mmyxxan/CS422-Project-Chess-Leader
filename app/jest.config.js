module.exports = {
  snapshotSerializers: ['jest-emotion'],
  transform: {
    '^.+\\.[tj]sx?$': 'babel-jest',
  },
  testRegex: '/__tests__/.*\\.(ts|tsx|js)$',
  collectCoverageFrom: ['src/**/*.{ts,tsx}'],
  setupFilesAfterEnv: ['./test/setup/setup.js'],
  testEnvironment: 'jsdom',
  transformIgnorePatterns: [
    'node_modules/(?!(react-dnd|dnd-core|@react-dnd|@react-dnd/invariant|@react-dnd/shallowequal|@react-dnd/asap)/)' 
  ],
};
