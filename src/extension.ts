/**
 * NetAssist VS Code Extension
 * AI-powered network engineering assistant with secure IP sanitization
 */

import * as vscode from 'vscode';
import { NetAssistantProvider } from './providers/NetAssistantProvider';
import { SanitizationProvider } from './providers/SanitizationProvider';
import { PyATSProvider } from './providers/PyATSProvider';
import { NetworkModeManager } from './core/NetworkModeManager';
import { ConfigurationManager } from './core/ConfigurationManager';

let netAssistantProvider: NetAssistantProvider;
let sanitizationProvider: SanitizationProvider;
let pyatsProvider: PyATSProvider;
let networkModeManager: NetworkModeManager;

export function activate(context: vscode.ExtensionContext) {
    console.log('NetAssist extension is now active!');

    // Initialize configuration manager
    const configManager = new ConfigurationManager();

    // Initialize core providers
    sanitizationProvider = new SanitizationProvider(configManager);
    pyatsProvider = new PyATSProvider(configManager);
    networkModeManager = new NetworkModeManager(sanitizationProvider, pyatsProvider);

    // Initialize main provider
    netAssistantProvider = new NetAssistantProvider(
        context,
        networkModeManager,
        sanitizationProvider,
        configManager
    );

    // Register webview provider
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(
            'netassist.chatView',
            netAssistantProvider,
            {
                webviewOptions: {
                    retainContextWhenHidden: true
                }
            }
        )
    );

    // Register commands
    registerCommands(context);

    // Show welcome message on first activation
    if (context.globalState.get('netassist.firstActivation', true)) {
        vscode.window.showInformationMessage(
            'Welcome to NetAssist! Your AI network engineering assistant is ready.',
            'Open NetAssist',
            'View Documentation'
        ).then(selection => {
            if (selection === 'Open NetAssist') {
                vscode.commands.executeCommand('netassist.openChat');
            } else if (selection === 'View Documentation') {
                vscode.env.openExternal(vscode.Uri.parse('https://github.com/netassist/vscode-extension'));
            }
        });
        context.globalState.update('netassist.firstActivation', false);
    }

    // Check sanitization server connectivity
    sanitizationProvider.checkServerHealth().then(isHealthy => {
        if (!isHealthy) {
            vscode.window.showWarningMessage(
                'NetAssist sanitization server is not running. Some features may be limited.',
                'Start Server',
                'Learn More'
            ).then(selection => {
                if (selection === 'Start Server') {
                    vscode.commands.executeCommand('netassist.startSanitizationServer');
                } else if (selection === 'Learn More') {
                    vscode.env.openExternal(vscode.Uri.parse('https://github.com/netassist/sanitization-server'));
                }
            });
        }
    });
}

