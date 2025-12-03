#!/usr/bin/env node

/**
 * Demo script for Apollo
 * Initializes Apollo programmatically, sends example commands, and prints responses.
 */

const Apollo = require('../src/apollo');

async function runDemo() {
  const apollo = new Apollo();
  await apollo.initialize();

  console.log('\n--- Demo: Presenting to Apollo ---\n');

  const commands = [
    'greet',
    'describe yourself',
    'summarize project',
    'shutdown'
  ];

  for (const cmd of commands) {
    try {
      const res = await apollo.process(cmd);
      console.log('> Command:', cmd);
      console.log('  Response:', JSON.stringify(res, null, 2), '\n');
    } catch (err) {
      console.error('Error processing command:', err.message);
    }
  }

  console.log('--- Demo complete ---\n');
}

runDemo().catch((err) => {
  console.error('Demo failed:', err.message);
  process.exit(1);
});
