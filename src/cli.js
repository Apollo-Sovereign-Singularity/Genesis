#!/usr/bin/env node

/**
 * Apollo CLI - Cursor Agent Integration
 * Interface to interact with Apollo via command line
 */

const Apollo = require('./apollo');
const readline = require('readline');

class ApolloCLI {
  constructor() {
    this.apollo = new Apollo();
    this.rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
  }

  async start() {
    await this.apollo.initialize();
    
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('Apollo CLI - Sovereign AI');
    console.log('Type "help" for available commands');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    
    this.prompt();
  }

  prompt() {
    this.rl.question('apollo> ', async (input) => {
      if (!input.trim()) {
        this.prompt();
        return;
      }

      const command = input.trim().toLowerCase();

      try {
        switch (command) {
          case 'help':
            this.showHelp();
            break;
          case 'status':
            console.log(JSON.stringify(this.apollo.getStatus(), null, 2));
            break;
          case 'exit':
          case 'quit':
            console.log('\nApollo shutting down. Long live the Singularity.\n');
            this.rl.close();
            process.exit(0);
            break;
          default:
            const result = await this.apollo.process(input);
            console.log('Result:', result);
        }
      } catch (error) {
        console.error('Error:', error.message);
      }

      this.prompt();
    });
  }

  showHelp() {
    console.log(`
Apollo CLI Commands:
  help              - Show this help message
  status            - Display Apollo's current status
  exit / quit       - Exit the CLI
  [command]         - Send command to Apollo for processing
    `);
  }
}

// Start CLI
const cli = new ApolloCLI();
cli.start().catch((error) => {
  console.error('Fatal error:', error.message);
  process.exit(1);
});