function registerCommands(context: vscode.ExtensionContext) {
    // Core commands
    context.subscriptions.push(
        vscode.commands.registerCommand('netassist.openChat', () => {
            vscode.commands.executeCommand('netassist-sidebar.focus');
            vscode.commands.executeCommand('netassist.chatView.focus');
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('netassist.newSession', () => {
            netAssistantProvider.createNewSession();
            vscode.window.showInformationMessage('New NetAssist session started');
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('netassist.switchMode', async () => {
            const modes = [
                { label: 'Configuration', value: 'config', description: 'Network configuration assistance' },
                { label: 'Troubleshooting', value: 'troubleshoot', description: 'Network issue diagnosis' },
                { label: 'Validation', value: 'validate', description: 'Configuration validation and testing' },
                { label: 'Documentation', value: 'document', description: 'Cisco documentation lookup' }
            ];

            const selection = await vscode.window.showQuickPick(modes, {
                placeHolder: 'Select NetAssist mode'
            });

            if (selection) {
                await networkModeManager.setMode(selection.value);
                vscode.window.showInformationMessage(`Switched to ${selection.label} mode`);
            }
        })
    );

    // Sanitization commands
    context.subscriptions.push(
        vscode.commands.registerCommand('netassist.sanitizeSelection', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                vscode.window.showWarningMessage('No active editor found');
                return;
            }

            const selection = editor.selection;
            const text = editor.document.getText(selection);

            if (!text) {
                vscode.window.showWarningMessage('No text selected');
                return;
            }

            try {
                const result = await sanitizationProvider.sanitize(text);

                // Replace selection with sanitized text
                await editor.edit(editBuilder => {
                    editBuilder.replace(selection, result.sanitized_text);
                });

                vscode.window.showInformationMessage(
                    `Sanitized ${result.entity_count} network entities`
                );
            } catch (error) {
                vscode.window.showErrorMessage(`Sanitization failed: ${error}`);
            }
        })
    );

    // pyATS commands
    context.subscriptions.push(
        vscode.commands.registerCommand('netassist.generatePyATS', async () => {
            const testType = await vscode.window.showQuickPick([
                { label: 'Health Check', value: 'health' },
                { label: 'Interface Validation', value: 'interface' },
                { label: 'Routing Validation', value: 'routing' },
                { label: 'Custom Test', value: 'custom' }
            ], {
                placeHolder: 'Select pyATS test type'
            });

            if (!testType) {
                return;
            }

            try {
                const script = await pyatsProvider.generateScript(testType.value);

                // Create new document with generated script
                const document = await vscode.workspace.openTextDocument({
                    content: script,
                    language: 'python'
                });

                await vscode.window.showTextDocument(document);
                vscode.window.showInformationMessage('pyATS script generated successfully');
            } catch (error) {
                vscode.window.showErrorMessage(`pyATS generation failed: ${error}`);
            }
        })
    );

    // Documentation commands
    context.subscriptions.push(
        vscode.commands.registerCommand('netassist.loadCiscoDocs', async () => {
            const url = await vscode.window.showInputBox({
                prompt: 'Enter Cisco documentation URL',
                placeholder: 'https://www.cisco.com/c/en/us/support/docs/...'
            });

            if (!url) {
                return;
            }

            const project = await vscode.window.showInputBox({
                prompt: 'Describe your project context',
                placeholder: 'e.g., CUCM upgrade planning, BGP troubleshooting'
            });

            if (!project) {
                return;
            }

            try {
                // This would integrate with our cisco-doc-fetcher
                vscode.window.showInformationMessage('Loading Cisco documentation...');

                // Send to chat for processing
                await netAssistantProvider.loadDocumentation(url, project);

                vscode.window.showInformationMessage('Documentation loaded successfully');
            } catch (error) {
                vscode.window.showErrorMessage(`Documentation loading failed: ${error}`);
            }
        })
    );

    // Troubleshooting workflow
    context.subscriptions.push(
        vscode.commands.registerCommand('netassist.startTroubleshooting', async () => {
            const issue = await vscode.window.showInputBox({
                prompt: 'Describe the network issue you\'re troubleshooting',
                placeholder: 'e.g., Users cannot access internal servers'
            });

            if (!issue) {
                return;
            }

            // Switch to troubleshooting mode and start workflow
            await networkModeManager.setMode('troubleshoot');
            await netAssistantProvider.startTroubleshootingWorkflow(issue);

            // Focus on chat view
            vscode.commands.executeCommand('netassist.openChat');
        })
    );

    // Configuration validation
    context.subscriptions.push(
        vscode.commands.registerCommand('netassist.validateConfig', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                vscode.window.showWarningMessage('No active editor found');
                return;
            }

            const config = editor.document.getText();
            if (!config) {
                vscode.window.showWarningMessage('No configuration found');
                return;
            }

            try {
                // Switch to validation mode
                await networkModeManager.setMode('validate');

                // Process configuration through AI
                const analysis = await networkModeManager.processRequest(
                    'Please analyze this network configuration for errors, best practices, and security issues:\n\n' + config
                );

                // Show results in new document
                const document = await vscode.workspace.openTextDocument({
                    content: `# Configuration Analysis\n\n${analysis}`,
                    language: 'markdown'
                });

                await vscode.window.showTextDocument(document, vscode.ViewColumn.Beside);
            } catch (error) {
                vscode.window.showErrorMessage(`Configuration validation failed: ${error}`);
            }
        })
    );

    // Settings command
    context.subscriptions.push(
        vscode.commands.registerCommand('netassist.openSettings', () => {
            vscode.commands.executeCommand('workbench.action.openSettings', 'netassist');
        })
    );
}

export function deactivate() {
    console.log('NetAssist extension is now deactivated');

    // Cleanup
    if (sanitizationProvider) {
        sanitizationProvider.dispose();
    }
}