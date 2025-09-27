/**
 * NetworkModeManager - Core network-specific AI mode routing
 * Routes requests to appropriate network domain experts
 */

import { SanitizationProvider } from '../providers/SanitizationProvider';
import { PyATSProvider } from '../providers/PyATSProvider';
import { ConfigMode } from '../modes/ConfigMode';
import { TroubleshootMode } from '../modes/TroubleshootMode';
import { ValidateMode } from '../modes/ValidateMode';
import { DocumentMode } from '../modes/DocumentMode';

export type NetworkMode = 'config' | 'troubleshoot' | 'validate' | 'document';

export interface NetworkModeHandler {
    processRequest(request: string, context?: any): Promise<string>;
    getSystemPrompt(): string;
    getSuggestedActions(): string[];
}

export interface ModeContext {
    sessionId?: string;
    previousExchanges?: string[];
    currentIssue?: string;
    detectedEntities?: any[];
}

export class NetworkModeManager {
    private currentMode: NetworkMode = 'config';
    private modes: Map<NetworkMode, NetworkModeHandler>;
    private context: ModeContext = {};

    constructor(
        private sanitizationProvider: SanitizationProvider,
        private pyatsProvider: PyATSProvider
    ) {
        // Initialize mode handlers
        this.modes = new Map([
            ['config', new ConfigMode(sanitizationProvider, pyatsProvider)],
            ['troubleshoot', new TroubleshootMode(sanitizationProvider, pyatsProvider)],
            ['validate', new ValidateMode(sanitizationProvider, pyatsProvider)],
            ['document', new DocumentMode(sanitizationProvider, pyatsProvider)]
        ]);
    }

    /**
     * Process a request through the current mode
     */
    async processRequest(request: string): Promise<string> {
        const modeHandler = this.modes.get(this.currentMode);
        if (!modeHandler) {
            throw new Error(`Unknown mode: ${this.currentMode}`);
        }

        try {
            // Add request to context for future reference
            if (!this.context.previousExchanges) {
                this.context.previousExchanges = [];
            }
            this.context.previousExchanges.push(`User: ${request}`);

            // Process through current mode
            const response = await modeHandler.processRequest(request, this.context);

            // Add response to context
            this.context.previousExchanges.push(`Assistant: ${response}`);

            // Keep only last 10 exchanges to prevent context bloat
            if (this.context.previousExchanges.length > 20) {
                this.context.previousExchanges = this.context.previousExchanges.slice(-20);
            }

            return response;
        } catch (error) {
            const errorMessage = `Error in ${this.currentMode} mode: ${error}`;
            console.error(errorMessage);
            throw new Error(errorMessage);
        }
    }

    /**
     * Set the current mode
     */
    async setMode(mode: NetworkMode): Promise<void> {
        if (!this.modes.has(mode)) {
            throw new Error(`Invalid mode: ${mode}`);
        }

        this.currentMode = mode;

        // Clear context when switching modes (optional)
        this.context = {
            sessionId: this.context.sessionId // Preserve session ID
        };
    }

    /**
     * Get current mode
     */
    getCurrentMode(): NetworkMode {
        return this.currentMode;
    }

    /**
     * Get system prompt for current mode
     */
    getCurrentSystemPrompt(): string {
        const modeHandler = this.modes.get(this.currentMode);
        return modeHandler?.getSystemPrompt() || '';
    }

    /**
     * Get suggested actions for current mode
     */
    getCurrentSuggestedActions(): string[] {
        const modeHandler = this.modes.get(this.currentMode);
        return modeHandler?.getSuggestedActions() || [];
    }

    /**
     * Intelligently suggest mode based on request content
     */
    suggestMode(request: string): NetworkMode {
        const lowerRequest = request.toLowerCase();

        // Troubleshooting keywords
        if (this.containsKeywords(lowerRequest, [
            'error', 'issue', 'problem', 'troubleshoot', 'debug', 'not working',
            'can\'t connect', 'connectivity', 'timeout', 'failed', 'down'
        ])) {
            return 'troubleshoot';
        }

        // Validation keywords
        if (this.containsKeywords(lowerRequest, [
            'validate', 'test', 'verify', 'check', 'pyats', 'health check',
            'compliance', 'audit', 'review'
        ])) {
            return 'validate';
        }

        // Documentation keywords
        if (this.containsKeywords(lowerRequest, [
            'documentation', 'docs', 'manual', 'guide', 'how to',
            'cisco.com', 'reference', 'best practice'
        ])) {
            return 'document';
        }

        // Configuration keywords (default)
        if (this.containsKeywords(lowerRequest, [
            'config', 'configure', 'setup', 'install', 'create',
            'vlan', 'interface', 'bgp', 'ospf', 'routing'
        ])) {
            return 'config';
        }

        // Default to current mode if no clear indication
        return this.currentMode;
    }

    /**
     * Auto-switch mode based on request if appropriate
     */
    async autoSwitchMode(request: string): Promise<boolean> {
        const suggestedMode = this.suggestMode(request);

        if (suggestedMode !== this.currentMode) {
            await this.setMode(suggestedMode);
            return true;
        }

        return false;
    }

    /**
     * Get context for current session
     */
    getContext(): ModeContext {
        return { ...this.context };
    }

    /**
     * Set context (useful for maintaining state across requests)
     */
    setContext(context: Partial<ModeContext>): void {
        this.context = { ...this.context, ...context };
    }

    /**
     * Reset context
     */
    resetContext(): void {
        const sessionId = this.context.sessionId;
        this.context = { sessionId };
    }

    /**
     * Get mode information
     */
    getModeInfo(): { [key in NetworkMode]: { name: string; description: string; icon: string } } {
        return {
            config: {
                name: 'Configuration',
                description: 'Network device configuration assistance',
                icon: '$(settings-gear)'
            },
            troubleshoot: {
                name: 'Troubleshooting',
                description: 'Network issue diagnosis and resolution',
                icon: '$(search)'
            },
            validate: {
                name: 'Validation',
                description: 'Configuration validation and testing',
                icon: '$(verified)'
            },
            document: {
                name: 'Documentation',
                description: 'Cisco documentation and reference lookup',
                icon: '$(book)'
            }
        };
    }

    /**
     * Generate mode-specific context prompt
     */
    generateContextPrompt(): string {
        const modeInfo = this.getModeInfo()[this.currentMode];
        let prompt = `Current mode: ${modeInfo.name} - ${modeInfo.description}\n\n`;

        // Add system prompt
        prompt += this.getCurrentSystemPrompt() + '\n\n';

        // Add recent context if available
        if (this.context.previousExchanges && this.context.previousExchanges.length > 0) {
            prompt += 'Recent conversation:\n';
            prompt += this.context.previousExchanges.slice(-6).join('\n') + '\n\n';
        }

        // Add current issue context if available
        if (this.context.currentIssue) {
            prompt += `Current issue: ${this.context.currentIssue}\n\n`;
        }

        return prompt;
    }

    /**
     * Check if text contains any of the given keywords
     */
    private containsKeywords(text: string, keywords: string[]): boolean {
        return keywords.some(keyword => text.includes(keyword));
    }

    /**
     * Get all available modes
     */
    getAvailableModes(): NetworkMode[] {
        return Array.from(this.modes.keys());
    }

    /**
     * Validate mode
     */
    isValidMode(mode: string): mode is NetworkMode {
        return this.modes.has(mode as NetworkMode);
    }
}